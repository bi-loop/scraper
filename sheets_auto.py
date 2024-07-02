import os
import pickle
import pandas as pd
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
spreadsheet_id = '1FGPoxaLRCPR7toyPjNaHvKdZfUl-rohbiDCEgWADnqA'
excel_file_path = 'data.xlsx'

def get_credentials():
    """Authenticate and return credentials."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'token.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def fetch_all_data():
    """Fetch all data from a Google Sheet and return it as a DataFrame."""
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    result = sheet.values().get(spreadsheetId=spreadsheet_id, range='QC_data').execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
        return pd.DataFrame()

    # Assuming the first row contains column headers
    headers = values[0]
    data = values[1:]

    # Ensure all rows have the same number of columns as the headers
    for i in range(len(data)):
        if len(data[i]) < len(headers):
            data[i].extend([None] * (len(headers) - len(data[i])))

    df = pd.DataFrame(data, columns=headers)

    return df

def update_sheet_with_dataframe(df):
    """Update the Google Sheet with the contents of the DataFrame."""
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # Convert DataFrame to list of lists
    values = [df.columns.tolist()] + df.values.tolist()

    # Clear existing data
    sheet.values().clear(spreadsheetId=spreadsheet_id, range='QC_data').execute()

    # Update the sheet with the new data
    body = {
        'values': values
    }
    result = sheet.values().update(
        spreadsheetId=spreadsheet_id,
        range='QC_data',
        valueInputOption="RAW",
        body=body
    ).execute()

    print(f"Updated sheet with new data: {result.get('updatedCells')} cells updated.")


