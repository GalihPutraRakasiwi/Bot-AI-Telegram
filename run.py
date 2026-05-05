# ============================================
# run.py
# Jalankan semua sekaligus:
# - Telegram Bot
# - WhatsApp Bot (webhook server)
# - Ngrok tunnel otomatis
# ============================================

import subprocess
import threading
import time
import os
import requests
from dotenv import load_dotenv

load_dotenv()

FONNTE_TOKEN = os.getenv("FONNTE_TOKEN")


def run_telegram():
    """Jalankan Telegram bot di thread terpisah."""
    print("🤖 Memulai Telegram Bot...")
    subprocess.run(["python", "telegram_bot.py"])


def run_whatsapp():
    """Jalankan WhatsApp webhook server."""
    print("📱 Memulai WhatsApp Server di port 8000...")
    subprocess.run(["python", "whatsapp_bot.py"])


def run_ngrok_and_set_webhook():
    """
    Jalankan ngrok dan otomatis set webhook ke Fonnte.
    Tunggu dulu sampai server WA siap.
    """
    time.sleep(3)  # tunggu server WA start dulu

    from pyngrok import ngrok

    # Buka tunnel
    tunnel = ngrok.connect(8000)
    public_url = tunnel.public_url
    webhook_url = f"{public_url}/webhook"

    print(f"\n{'='*50}")
    print(f"🌐 Ngrok URL  : {public_url}")
    print(f"🔗 Webhook URL: {webhook_url}")
    print(f"{'='*50}\n")

    # Otomatis set webhook ke Fonnte
    if FONNTE_TOKEN:
        try:
            resp = requests.post(
                "https://api.fonnte.com/set-webhook",
                headers={"Authorization": FONNTE_TOKEN},
                data={"webhook": webhook_url}
            )
            if resp.status_code == 200:
                print("✅ Webhook WhatsApp berhasil diset otomatis!")
            else:
                print(f"⚠️  Set webhook manual di fonnte.com: {webhook_url}")
        except Exception:
            print(f"⚠️  Set webhook manual di fonnte.com: {webhook_url}")
    else:
        print(f"⚠️  Set webhook manual di fonnte.com: {webhook_url}")

    print("\n✅ Semua service berjalan! Tekan Ctrl+C untuk stop.\n")

    # Jaga ngrok tetap hidup
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        ngrok.kill()


if __name__ == "__main__":
    print("\n🚀 Memulai Bot Foto → Excel...\n")

    # Jalankan semua di thread terpisah
    threads = [
        threading.Thread(target=run_telegram, daemon=True),
        threading.Thread(target=run_whatsapp, daemon=True),
        threading.Thread(target=run_ngrok_and_set_webhook, daemon=True),
    ]

    for t in threads:
        t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Bot dihentikan.")