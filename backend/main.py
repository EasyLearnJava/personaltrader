from massive import WebSocketClient
from massive.websocket.models import WebSocketMessage, Feed, Market
from typing import List
import datetime
import os
import time
import pytz
import requests
import threading
import json
from collections import deque
from flask import Flask, jsonify
from flask_cors import CORS

# Configuration
POLYGON_API_KEY = os.getenv('POLYGON_API_KEY', 'wsWMG2p9vhDDjVxAHSRz6qbSR_a7B1wL')

# Global variables for dynamic strike management
current_strike = None
last_strike = None
live_ndx_price = None
next_refresh_time = None
reconnect_flag = False
websocket_running = False

# In-memory data storage (keep last 1000 records)
options_data = deque(maxlen=1000)
data_lock = threading.Lock()

# Flask app for API
flask_app = Flask(__name__)
CORS(flask_app)  # Enable CORS for frontend access

@flask_app.route('/api/options', methods=['GET'])
def get_options_data():
    """API endpoint to get options data"""
    with data_lock:
        data_list = list(options_data)
    return jsonify({
        'data': data_list,
        'count': len(data_list),
        'last_update': datetime.datetime.now().isoformat()
    })

@flask_app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    # Calculate seconds until next refresh
    seconds_until_refresh = None
    if next_refresh_time:
        time_diff = next_refresh_time - datetime.datetime.now()
        seconds_until_refresh = max(0, int(time_diff.total_seconds()))

    return jsonify({
        'status': 'ok',
        'websocket_running': websocket_running,
        'data_count': len(options_data),
        'current_strike': current_strike,
        'live_ndx_price': live_ndx_price,
        'next_refresh_seconds': seconds_until_refresh
    })

def start_flask_server():
    """Start Flask server in a separate thread"""
    flask_app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# WebSocket client (will be initialized dynamically)
client = None

# Debug counters
message_count = 0
last_message_time = None

def store_data(data_dict):
    """Store data in memory"""
    with data_lock:
        options_data.append(data_dict)
    return True

def get_current_ndx_price():
    """
    Fetch REAL-TIME NDX index price from Polygon.io
    Returns both the actual price and the price rounded to nearest 10 (strike interval)
    """
    try:
        # Use snapshot endpoint for real-time data
        url = f"https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers/I:NDX?apiKey={POLYGON_API_KEY}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if 'ticker' in data and 'lastTrade' in data['ticker']:
                price = data['ticker']['lastTrade']['p']  # Real-time last trade price
                strike = round(price / 10) * 10  # Round to nearest 10
                print(f"✅ Fetched REAL-TIME NDX price: ${price:,.2f} → Strike: ${int(strike):,}")
                return int(strike), price
        else:
            print(f"⚠️ Polygon API returned status {response.status_code}")
    except Exception as e:
        print(f"⚠️ Error fetching NDX price: {e}")

    # Fallback to default
    default_strike = 25650
    default_price = 25650.0
    print(f"⚠️ Using fallback strike: ${default_strike:,}")
    return default_strike, default_price

def check_strike_and_reconnect():
    """
    Background thread that checks NDX price every 10 minutes
    ALWAYS triggers reconnection to use latest strike price
    """
    global current_strike, last_strike, live_ndx_price, next_refresh_time, reconnect_flag, websocket_running

    while websocket_running:
        # Set next refresh time (10 minutes from now)
        next_refresh_time = datetime.datetime.now() + datetime.timedelta(minutes=10)

        # Wait 10 minutes (600 seconds)
        for i in range(600):
            if not websocket_running:
                break
            time.sleep(1)  # Sleep 1 second at a time to allow clean shutdown

        if not websocket_running:
            break

        new_strike, new_price = get_current_ndx_price()
        strike_change = abs(new_strike - current_strike)

        print(f"\n🔍 10-Minute Strike Check:")
        print(f"   Current Strike: ${current_strike:,}")
        print(f"   New Strike: ${new_strike:,}")
        print(f"   Live NDX Price: ${new_price:,.2f}")
        print(f"   Change: ${strike_change:,}")

        # ALWAYS reconnect every 10 minutes with latest strike
        print(f"🔄 10-minute interval reached - Triggering reconnection with latest strike...")
        current_strike = new_strike
        live_ndx_price = new_price
        reconnect_flag = True
        else:
            print(f"✅ Strike change ≤100 points. Continuing current connection.")

