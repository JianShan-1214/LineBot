from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi('m0EVC71bOpkTZUtkSz8EcrCuvm8WTugiLjihIVsExLqsaPgHnnR5kzFpORMj27hQ4bNHaZM96xBKJe82Mv0cPgMbtu2XC9f4mdKBGDOF/z60J56Ox7HVihWMC64Cr9vHpxC0d7SEYYswb1MBN80cAgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ddab94bc0b9106ec728b01ebb44b99d3')


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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0', port=8080)

