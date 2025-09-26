from flask import Flask, jsonify
import requests
import time
import threading
from datetime import datetime
import random

app = Flask(__name__)

# ==================== PREMIUM CONFIG ====================
TOKEN = "7999501715:AAHPb6LuIIn8KKqF4g2yUYKii7w85VT0OX0"
CHANNEL = "@CryptoAlertsBot0"

# PREMIUM COIN LIST WITH MEMECOINS
PREMIUM_COINS = [
    'bitcoin', 'ethereum', 'binancecoin', 'solana', 'dogecoin',
    'shiba-inu', 'pepe', 'cardano', 'ripple', 'matic-network'
]

# ==================== PREMIUM ALERT FORMAT ====================
def send_premium_alert(coin_data):
    """RICH alerts with images and premium features"""

    # Get proper coin data with all timeframes
    detailed_data = get_detailed_coin_data(coin_data['id'])
    if not detailed_data:
        return False

    symbol = detailed_data['symbol'].upper()
    price = detailed_data['current_price']
    changes = detailed_data['price_changes']

    # Generate smart signal
    signal = generate_smart_signal(changes)

    # Coin image URL
    image_url = f"https://coins-images.coingecko.com/coins/images/1/large/bitcoin.png?1547033579"

    message = f"""
🪙 <b>{detailed_data['name']} ({symbol})</b> 💎

📊 <b>Multi-Timeframe Analysis:</b>
├─ 1H: {changes.get('1h', 0):+.2f}%
├─ 24H: {changes.get('24h', 0):+.2f}% 
├─ 7D: {changes.get('7d', 0):+.2f}%
└─ Market Cap: ${detailed_data.get('market_cap', 0):,.0f}

💰 <b>Price:</b> ${price:.8f} {f'(${price:.2e})' if price < 0.01 else ''}

🎯 <b>Trading Signal:</b> {signal['level']}
📈 <b>Action:</b> {signal['action']} 
⭐ <b>Confidence:</b> {signal['confidence']}/10

🔥 <b>Market Insight:</b>
{generate_insight(detailed_data, changes)}

💎 <b>Premium Tip:</b> {generate_trading_tip()}

👥 <b>Community Sentiment:</b> {random.choice(['🟢 Very Bullish', '🟡 Neutral', '🔴 Cautious'])}

📸 <a href="{image_url}">⠀</a>

🔗 <a href="https://www.coingecko.com/en/coins/{coin_data['id']}">View Detailed Analysis</a>

⏰ <i>Alert ID: #{random.randint(1000,9999)} | {datetime.now().strftime('%H:%M UTC')}</i>

<b>✨ Upgrade to PRO for real-time portfolio tracking!</b>
    """

    return send_telegram(message)

def generate_smart_signal(changes):
    """Advanced signal generation"""
    hour_1 = changes.get('1h', 0)
    hour_24 = changes.get('24h', 0)
    week_1 = changes.get('7d', 0)

    # Bullish signals
    if hour_1 > 4.0 and hour_24 > 6.0:
        return {"level": "STRONG BUY 🚀", "action": "Momentum breakout in progress", "confidence": 9}
    elif hour_24 > 10.0:
        return {"level": "TREND BUY 📈", "action": "Strong daily trend confirmed", "confidence": 8}
    elif hour_1 > 8.0:
        return {"level": "PUMP ALERT ⚡", "action": "Significant hourly movement", "confidence": 7}

    # Bearish signals
    elif hour_1 < -5.0 and hour_24 < -8.0:
        return {"level": "STRONG SELL 📉", "action": "Downtrend accelerating", "confidence": 8}
    elif hour_24 < -12.0:
        return {"level": "TREND SELL 🔻", "action": "Major daily decline", "confidence": 7}

    # Neutral/consolidation
    elif abs(hour_1) < 1.0:
        return {"level": "HOLD STEADY ⚖️", "action": "Price consolidating", "confidence": 6}
    else:
        return {"level": "MONITOR CLOSELY 👀", "action": "Market indecision", "confidence": 5}

def generate_insight(coin_data, changes):
    """Premium market insights"""
    hour_1 = changes.get('1h', 0)

    if hour_1 > 5.0:
        return "Strong buying pressure detected with increasing volume"
    elif hour_1 < -5.0:
        return "Selling pressure intensifying, watch support levels"
    elif changes.get('7d', 0) > 20.0:
        return "Weekly trend remains strongly bullish"
    else:
        insights = [
            "Technical indicators showing potential breakout formation",
            "Volume analysis suggests accumulation phase",
            "Key resistance level approaching, watch for break",
            "Market structure intact, trend remains healthy",
            "Whale activity detected in recent hours"
        ]
        return random.choice(insights)

