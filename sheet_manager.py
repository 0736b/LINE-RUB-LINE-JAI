import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import dotenv_values


config = dotenv_values(".env")


class SheetManager:
    
    def __init__(self):
        self.scope_app = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive'] 
        self.cred = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(config['GOOGLE_SHEET_PRIVATE_KEY']), self.scope_app)
        self.start_index = 2
        
    def connect(self):
        self.client = gspread.authorize(self.cred)
        self.sheet = self.client.open("LINE-RUB-LINE-JAI").worksheet("Logs")
        
    def get_records_data(self):
        records = self.sheet.get_all_records()
        print('records len:', len(records))
        print(records)
        
    def append_data(self, date_time, command, price, description):
        records = self.sheet.get_all_records()
        len_records = len(records)
        if len(records) == 0:
            match command:
                case "รับ":
                    no = 1
                    balance = price
                    row_data = [no, str(date_time), str(command), float(price), str(description), float(balance)]
                    self.sheet.insert_row(row_data, self.start_index)
                    return "บันทึกรายการที่ " + str(no) + "สำเร็จ"
                case "จ่าย":
                    return "จะต้องบันทึกรายการแรกของคุณด้วยคำสั่ง รับ เพื่อระบุเงินตั้งต้น"
        else:
            last_record = records[-1]
            no = len_records + 1
            index = self.start_index + len_records
            balance = float(last_record['ยอดคงเหลือ'])
            match command:
                case "รับ":
                    balance += float(price)
                case "จ่าย":
                    balance -= float(price)
            row_data = [no, str(date_time), str(command), float(price), str(description), float(balance)]
            self.sheet.insert_row(row_data, index)
            return "บันทึกรายการที่ " + str(no) + "สำเร็จ"

if __name__ == "__main__":
    sheet_mgr = SheetManager()
    sheet_mgr.connect()
    status = sheet_mgr.append_data("2022-12-28 02:10:27", "จ่าย", 9000.0, "เงินรายเดือน")
    print(status)