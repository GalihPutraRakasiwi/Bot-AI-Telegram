import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

sheets = client.openall()
spreadsheet = sheets[0]
print(f"✅ Berhasil! Nama: {spreadsheet.title}, ID: {spreadsheet.id}")

# Coba tulis data test
ws = spreadsheet.sheet1
ws.append_row(["test", "berhasil", "123"])
print("✅ Tulis data berhasil!")