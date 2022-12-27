import json
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import dotenv_values

config = dotenv_values(".env")

# defining the scope of the application
scope_app = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive'] 

#credentials to the account
cred = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(config['GOOGLE_SHEET_PRIVATE_KEY']), scope_app) 

# authorize the clientsheet 
client = gspread.authorize(cred)

# get the sample of the Spreadsheet
sheet = client.open("LINE-RUB-LINE-JAI").worksheet("Logs")

# get all the records of the data
records = sheet.get_all_records()

records_df = pd.DataFrame.from_dict(records)

print(records_df)