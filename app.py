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

line_bot_api = LineBotApi('DP4SRDa6l4Xjq8tlW1Ap7WMt8eM7Fwc5b5dmmzc7jfkd+eHr8kW59ukeFDiOQOUSKtKsmnJQ4UYOvPftvKM3zs/jmrlCtfVnsV/Xq0Z1Tvg1BFq8ia1EfoYaXsX/IVzP0yYh0TU3RM2uSgfRne1hHAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('200291b4fdfb04f77855f73dbc5aba55')

app = Flask(__name__)


@app.route("/")
def say_hello():
    return "Hello"


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
    app.run()
