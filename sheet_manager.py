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
        if len_records == 0:
            match command:
                case "รับ":
                    no = 1
                    balance = price
                    diff = "+" + str(float(price))
                    row_data = [no, str(date_time), str(command), float(price), str(description), float(balance), str(diff)]
                    self.format_color(self.start_index, command)
                    self.sheet.insert_row(row_data, self.start_index)
                    return "บันทึกรายการที่ " + str(no) + " สำเร็จ"
                case "จ่าย":
                    return "จะต้องบันทึกรายการแรกของคุณด้วยคำสั่ง รับ เพื่อระบุเงินตั้งต้น"
        else:
            last_record = records[-1]
            no = len_records + 1
            index = self.start_index + len_records
            balance = float(last_record['ยอดคงเหลือ'])
            diff = "0"
            match command:
                case "รับ":
                    balance += float(price)
                    diff = "+" + str(float(price))
                case "จ่าย":
                    balance -= float(price)
                    diff = "-" + str(float(price))
            row_data = [no, str(date_time), str(command), float(price), str(description), float(balance), str(diff)]
            self.format_color(index, command)
            self.sheet.insert_row(row_data, index)
            return "บันทึกรายการที่ " + str(no) + " สำเร็จ"
        
    def format_color(self, index, command):
        text_center_cell_range = "A$:G$".replace("$", str(index))
        command_cell_range = "C$".replace("$", str(index))
        diff_cell_range = "G$".replace("$", str(index))
        self.sheet.format(text_center_cell_range, {"backgroundColor": {"red": 0.0, "green": 0.0, "blue": 0.0}, "horizontalAlignment": "CENTER", "textFormat": {"fontSize": 10, "foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}}})
        match command:
            case "รับ":
                self.sheet.format(command_cell_range, {"backgroundColor": {"red": 0.0, "green": 0.0, "blue": 0.0}, "textFormat": {"foregroundColor": {"red": 0.0, "green": 1.0, "blue": 0.0}}})
                self.sheet.format(diff_cell_range, {"backgroundColor": {"red": 0.0, "green": 0.0, "blue": 0.0}, "textFormat": {"foregroundColor": {"red": 0.0, "green": 1.0, "blue": 0.0}}})
            case "จ่าย":
                self.sheet.format(command_cell_range, {"backgroundColor": {"red": 0.0, "green": 0.0, "blue": 0.0}, "textFormat": {"foregroundColor": {"red": 1.0, "green": 0.0, "blue": 0.0}}})
                self.sheet.format(diff_cell_range, {"backgroundColor": {"red": 0.0, "green": 0.0, "blue": 0.0}, "textFormat": {"foregroundColor": {"red": 1.0, "green": 0.0, "blue": 0.0}}})
        
        
if __name__ == "__main__":
    sheet_mgr = SheetManager()
    sheet_mgr.connect()
    status = sheet_mgr.append_data("2022-12-28 01:10:27", "รับ", 6000.0, "เงินรายเดือน")
    print(status)
    status = sheet_mgr.append_data("2022-12-28 02:10:27", "จ่าย", 60.0, "กะเพราหมู")
    print(status)
    status = sheet_mgr.append_data("2022-12-28 03:10:27", "จ่าย", 103.75, "กุ้งแก้ว")
    print(status)
    status = sheet_mgr.append_data("2022-12-28 04:10:27", "รับ", 1000.0, "หวย")
    print(status)