from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "8619654734:AAHE4qZzMnVknIJyQ5EJA4-rDj-IFwym1i8")
CHAT_ID = os.getenv("CHAT_ID", "-5598919041")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


@app.route("/", methods=["GET"])
def home():
    return "ADF Telegram Webhook is running."


def clean(value):
    if value is None or value == "":
        return "N/A"
    return str(value)


def build_message(data):
    event = clean(data.get("event", "ENTRY"))

    if event == "ENTRY":
        title = "ADF ENTRY SIGNAL"
    elif event == "TP1_HIT":
        title = "ADF TP1 HIT"
    elif event == "TP2_HIT":
        title = "ADF TP2 HIT"
    elif event == "SL_HIT":
        title = "ADF STOP LOSS HIT"
    else:
        title = "ADF SIGNAL"

    text = f"""
{title}

Event: {event}
Version: {clean(data.get('version'))}
Symbol: {clean(data.get('symbol'))}
Command: {clean(data.get('command'))}
Grade: {clean(data.get('grade'))}
Score: {clean(data.get('score'))}

Entry: {clean(data.get('entry'))}
SL: {clean(data.get('sl'))}
TP1: {clean(data.get('tp1'))}
TP2: {clean(data.get('tp2'))}

Hit Price: {clean(data.get('hit_price'))}

Risk USD: {clean(data.get('risk_usd'))}
Lot Size: {clean(data.get('lot_size'))}
SL Buffer: {clean(data.get('sl_buffer'))}

Target R: {clean(data.get('target_r'))}
Exit Model: {clean(data.get('exit_model'))}
Entry ID: {clean(data.get('entry_id'))}

Weak Hour Filter: {clean(data.get('weak_hour_filter'))}
Blocked Hours: {clean(data.get('blocked_hours'))}

Timeframe: {clean(data.get('timeframe'))}
"""
    return text.strip()


@app.route("/adf", methods=["POST"])
def adf():
    try:
        data = request.get_json(silent=True) or {}

        if not BOT_TOKEN:
            return jsonify({
                "status": "error",
                "message": "BOT_TOKEN is missing from Render environment variables."
            }), 500

        if not CHAT_ID:
            return jsonify({
                "status": "error",
                "message": "CHAT_ID is missing from Render environment variables."
            }), 500

        text = build_message(data)

        response = requests.post(
            TELEGRAM_API_URL,
            json={
                "chat_id": CHAT_ID,
                "text": text
            },
            timeout=10
        )

        telegram_json = response.json()

        return jsonify({
            "status": "ok",
            "received": data,
            "telegram_response": telegram_json
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
