from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Better: store these in Render Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN", "8619654734:AAHE4qZzMnVknIJyQ5EJA4-rDj-IFwym1i8")
CHAT_ID = os.getenv("CHAT_ID", "-5598919041")


@app.route("/", methods=["GET"])
def home():
    return "ADF Telegram Webhook is running."


@app.route("/adf", methods=["POST"])
def adf():
    data = request.json or {}

    text = f"""
ADF SIGNAL

Version: {data.get('version', 'N/A')}
Symbol: {data.get('symbol', 'N/A')}
Command: {data.get('command', 'N/A')}
Grade: {data.get('grade', 'N/A')}
Score: {data.get('score', 'N/A')}

Entry: {data.get('entry', 'N/A')}
SL: {data.get('sl', 'N/A')}
TP1: {data.get('tp1', 'N/A')}
TP2: {data.get('tp2', 'N/A')}

Risk USD: {data.get('risk_usd', 'N/A')}
Lot Size: {data.get('lot_size', 'N/A')}
SL Buffer: {data.get('sl_buffer', 'N/A')}

Exit Model: {data.get('exit_model', 'N/A')}
Timeframe: {data.get('timeframe', 'N/A')}
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
        "received": data,
        "telegram_response": response.json()
    }


if __name__ == "__main__":
    app.run()
