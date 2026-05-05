# ============================================
# telegram_bot.py - Versi Google Sheets
# ============================================

import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes
)
from ai_extractor import extract_data_from_image, format_summary
from sheets_handler import save_to_sheets

load_dotenv()
logging.basicConfig(level=logging.INFO)

DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Halo! Saya bot pencatat data dari foto.\n\n"
        "📸 Kirimkan foto apapun:\n"
        "  • Struk / nota belanja\n"
        "  • Tabel / dokumen\n"
        "  • Form / kwitansi\n\n"
        "Saya akan ekstrak datanya dan simpan ke Google Sheets. ✅"
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_path = None
    msg = await update.message.reply_text("⏳ Sedang memproses foto kamu...")

    try:
        # 1. Download foto
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        image_path = DOWNLOAD_DIR / f"{photo.file_id}.jpg"
        await file.download_to_drive(str(image_path))

        await msg.edit_text("🔍 Menganalisa gambar dengan AI...")

        # 2. Ekstrak data dengan Groq AI
        extracted = extract_data_from_image(str(image_path))

        await msg.edit_text("📊 Menyimpan ke Google Sheets...")

        # 3. Simpan ke Google Sheets
        from_user = update.message.from_user.first_name or "unknown"
        sheet_url = save_to_sheets(extracted, from_user)

        # 4. Kirim ringkasan ke user
        summary = format_summary(extracted)
        await msg.edit_text(
            summary + f"\n\n🔗 Lihat Google Sheets:\n{sheet_url}"
        )

    except Exception as e:
        logging.error(f"Error handle_photo: {e}")
        await msg.edit_text(
            "❌ Gagal memproses foto.\n"
            "Pastikan foto cukup jelas dan coba lagi."
        )
    finally:
        import time
        time.sleep(0.3)
        if image_path and Path(image_path).exists():
            try:
                Path(image_path).unlink()
            except Exception:
                pass


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_path = None
    doc = update.message.document

    if not doc.mime_type.startswith("image/"):
        await update.message.reply_text("❌ Harap kirim file gambar (JPG, PNG, dll)")
        return

    msg = await update.message.reply_text("⏳ Sedang memproses file kamu...")

    try:
        file = await context.bot.get_file(doc.file_id)
        ext = Path(doc.file_name).suffix or ".jpg"
        image_path = DOWNLOAD_DIR / f"{doc.file_id}{ext}"
        await file.download_to_drive(str(image_path))

        await msg.edit_text("🔍 Menganalisa dengan AI...")
        extracted = extract_data_from_image(str(image_path))

        await msg.edit_text("📊 Menyimpan ke Google Sheets...")
        from_user = update.message.from_user.first_name or "unknown"
        sheet_url = save_to_sheets(extracted, from_user)

        summary = format_summary(extracted)
        await msg.edit_text(
            summary + f"\n\n🔗 Lihat Google Sheets:\n{sheet_url}"
        )

    except Exception as e:
        logging.error(f"Error handle_document: {e}")
        await msg.edit_text("❌ Gagal memproses. Coba lagi dengan foto yang lebih jelas.")
    finally:
        import time
        time.sleep(0.3)
        if image_path and Path(image_path).exists():
            try:
                Path(image_path).unlink()
            except Exception:
                pass


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.Document.IMAGE, handle_document))

    print("🤖 Telegram Bot berjalan...")
    app.run_polling()


if __name__ == "__main__":
    main()