# ============================================
# ai_extractor.py
# Pakai Groq Vision — GRATIS!
# Daftar API key di: console.groq.com
# ============================================

import groq
import base64
import json
import re
import time
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Setup Groq
client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"  # gratis & support vision


def extract_data_from_image(image_path: str) -> dict:
    """Kirim gambar ke Groq, ekstrak data jadi JSON."""

    # Baca dan encode gambar ke base64
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    # Deteksi tipe file
    ext = Path(image_path).suffix.lower()
    mime_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp"
    }
    mime_type = mime_map.get(ext, "image/jpeg")

    prompt = """
    Analisa gambar ini dan ekstrak SEMUA data/informasi penting.
    
    Gambar bisa berupa apapun: struk, nota, tabel, form, kwitansi, 
    menu, daftar harga, laporan, dll.
    
    Return HANYA JSON valid, tanpa teks lain:
    {
        "tipe_dokumen": "struk/nota/tabel/form/lainnya",
        "judul": "judul dokumen jika ada",
        "tanggal": "tanggal jika ada format YYYY-MM-DD",
        "data": [
            {"kolom1": "nilai1", "kolom2": "nilai2"}
        ],
        "total": "nilai total jika ada",
        "catatan": "informasi penting lainnya"
    }
    
    Sesuaikan nama kolom di 'data' dengan isi dokumen.
    Struk: nama_item, qty, harga_satuan, subtotal
    Tabel: ikuti header tabel yang ada di gambar
    HANYA JSON, tanpa penjelasan apapun di luar JSON.
    """

    # Retry otomatis jika kena rate limit
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{image_b64}"
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ],
                max_tokens=2000,
                temperature=0.1
            )
            break  # sukses, keluar loop

        except groq.RateLimitError:
            if attempt < 2:
                wait = 15 * (attempt + 1)
                print(f"Rate limit, tunggu {wait} detik...")
                time.sleep(wait)
            else:
                raise
        except Exception:
            raise

    raw_text = response.choices[0].message.content.strip()

    # Bersihkan markdown jika ada
    raw_text = re.sub(r"```json\n?", "", raw_text)
    raw_text = re.sub(r"```\n?", "", raw_text)

    return json.loads(raw_text)


def format_summary(extracted: dict) -> str:
    """Ringkasan hasil ekstraksi untuk dikirim ke user."""

    def safe(text):
        """Hapus karakter yang bisa merusak pesan Telegram."""
        if not text:
            return ""
        # Hapus karakter spesial Markdown
        for ch in ["*", "_", "`", "[", "]", "(", ")", "#"]:
            text = str(text).replace(ch, "")
        return text

    lines = []
    lines.append(f"✅ Berhasil membaca {safe(extracted.get('tipe_dokumen', 'dokumen'))}")

    if extracted.get("judul"):
        lines.append(f"📄 Judul: {safe(extracted['judul'])}")

    if extracted.get("tanggal"):
        lines.append(f"📅 Tanggal: {safe(extracted['tanggal'])}")

    data = extracted.get("data", [])
    lines.append(f"📊 {len(data)} baris data ditemukan")

    if extracted.get("total"):
        lines.append(f"💰 Total: {safe(extracted['total'])}")

    if extracted.get("catatan"):
        lines.append(f"📝 {safe(extracted['catatan'])}")

    lines.append("\n📎 File Excel siap!")
    return "\n".join(lines)