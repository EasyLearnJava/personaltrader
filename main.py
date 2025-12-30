from massive import WebSocketClient
from massive.websocket.models import WebSocketMessage, Feed, Market
from typing import List
import gspread
from google.oauth2.service_account import Credentials
import datetime
import os
import time
import pytz
import requests
import threading

# Configuration
POLYGON_API_KEY = "wsWMG2p9vhDDjVxAHSRz6qbSR_a7B1wL"
GOOGLE_SHEET_NAME = "Dataintab"
CREDENTIALS_FILE = "service_account.json"

# Global variables for dynamic strike management
current_strike = None
last_strike = None
reconnect_flag = False
websocket_running = False

# Initialize Google Sheets client
def init_google_sheets():
    try:
        if not os.path.exists(CREDENTIALS_FILE):
            print(f"❌ {CREDENTIALS_FILE} not found. Please follow GOOGLE_SHEETS_SETUP.md")
            return None

        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scope)
        gc = gspread.authorize(credentials)
        sheet = gc.open(GOOGLE_SHEET_NAME).sheet1

        try:
            existing_data = sheet.get_all_records()
            if not existing_data:
                headers = ['Timestamp', 'Symbol', 'Option_Type', 'Strike_Price', 'Close_Price',
                           'Volume', 'Accumulated_Volume', 'High', 'Low', 'Open', 'VWAP']
                sheet.append_row(headers)
                print("✅ Google Sheet initialized with headers")
        except Exception as header_error:
            print(f"⚠️ Header check issue (sheet may have existing data): {header_error}")

        return sheet
    except Exception as e:
        print(f"❌ Google Sheets setup error: {e}")
        return None

# Initialize Google Sheets
google_sheet = init_google_sheets()

# WebSocket client (will be initialized dynamically)
client = None

# Debug counters
message_count = 0
last_message_time = None

def get_current_ndx_price():
    """
    Fetch current NDX index price from Polygon.io
    Returns the price rounded to nearest 10 (strike interval)
    """
    try:
        url = f"https://api.polygon.io/v2/aggs/ticker/I:NDX/prev?apiKey={POLYGON_API_KEY}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if 'results' in data and len(data['results']) > 0:
                price = data['results'][0]['c']  # Close price
                strike = round(price / 10) * 10  # Round to nearest 10
                print(f"✅ Fetched NDX price: ${price:,.2f} → Strike: ${int(strike):,}")
                return int(strike)
        else:
            print(f"⚠️ Polygon API returned status {response.status_code}")
    except Exception as e:
        print(f"⚠️ Error fetching NDX price: {e}")

    # Fallback to default
    default_strike = 25650
    print(f"⚠️ Using fallback strike: ${default_strike:,}")
    return default_strike

def check_strike_and_reconnect():
    """
    Background thread that checks NDX price every 10 minutes
    Triggers reconnection if strike changes by more than 100 points
    """
    global current_strike, last_strike, reconnect_flag, websocket_running

    while websocket_running:
        time.sleep(600)  # Wait 10 minutes (600 seconds)

        if not websocket_running:
            break

        new_strike = get_current_ndx_price()
        strike_change = abs(new_strike - current_strike)

        print(f"\n🔍 10-Minute Strike Check:")
        print(f"   Current Strike: ${current_strike:,}")
        print(f"   New Strike: ${new_strike:,}")
        print(f"   Change: ${strike_change:,}")

        if strike_change > 100:
            print(f"⚠️ Strike changed by >{100} points! Triggering reconnection...")
            current_strike = new_strike
            reconnect_flag = True
        else:
            print(f"✅ Strike change ≤100 points. Continuing current connection.")

def initialize_websocket_client():
    """Initialize or reinitialize the WebSocket client"""
    global client

    print("🔗 Initializing WebSocket connection...")
    client = WebSocketClient(
        api_key=POLYGON_API_KEY,
        feed=Feed.RealTime,
        market=Market.Options
    )
    return client

def write_to_sheet(data_row):
    global google_sheet
    if google_sheet:
        try:
            google_sheet.append_row(data_row)
            return True
        except Exception as e:
            print(f"❌ Error writing to sheet: {e}")
            return False
    return False

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
                    data_row = [
                        full_timestamp, symbol, option_type, formatted_strike, close,
                        volume, accumulated_volume, high, low, open_price, vwap
                    ]

                    if volume > 20 and google_sheet:
                        if write_to_sheet(data_row):
                            print(f" 📊 Data saved to Google Sheet")

                except Exception as e:
                    print(f"Error parsing: {e}")

def is_market_hours():
    cst = pytz.timezone('America/Chicago')
    now = datetime.datetime.now(cst)
    market_close = now.replace(hour=15, minute=0, second=0, microsecond=0)
    return now < market_close

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
    Reconnects when strike changes by >100 points
    """
    global current_strike, last_strike, reconnect_flag, websocket_running, client

    retry_count = 0
    max_retries = 100

    # Get initial strike price
    current_strike = get_current_ndx_price()
    last_strike = current_strike

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

# Main execution
print("\n🎯 Starting NDX Options Monitor with Dynamic Strike Adjustment...")
print("📊 Volume threshold: >20 for Google Sheets")
print("🕒 Running until 3:00 PM CST")
print("🔗 All subscriptions using SINGLE WebSocket connection")
print("⚡ Auto-reconnect when strike changes >100 points")
print("🔍 Strike check interval: Every 10 minutes")
print("-" * 60)

run_websocket_client()

print(f"\n📊 Total messages received: {message_count}")
if last_message_time:
    print(f"🕐 Last message received at: {last_message_time.strftime('%H:%M:%S')}")
print("👋 Goodbye!")
