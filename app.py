'''
import openai
import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

    
app = Flask(__name__)

# 設定 OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# 設定 LINE BOT API
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))


@app.route('/')
def home():
    print("==> home")
    return "Hello, this is the webhook server!", 200  # ✅ 新增首頁路由，確保 Flask 正常運作

#@app.route("/", methods=["GET"])
#def home():
#    return "LINE Bot is running.", 200

# LINE Webhook 端點

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    print("Received webhook data:", data)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return jsonify({"Invalid signature"}), 400

    return jsonify({"message": "Webhook received"}), 200

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

if __name__ == '__main__':
    print("==> get in port")
    port = int(os.environ.get("PORT", 8080))  # ✅ Railway 預設 8080
    # app.run(host="0.0.0.0", port=port)
    app.run(host="0.0.0.0", port=port, debug=True)  # ✅ Flask 直接啟動，開啟 debug
'''

import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, this is the webhook server!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON received"}), 400
    print("Received webhook data:", data)
    return jsonify({"message": "Webhook received"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # ✅ Railway 預設 PORT=8080
    print(f"🚀 Running on port {port}")  # ✅ 確保在 Logs 中能看到這個輸出
    app.run(host="0.0.0.0", port=port, debug=True)
