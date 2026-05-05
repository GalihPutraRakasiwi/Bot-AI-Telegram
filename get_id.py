# fix_env.py
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

sheets = client.openall()
if sheets:
    correct_id = sheets[0].id
    print(f"ID yang benar: [{correct_id}]")
    
    # Baca .env
    with open(".env", "r") as f:
        content = f.read()
    
    # Ganti baris SPREADSHEET_ID
    import re
    new_content = re.sub(
        r"SPREADSHEET_ID=.*",
        f"SPREADSHEET_ID={correct_id}",
        content
    )
    
    # Tulis balik
    with open(".env", "w") as f:
        f.write(new_content)
    
    print("✅ .env sudah diupdate otomatis!")
    print(f"Cek: https://docs.google.com/spreadsheets/d/{correct_id}")