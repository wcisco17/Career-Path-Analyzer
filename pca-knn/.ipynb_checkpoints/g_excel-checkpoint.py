import csv
import json

from google.oauth2 import service_account
from googleapiclient.discovery import build

from structure import generate_col, merge_structures

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'

creds = None
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID Spreadsheet
SPREADSHEET_ID = '1n3h1nrJdmUGz80mkU6HOslwhGqEkghL2qnKsNTghP8E'


def sheet_init():
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    return sheet


def create_sheet(j, source):
    sheet = sheet_init()
    item = json.dumps(merge_structures(source))
    append_sheet2 = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        valueInputOption="USER_ENTERED", body={"values": [[item]]}, range=f"finance2!A{j + 1}").execute()
    return append_sheet2


def save_excel_db():
    sheet = sheet_init()

    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="all-update"
    ).execute()

    col = generate_col(7)

    with open('excel-data/1_update-linkedin.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=col)
        writer.writeheader()
        for value in (result['values']):
            db = json.loads(value[0])
            writer.writerow(db)


save_excel_db()