def initialize_websocket_client():
    """Initialize or reinitialize the WebSocket client"""
    global client

    print("🔗 Initializing WebSocket connection...")
    client = WebSocketClient(
        api_key=POLYGON_API_KEY,
        feed=Feed.RealTime,  # Real-time data feed
        market=Market.Options
    )
    return client

def handle_msg(msgs: List[WebSocketMessage]):
    global message_count, last_message_time

    message_count += len(msgs)
    last_message_time = datetime.datetime.now()

    if message_count % 10 == 0:
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"💓 [{timestamp}] Heartbeat: Received {message_count} messages so far...")

    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    for m in msgs:
        if hasattr(m, 'symbol') and hasattr(m, 'volume') and hasattr(m, 'close'):
            symbol = getattr(m, 'symbol', 'Unknown')
            volume = getattr(m, 'volume', 0)
            close = getattr(m, 'close', 0)
            accumulated_volume = getattr(m, 'accumulated_volume', 0)
            high = getattr(m, 'high', 0)
            low = getattr(m, 'low', 0)
            open_price = getattr(m, 'open', 0)
            vwap = getattr(m, 'vwap', 0)

            if 'NDXP' in symbol:
                if 'C' in symbol and symbol.count('C') == 1:
                    option_type = 'CALL'
                    strike_part = symbol.split('C')[1]
                elif 'P' in symbol and symbol.count('P') >= 2:
                    option_type = 'PUT'
                    parts = symbol.split('P')
                    strike_part = parts[-1]
                else:
                    option_type = 'UNK'
                    strike_part = '0'

                try:
                    strike_price = int(strike_part[:5])
                    print(f"[{timestamp}] {option_type} ${strike_price:,} | Price: ${close:.2f} | Vol: {volume} | Total Vol: {accumulated_volume}")

                    full_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    formatted_strike = f"${strike_price:,}"

                    # Create data dictionary for storage
                    data_dict = {
                        'Timestamp': full_timestamp,
                        'Symbol': symbol,
                        'Option_Type': option_type,
                        'Strike_Price': formatted_strike,
                        'Close_Price': close,
                        'Volume': volume,
                        'Accumulated_Volume': accumulated_volume,
                        'High': high,
                        'Low': low,
                        'Open': open_price,
                        'VWAP': vwap
                    }

                    if volume > 20:
                        if store_data(data_dict):
                            print(f" 📊 Data stored in memory")

                except Exception as e:
                    print(f"Error parsing: {e}")

def is_market_hours():
    """Check if current time is within market hours (8:29 AM - 3:01 PM CST)"""
    cst = pytz.timezone('America/Chicago')
    now = datetime.datetime.now(cst)

    # Market opens at 8:29 AM CST
    market_open = now.replace(hour=8, minute=29, second=0, microsecond=0)
    # Market closes at 3:01 PM CST
    market_close = now.replace(hour=15, minute=1, second=0, microsecond=0)

    return market_open <= now <= market_close

