from flask import Flask, request, abort
import requests


from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

line_bot_api = LineBotApi('')
handler = WebhookHandler('')

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
  
  # 挨拶
  if event.message.text == "おはよう":
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="おはっピ！"))
    
    
  if event.message.text == "こんにちは":
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="こんにちはっピ！"))
    
    
  if event.message.text == "こんばんは":
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="こんばんはっピ！"))
    
  
  if event.message.text == "おやすみ":
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="おやすみっピ！"))
    
  
  # いじめる
  if event.message.text == "タコピー":
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="どうしたっピか？"))
    
    
  if event.message.text == "クソピー":
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="ピピピピピピピピピピピ(泣)"))
    
    
  if event.message.text == "シネピー":
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="ピピピピピピピピピピピ(泣)"*64))
    
  
  # 天気
  if event.message.text == "天気":
    params = {"q": "Tokyo", "appid": "706a6848e95d332c4d575e7d8d2ac78e"}
    url = "http://api.openweathermap.org/data/2.5/forecast"
    res = requests.get(url, params=params)
    jsonText = res.json()

    # ケルビンから摂氏に変換
    data = jsonText["list"][1]["main"]["temp"] - 273.15
    data = data * 1
    data = str(data)

    do = "気温: " + data[0:4] + "℃"
    whether = "天気: " + jsonText["list"][1]["weather"][0]["main"]
    wind = "風速: " + str(jsonText["list"][1]["wind"]["speed"])
    date = "日時: " + jsonText["list"][1]["dt_txt"]

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="天気情報っピ！"+"\n"+do+"\n"+whether+"\n"+wind+"\n"+date)
    
    )

    
  # スプラの情報
  if event.message.text == "今のステージ":
    nawa_url = "https://spla2.yuu26.com/regular/now"
    nawa_res = requests.get(nawa_url)
    nawa_json = nawa_res.json()
    nawa1 = nawa_json["result"][0]["maps"][0]
    nawa2 = nawa_json["result"][0]["maps"][1]
    
    gachi_url = "https://spla2.yuu26.com/gachi/now"
    gachi_res = requests.get(gachi_url)
    gachi_json = gachi_res.json()
    gachi1 = gachi_json["result"][0]["maps"][0]
    gachi2 = gachi_json["result"][0]["maps"][1]
    
    league_url = "https://spla2.yuu26.com/league/now"
    league_res = requests.get(league_url)
    league_json = league_res.json()
    league1 = league_json["result"][0]["maps"][0]
    league2 = league_json["result"][0]["maps"][1]
    
    line_bot_api.reply_message(
      event.reply_token,
      TextSendMessage(text="今のステージ情報っピ！"+"\n\n"+
                            "レギュラーマッチ"+"\n"+
                            "・"+nawa1+"\n"+
                            "・"+nawa2+"\n\n"+
                            "ガチマッチ"+"\n"+
                            "・"+gachi1+"\n"+
                            "・"+gachi2+"\n\n"+
                            "リーグマッチ"+"\n"+
                            "・"+league1+"\n"+
                            "・"+league2
                     )
    )
    
    
  if event.message.text == "次のステージ":
    nawa_url = "https://spla2.yuu26.com/regular/next"
    nawa_res = requests.get(nawa_url)
    nawa_json = nawa_res.json()
    nawa1 = nawa_json["result"][0]["maps"][0]
    nawa2 = nawa_json["result"][0]["maps"][1]
    
    gachi_url = "https://spla2.yuu26.com/gachi/next"
    gachi_res = requests.get(gachi_url)
    gachi_json = gachi_res.json()
    gachi1 = gachi_json["result"][0]["maps"][0]
    gachi2 = gachi_json["result"][0]["maps"][1]
    
    league_url = "https://spla2.yuu26.com/league/next"
    league_res = requests.get(league_url)
    league_json = league_res.json()
    league1 = league_json["result"][0]["maps"][0]
    league2 = league_json["result"][0]["maps"][1]
    
    line_bot_api.reply_message(
      event.reply_token,
      TextSendMessage(text="次のステージ情報っピ！"+"\n\n"+
                            "レギュラーマッチ"+"\n"+
                            "・"+nawa1+"\n"+
                            "・"+nawa2+"\n\n"+
                            "ガチマッチ"+"\n"+
                            "・"+gachi1+"\n"+
                            "・"+gachi2+"\n\n"+
                            "リーグマッチ"+"\n"+
                            "・"+league1+"\n"+
                            "・"+league2
                     )
    )
    
    
if __name__ == "__main__":
    app.run()
