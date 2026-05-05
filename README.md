# 📦 Installation Guide - Python Telegram Bot Project

## 🚀 Requirements

Pastikan sudah terinstall:

- Python 3.8+
- pip
- Git

---

## 📁 1. Clone Repository

```bash
git clone https://github.com/username/repo.git
cd repo
```

---

## 🐍 2. Setup Virtual Environment (venv)

### Buat venv

```bash
python -m venv venv
```

### Aktifkan venv

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

---

## 📦 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ 4. Setup Environment Variables

Copy file `.env.example` menjadi `.env`:

```bash
cp .env.example .env
```

Lalu isi `.env`:

```env
# Telegram Bot Token (dari BotFather)
TELEGRAM_BOT_TOKEN=your_token_here

# Groq API Key
GROQ_API_KEY=your_groq_api_key

# Google Spreadsheet ID
SPREADSHEET_ID=your_spreadsheet_id
```

---

## 🤖 5. Cara Mendapatkan Telegram Bot Token

1. Buka Telegram
2. Cari **@BotFather**
3. Jalankan perintah:

```
/start
/newbot
```

4. Ikuti instruksi → akan mendapatkan `TELEGRAM_BOT_TOKEN`

---

## 🧠 6. Cara Mendapatkan Groq API Key

1. Daftar/login ke Groq Console
2. Generate API Key
3. Masukkan ke `.env`

---

## 📊 7. Setup Google Spreadsheet & Credentials

### a. Buat Spreadsheet

- Buka Google Sheets
- Copy ID dari URL:

```
https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit
```

---

### b. Generate `credentials.json`

1. Buka Google Cloud Console
2. Buat Project baru (atau gunakan yang sudah ada)
3. Enable API:
   - Google Sheets API
   - Google Drive API

4. Masuk ke **Credentials**
5. Klik **Create Credentials → Service Account**
6. Buat Service Account
7. Masuk ke tab **Keys**
8. Klik **Add Key → Create new key → JSON**
9. Download file → rename menjadi:

```
credentials.json
```

10. Letakkan file di root project

---

### c. Share Spreadsheet

- Buka Google Sheet
- Klik **Share**
- Tambahkan email dari service account (ada di credentials.json)
- Berikan akses **Editor**

---

## ▶️ 8. Run Project

```bash
python telegram_bot.py
```

---

## 🔐 Security Notes

- Jangan commit:
  - `.env`
  - `credentials.json`

- Pastikan sudah ada di `.gitignore`

---

## ✅ Done!

Bot siap digunakan 🚀
