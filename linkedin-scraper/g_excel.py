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

# {'Industry': 'Finance', 'Headline': 'Partner at Forsyth Street Advisors', 'College-Name-1': 'Cornell University', 'Degree-Name-1': 'Bachelor of Science (BS), Resource Economics', 'Field-Of-Study-1': 'Bachelor of Science (BS), Resource Economics', 'Activities-and-Societies-1': '', 'Activities-and-Societies--1': '', 'Job-Title-1': '', 'Company-Name-1': '', 'Dates-Employed-1': '', 'Employment-Duration-1': '', 'Location-1': '', 'Job-Title-2': 'Associate/Assistant Commissioner', 'Company-Name-2': 'NYC HPD', 'Dates-Employed-2': '2002 - 2005', 'Employment-Duration-2': '3 yrs', 'Location-2': '', 'skills': ''}
# {'Industry': 'Business', 'Headline': 'Highly Experienced Operations Leader', 'College-Name-1': '', 'Degree-Name-1': '', 'Field-Of-Study-1': '', 'Activities-and-Societies-1': '', 'Activities-and-Societies--1': '', 'Job-Title-1': 'General Manager', 'Company-Name-1': 'Patriot Ventures, Inc. · Self-employed', 'Dates-Employed-1': '2015 - Present', 'Employment-Duration-1': '7 yrs 4 mos', 'Location-1': 'Sudbury, Massachusetts, United States', 'Job-Title-2': 'Chief Operating Officer', 'Company-Name-2': 'Cambrian Innovation, Inc. · Full-time', 'Dates-Employed-2': '2014 - 2015', 'Employment-Duration-2': '1 yr', 'Location-2': 'Boston, MA', 'Job-Title-3': 'Sr. Vice President, Manufacturing Operations', 'Company-Name-3': 'Columbia Tech', 'Dates-Employed-3': '2010 - 2013', 'Employment-Duration-3': '3 yrs', 'Location-3': 'Worcester, MA', 'skills': 'Manufacturing,Supply Chain Management,Cross-functional Team Leadership,'}