def create_subscriptions(strike, base_date):
    """Create all option subscriptions based on current strike price"""
    global client

    strike_interval = 10

    print(f"\n📡 SUBSCRIBING ALL TICKERS VIA SINGLE WEBSOCKET CONNECTION")
    print(f"📍 Center Strike: ${strike:,}")
    print(f"📅 Expiry Date: {base_date}")
    print("-" * 60)

    subscription_count = 0

    # 1. Base ticker
    original_ticker = f"AM.O:NDXP{base_date}C{strike:05d}000"
    print(f"1. Base Ticker: {original_ticker}")
    client.subscribe(original_ticker)
    subscription_count += 1

    # 2. Test Range
    test_strikes = [
        strike - 500,
        strike - 200,
        strike,
        strike + 200,
        strike + 500
    ]

    print(f"\n2. Test Range (±500 points):")
    for test_strike in test_strikes:
        test_call = f"AM.O:NDXP{base_date}C{test_strike:05d}000"
        test_put = f"AM.O:NDXP{base_date}P{test_strike:05d}000"
        print(f"   CALL: ${test_strike:,} | PUT: ${test_strike:,}")
        client.subscribe(test_call)
        client.subscribe(test_put)
        subscription_count += 2

    # 3. PUTs below
    print(f"\n3. PUT Options (30 strikes below ${strike:,}):")
    for i in range(1, 31):
        put_strike = strike - (i * strike_interval)
        put_ticker = f"AM.O:NDXP{base_date}P{put_strike:05d}000"
        client.subscribe(put_ticker)
        subscription_count += 1

    # 4. PUTs above
    print(f"\n4. PUT Options (20 strikes above ${strike:,}):")
    for i in range(1, 21):
        put_strike = strike + (i * strike_interval)
        put_ticker = f"AM.O:NDXP{base_date}P{put_strike:05d}000"
        client.subscribe(put_ticker)
        subscription_count += 1

    # 5. CALLs below
    print(f"\n5. CALL Options (20 strikes below ${strike:,}):")
    for i in range(1, 21):
        call_strike = strike - (i * strike_interval)
        call_ticker = f"AM.O:NDXP{base_date}C{call_strike:05d}000"
        client.subscribe(call_ticker)
        subscription_count += 1

    # 6. CALLs above
    print(f"\n6. CALL Options (20 strikes above ${strike:,}):")
    for i in range(1, 21):
        call_strike = strike + (i * strike_interval)
        call_ticker = f"AM.O:NDXP{base_date}C{call_strike:05d}000"
        client.subscribe(call_ticker)
        subscription_count += 1

    print("-" * 60)
    print(f"✅ TOTAL SUBSCRIPTIONS: {subscription_count} tickers")
    print(f"🔗 ALL USING SINGLE WEBSOCKET CONNECTION")
    print(f"📊 Connection reuses same WebSocket client instance")
    print("-" * 60)

