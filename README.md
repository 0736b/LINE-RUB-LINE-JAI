<p align="center">
  <img src="https://raw.githubusercontent.com/0736b/0736b/main/Previews/line-rub-line-jai-logo.png" width="100px"/>
  <br>
  <b>LINE-RUB-LINE-JAI (รายรับ-รายจ่าย)</b>
  <br>
  LINE Chatbot for recording my personal expenses and save to google sheet.
</p>

#### Using
Typing command to LINE chatbot
- `รับ {จำนวนเงิน} {คำอธิบาย}` for recording income.
- `จ่าย {จำนวนเงิน} {คำอธิบาย}` for recording expense.
<img src="https://raw.githubusercontent.com/0736b/0736b/main/Previews/line-rub-line-jai-user1.JPG" width="300px"/>

<img src="https://raw.githubusercontent.com/0736b/0736b/main/Previews/line-rub-line-jai-user2.JPG" width="800px"/>

#### Running on local
- install ngrok and run `ngrok http 5000`
- setup your LINE Developer for Messaging API.
- setup your Google Sheet and API on Google cloud console.
- `pip install requirements.txt`
- create `.env` file and put your key from LINE and Google like `.env.example`
- `python main.py`

#### Deploy on render.com
- new "Web Service" and paste this repo link.
- environment add variable key `PYTHON_VERSION` value `3.11.0`
- add secret file with filename `.env` and paste your content in `.env` file.
- build command: `pip install -r requirements.txt`
- start command: `gunicorn main:app`
