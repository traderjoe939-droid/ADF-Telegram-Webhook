
from flask import Flask, request
import requests

app = Flask(__name__)

# TEMPORARY TEST VALUES
BOT_TOKEN = "8619654734:AAH9tTYpxEOZtTx37MnTsQlvqii4CB6HuFM"
CHAT_ID = "-5598919041"


@app.route("/", methods=["GET"])
def home():
    return "ADF Telegram Webhook is running."


@app.route("/adf", methods=["POST"])
def adf():
    data = request.json or {}

    text = f"""
ADF SIGNAL

Symbol: {data.get('symbol')}
Command: {data.get('command')}
Grade: {data.get('grade')}
Score: {data.get('score')}
Risk USD: {data.get('risk_usd')}
Entry Type: {data.get('entry_type')}
Timeframe: {data.get('timeframe')}
"""

    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

    return {
        "status": "ok",
        "telegram_response": response.json()
    }


if __name__ == "__main__":
    app.run()

