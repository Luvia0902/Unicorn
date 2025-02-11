from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import config
import os
import logging

app = Flask(__name__)

# 設定 OpenAI API Key
openai.api_key = config.OPENAI_API_KEY

# 設定 LINE BOT API
line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)

logging.warning(openai.api_key)
logging.warning(line_bot_api)
logging.warning(handler)

@app.route("/", methods=["GET"])
def home():
    return "LINE Bot is running."

# LINE Webhook 端點
@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return "Invalid signature", 400

    return "OK"

# 文字訊息處理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    # 發送到 OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_message}]
    )

    reply_text = response["choices"][0]["message"]["content"].strip()

    # 回覆使用者
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # 預設 5000
    app.run(host="0.0.0.0", port=port)
    
    logging.warning(port)