def run_websocket_client():
    """
    Main WebSocket client loop with dynamic reconnection
    Reconnects every 10 minutes with latest real-time strike price
    Only runs during market hours: 8:29 AM - 3:01 PM CST
    """
    global current_strike, last_strike, live_ndx_price, next_refresh_time, reconnect_flag, websocket_running, client

    # Check if we're within market hours before starting
    if not is_market_hours():
        cst = pytz.timezone('America/Chicago')
        now = datetime.datetime.now(cst)
        market_open = now.replace(hour=8, minute=29, second=0, microsecond=0)
        market_close = now.replace(hour=15, minute=1, second=0, microsecond=0)

        print(f"\n⏰ MARKET IS CLOSED")
        print(f"🕐 Current CST time: {now.strftime('%I:%M:%S %p')}")
        print(f"📅 Current date: {now.strftime('%B %d, %Y (%A)')}")
        print(f"🔔 Market hours: 8:29 AM - 3:01 PM CST")

        if now < market_open:
            time_until_open = market_open - now
            hours, remainder = divmod(time_until_open.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            print(f"⏳ Market opens in: {hours}h {minutes}m {seconds}s")
        else:
            print(f"📊 Market closed for today. Opens tomorrow at 8:29 AM CST")

        print(f"💤 WebSocket client will not start outside market hours")
        websocket_running = False
        return

    retry_count = 0
    max_retries = 100

    # Get initial strike price and live price
    current_strike, live_price = get_current_ndx_price()
    last_strike = current_strike
    live_ndx_price = live_price

    # Get today's date for options
    cst = pytz.timezone('US/Central')
    today = datetime.datetime.now(cst)
    base_date = today.strftime("%y%m%d")

    print(f"📅 Today's Date: {today.strftime('%B %d, %Y')}")
    print(f"📅 Expiry Code: {base_date}")
    print(f"📊 Initial NDX Strike Level: ${current_strike:,}")

    # Start background thread to check strike every 10 minutes
    websocket_running = True
    monitor_thread = threading.Thread(target=check_strike_and_reconnect, daemon=True)
    monitor_thread.start()
    print("✅ Started 10-minute strike monitoring thread")

    while retry_count < max_retries and is_market_hours():
        try:
            # Initialize WebSocket client
            initialize_websocket_client()

            # Create subscriptions with current strike
            create_subscriptions(current_strike, base_date)

            now = datetime.datetime.now(pytz.timezone('America/Chicago'))
            market_close = now.replace(hour=15, minute=0, second=0, microsecond=0)
            time_remaining = market_close - now

            print(f"\n🚀 Starting WebSocket client (Attempt {retry_count + 1})...")
            print(f"🕐 Current CST time: {now.strftime('%H:%M:%S')}")
            print(f"⏰ Time until 3:00 PM CST: {time_remaining}")
            print("📡 Listening for options data on SINGLE WebSocket connection...")
            print("💡 If no messages appear within 30 seconds, there may be no active trading on these strikes")

            # Reset reconnect flag
            reconnect_flag = False

            # Run WebSocket in a separate thread so we can check for reconnect flag
            ws_thread = threading.Thread(target=lambda: client.run(handle_msg), daemon=True)
            ws_thread.start()

            # Monitor for reconnection trigger
            while ws_thread.is_alive() and is_market_hours():
                if reconnect_flag:
                    print(f"\n🔄 RECONNECTION TRIGGERED!")
                    print(f"   Old Strike: ${last_strike:,}")
                    print(f"   New Strike: ${current_strike:,}")
                    print(f"   Closing current connection...")

                    # Close current connection
                    try:
                        client.close()
                    except:
                        pass

                    last_strike = current_strike
                    reconnect_flag = False

                    print(f"✅ Connection closed. Will reconnect with new strike...")
                    break

                time.sleep(1)  # Check every second

            if not reconnect_flag:
                # Normal exit (market closed or thread ended)
                break

        except KeyboardInterrupt:
            print("\n🛑 User interrupted - shutting down...")
            websocket_running = False
            break

        except Exception as e:
            retry_count += 1
            print(f"\n❌ Connection error (Attempt {retry_count}): {e}")
            if retry_count < max_retries and is_market_hours():
                wait_time = min(retry_count * 5, 120)
                print(f"⏳ Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                print("🏁 Max retries reached or market closed")
                websocket_running = False
                break

    websocket_running = False
    print(f"\n✅ WebSocket client stopped")

def websocket_manager():
    """
    Manages WebSocket client lifecycle - starts it during market hours,
    waits when market is closed, and restarts when market opens
    """
    while True:
        if is_market_hours():
            # Market is open - run WebSocket client
            run_websocket_client()
            # If we get here, WebSocket stopped (market closed or error)
            # Wait a bit before checking again
            time.sleep(60)
        else:
            # Market is closed - wait and check again
            cst = pytz.timezone('America/Chicago')
            now = datetime.datetime.now(cst)
            market_open = now.replace(hour=8, minute=29, second=0, microsecond=0)

            if now < market_open:
                # Before market open today
                time_until_open = (market_open - now).total_seconds()
                print(f"\n⏰ Market opens in {time_until_open/3600:.1f} hours")
                print(f"💤 Sleeping until market opens...")
                # Sleep until 1 minute before market open
                sleep_time = max(60, time_until_open - 60)
                time.sleep(sleep_time)
            else:
                # After market close - wait until tomorrow
                print(f"\n📊 Market closed for today")
                print(f"💤 Will check again in 1 hour...")
                time.sleep(3600)  # Check every hour

if __name__ == "__main__":
    # Display startup information
    print("\n🎯 Starting NDX Options Monitor with Dynamic Strike Adjustment...")
    print("📊 Volume threshold: >20 for data storage")
    print("🕒 Market hours: 8:29 AM - 3:01 PM CST")
    print("🔗 All subscriptions using SINGLE WebSocket connection")
    print("⚡ Auto-reconnect when strike changes >100 points")
    print("🔍 Strike check interval: Every 10 minutes")
    print("🌐 API available at: http://localhost:5000/api/options")
    print("-" * 60)

    # Start WebSocket manager in background thread
    ws_thread = threading.Thread(target=websocket_manager, daemon=True)
    ws_thread.start()

    # Start Flask API server (this will run forever)
    print("🌐 Starting Flask API server on port 5000...")
    print("✅ Flask API server ready to accept requests")
    start_flask_server()

