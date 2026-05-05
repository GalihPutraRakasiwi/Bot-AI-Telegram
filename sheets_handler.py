# ============================================
# sheets_handler.py
# Simpan data langsung ke Google Sheets
# ============================================

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_sheet():
    """Koneksi ke Google Sheets."""
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    client = gspread.authorize(creds)
    
    # Gunakan openall() lalu filter by title, hindari open_by_key
    sheets = client.openall()
    if not sheets:
        raise Exception("Tidak ada sheet yang bisa diakses")
    
    # Ambil sheet pertama (sheet-bot)
    return sheets[0]


def flatten_dict(d: dict, parent_key: str = "") -> dict:
    """Ratakan nested dict menjadi flat. {'a': {'b': 1}} -> {'a_b': 1}"""
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}_{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key))
        else:
            items[new_key] = v
    return items


def save_to_sheets(extracted: dict, from_user: str = "") -> str:
    spreadsheet = get_sheet()
    spreadsheet_id = spreadsheet.id  # ambil ID dari object
    
    tipe = extracted.get("tipe_dokumen", "lainnya").strip().lower()
    sheet_name = tipe[:30]

    try:
        ws = spreadsheet.worksheet(sheet_name)
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=20)

    data_rows = extracted.get("data", [])
    if not data_rows:
        data_rows = [{}]

    flat_rows = []
    for row in data_rows:
        flat = flatten_dict(row) if isinstance(row, dict) else {"nilai": row}
        flat["_tanggal_dokumen"] = extracted.get("tanggal", "")
        flat["_total"] = extracted.get("total", "")
        flat["_dari_user"] = from_user
        flat["_waktu_input"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        flat_rows.append(flat)

    existing_data = ws.get_all_values()

    if not existing_data:
        all_keys = list(flat_rows[0].keys())
        ws.append_row(all_keys, value_input_option="RAW")
    else:
        all_keys = existing_data[0]
        new_keys = [k for k in flat_rows[0].keys() if k not in all_keys]
        if new_keys:
            all_keys.extend(new_keys)
            ws.update("1:1", [all_keys])

    for flat in flat_rows:
        row_values = [str(flat.get(k, "")) for k in all_keys]
        ws.append_row(row_values, value_input_option="RAW")

    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"