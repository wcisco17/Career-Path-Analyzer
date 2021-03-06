import csv
import json
import re
from google.oauth2 import service_account
from googleapiclient.discovery import build

from keys import SERVICE_ACCOUNT_FILE, SPREADSHEET_ID
from structure import generate_col, merge_structures

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = service_account.Credentials.from_service_account_info(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)


def sheet_init():
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    return sheet


def create_sheet(j, source):
    sheet = sheet_init()
    item = json.dumps(merge_structures(source))
    append_sheet2 = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        valueInputOption="USER_ENTERED", body={"values": [[item]]}, range=f"{'sales'}!A{j + 1}").execute()
    return append_sheet2


def save_excel_db():
    sheet = sheet_init()

    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="all-update"
    ).execute()

    col = generate_col(14)

    with open('../excel-data/f-linkedin-profile.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=col)
        writer.writeheader()
        for value in (result['values']):
            db = json.loads(value[0])
            writer.writerow(db)


if __name__ == '__main__':
    save_excel_db()
