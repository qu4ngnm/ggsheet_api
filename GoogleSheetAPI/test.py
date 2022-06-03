from oauth2client.service_account import ServiceAccountCredentials
import gspread
from googleapiclient.discovery import build
from google.oauth2 import service_account

# SERVICE_ACCOUNT_FILE = 'key.json'
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# SPREADSHEET_ID = '1eJU4xJgSyHyC2WDGsaVT8J6Mv4nn7fd-OJIS-Tl2Dig'
# creds = None
# creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# service = build('sheets', 'v4', credentials = creds)
# sheet = service.spreadsheets()
#
#
# batch_clear_values_by_data_filter_request_body = [["quang3", "quang3@gmail.com"]]
# result = sheet.values().batchClearByDataFilter(spreadsheetId=SPREADSHEET_ID, body=batch_clear_values_by_data_filter_request_body)
# # result_list = result.get('values', [])

gc = gspread.service_account(filename='key.json')
sh = gc.open_by_key('1eJU4xJgSyHyC2WDGsaVT8J6Mv4nn7fd-OJIS-Tl2Dig')
worksheet = sh.sheet1

# row_countz = worksheet.row_count
# data_to_insert = ["username2", "email3"]
# worksheet.insert_row(data_to_insert, row_countz)
cell = worksheet.find("quang3")
worksheet.delete_row(cell.row)