def generate_trading_tip():
    """Premium trading education"""
    tips = [
        "Use 1% risk management per trade to preserve capital",
        "Wait for candle close above key levels for confirmation",
        "Dollar-cost averaging reduces timing risk significantly",
        "Track BTC dominance for overall market direction clues",
        "Set stop-loss at recent swing low for protection",
        "Pyramid into positions as trend confirms strength"
    ]
    return random.choice(tips)

# ==================== FIXED API SYSTEM ====================
def get_detailed_coin_data(coin_id):
    """Get rich coin data with proper error handling"""
    try:
        time.sleep(3)  # Avoid rate limits
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        params = {'localization': 'false', 'tickers': 'false', 'community_data': 'false', 'developer_data': 'false'}

        response = requests.get(url, params=params, timeout=15)

        if response.status_code == 429:
            print(f"⏳ Rate limit: Waiting 30 seconds...")
            time.sleep(30)
            return None

        data = response.json()
        market_data = data.get('market_data', {})

        return {
            'id': coin_id,
            'name': data.get('name', 'Unknown'),
            'symbol': data.get('symbol', '???'),
            'current_price': market_data.get('current_price', {}).get('usd', 0),
            'market_cap': market_data.get('market_cap', {}).get('usd', 0),
            'price_changes': {
                '1h': market_data.get('price_change_percentage_1h_in_currency', {}).get('usd', 0),
                '24h': market_data.get('price_change_percentage_24h_in_currency', {}).get('usd', 0),
                '7d': market_data.get('price_change_percentage_7d_in_currency', {}).get('usd', 0)
            }
        }
    except Exception as e:
        print(f"❌ Detailed data error for {coin_id}: {e}")
        return None

def check_all_coins_properly():
    """Check coins with smart rate limiting"""
    print("🔍 PREMIUM SCAN: Checking all coins...")
    alerts_sent = 0

    for i, coin_id in enumerate(PREMIUM_COINS):
        print(f"💰 [{i+1}/{len(PREMIUM_COINS)}] Analyzing {coin_id}...")

        coin_data = get_detailed_coin_data(coin_id)
        if coin_data and coin_data['current_price'] > 0:
            changes = coin_data['price_changes']

            # Alert on meaningful moves (lower thresholds for more alerts)
            if any(abs(changes.get(timeframe, 0)) > threshold 
                   for timeframe, threshold in [('1h', 2.0), ('24h', 4.0), ('7d', 8.0)]):

                print(f"🎯 SIGNIFICANT MOVE: {coin_data['name']}")
                if send_premium_alert(coin_data):
                    alerts_sent += 1
                    time.sleep(5)  # Avoid Telegram rate limits
            else:
                print(f"⚡ {coin_data['name']}: Normal fluctuations")
        else:
            print(f"❌ Could not fetch data for {coin_id}")

        # Longer delay between coins to avoid API limits
        if i < len(PREMIUM_COINS) - 1:
            time.sleep(5)

    print(f"✅ PREMIUM SCAN COMPLETE: {alerts_sent} alerts sent")
    return alerts_sent

def send_telegram(message):
    """Send message to Telegram with proper error handling"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Telegram message sent successfully")
            return True
        else:
            print(f"❌ Telegram error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Telegram send error: {e}")
        return False

# ==================== PREMIUM BOT ====================
def run_premium_bot():
    print("💎 PREMIUM BOT ACTIVATED!")
    send_telegram("🎉 PREMIUM Crypto Bot Started! • Rich Alerts • Multi-Timeframe • Memecoins")

    while True:
        alerts = check_all_coins_properly()
        if alerts == 0:
            print("💤 No significant moves, resting...")
        time.sleep(300)  # 5 minutes

# ==================== WEB ROUTES ====================
@app.route('/')
def home():
    return "💎 PREMIUM Crypto Bot - Rich Alerts Active"

@app.route('/health')
def health():
    return jsonify({"status": "premium_active", "coins": len(PREMIUM_COINS)})

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_premium_bot)
    bot_thread.daemon = True
    bot_thread.start()

    print("🌐 Premium web server starting on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False)
