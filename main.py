from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from dotenv import dotenv_values
from datetime import datetime
from sheet_manager import SheetManager


config = dotenv_values(".env")

app = Flask(__name__)

line_bot_api = LineBotApi(config['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(config['CHANNEL_SECRET'])


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    date_time = str(datetime.fromtimestamp(round(event.timestamp / 1000)))
    date = date_time.split(" ")[0]
    time = date_time.split(" ")[1]
    if event.message.type == "text":
        reply_text = "คำสั่งขึ้นต้นด้วยคำว่า รับ หรือ จ่าย เช่น\nรับ 3000 เงินรายเดือน\nหรือ\nจ่าย 50 ผัดกระเพรา"
        user_text = event.message.text
        user_text_splitted = user_text.split(" ")
        if len(user_text_splitted) == 3:
            try:
                float(user_text_splitted[1])
            except:
                error_msg = "คำสั่ง หรือ จำนวนเงินไม่ถูกต้อง โปรดพิมพ์ใหม่"
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=error_msg))
            command = user_text_splitted[0]
            price = round(float(user_text_splitted[1]),2)
            description = user_text_splitted[2]
            match command:
                case "รับ":
                    reply_text = "เมื่อ " + date + " เวลา " + time + "\nคุณได้รับเงินจำนวน " + str(price) + ' บาท\nจาก ' + description
                    sheet_mgr = SheetManager()
                    sheet_mgr.connect()
                    status = sheet_mgr.append_data(date_time, command, price, description)
                    reply_text += "\n" + status
                case "จ่าย":
                    reply_text = "เมื่อ " + date + " เวลา " + time + "\nคุณได้จ่ายเงินจำนวน " + str(price) + ' บาท\nค่า ' + description
                    sheet_mgr = SheetManager()
                    sheet_mgr.connect()
                    status = sheet_mgr.append_data(date_time, command, price, description)
                    reply_text += "\n" + status
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))


if __name__ == "__main__":
    app.run()