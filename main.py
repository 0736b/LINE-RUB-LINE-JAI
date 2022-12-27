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
    print(body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = ""
    reply_text = ""
    if event.message.type == "text":
        user_text = event.message.text
        user_text_splitted = user_text.split(" ")
        if len(user_text_splitted) == 3:
            command = user_text_splitted[0]
            price = round(float(user_text_splitted[1]),2)
            description = user_text_splitted[2]
            match command:
                case "รับ":
                    reply_text = "คุณได้รับเงินจำนวน " + str(price) + ' บาท จาก ' + description
                case "จ่าย":
                    reply_text = "คุณได้จ่ายเงินจำนวน " + str(price) + ' บาท ค่า ' + description
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
        else:
            reply_text = "ควรขึ้นต้นด้วยคำว่า รับ หรือ จ่าย เช่น รับ 3000 เงินรายเดือน หรือ จ่าย 50 ผัดกระเพรา"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))


if __name__ == "__main__":
    app.run()