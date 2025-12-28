# 📊 NDX Options Monitor - Codebase Explanation

## 🆕 Recent Updates

**Key Changes in Latest Version:**
1. ✅ **Strike Price Updated**: Center strike moved from $25,500 → **$25,650**
2. ✅ **Expanded Coverage**: Now monitoring **~101 contracts** (nearly doubled from ~52)
3. ✅ **Better Organization**: Options grouped into 6 distinct subscription categories
4. ✅ **Comprehensive Range**: Both CALL and PUT options now tracked above AND below center strike
5. ✅ **API Key Added**: Massive.io API key is now configured in the code

---

## 🎯 What Does This Application Do?

This is a **real-time stock options monitoring system** that tracks NASDAQ-100 Index (NDX) options and automatically saves trading data to Google Sheets.

Think of it as a **live data recorder** that:
- Watches specific stock options prices in real-time
- Filters for active trading (volume > 20)
- Automatically logs the data to a Google spreadsheet for analysis

---

## 🔍 High-Level Overview

### The Big Picture
```
Live Market Data → WebSocket Connection → Python Script → Google Sheets
   (Massive.io)         (Real-time)        (Filters &      (Storage)
                                           Processes)
```

### What Happens When You Run It:
1. **Connects** to Massive.io's live market data feed
2. **Subscribes** to ~101 different NDX option contracts (both CALL and PUT options)
3. **Listens** for price updates throughout the trading day
4. **Filters** for options with trading volume > 20
5. **Saves** the data to your Google Sheet named "Dataintab"
6. **Runs** until 3:00 PM Central Time (market close)

---

## 🏗️ Main Components

### 1. **WebSocket Connection** (Lines 48-54)
- Uses a **single connection** to receive live market data
- Connects to Massive.io's real-time options feed
- More efficient than creating multiple connections

### 2. **Google Sheets Integration** (Lines 17-43)
- Connects to Google Sheets using a service account
- Creates headers if the sheet is empty
- Writes filtered trading data automatically

### 3. **Message Handler** (Lines 72-124)
- Processes incoming market data messages
- Extracts important information (price, volume, strike price)
- Filters for NDXP options only
- Saves to Google Sheets when volume > 20

### 4. **Subscription Manager** (Lines 128-198)
- Subscribes to ~101 different option contracts
- Covers a comprehensive range of strike prices around $25,650
- Includes both CALL and PUT options above AND below center strike
- Organized into 6 distinct subscription groups for better coverage

### 5. **Market Hours Monitor** (Lines 126-131)
- Checks if it's before 3:00 PM CST
- Automatically stops when market closes

---

## 📈 What Options Are Being Tracked?

### Current Configuration:
- **Center Strike Price**: $25,650 (updated from $25,500)
- **Expiry Date**: Today's date (changes daily)
- **Option Types**: Both CALL and PUT options

### Strike Price Coverage:
The system now monitors a **comprehensive range** of options both above AND below the center strike:

**6 Subscription Groups:**

| Group | Type | Count | Strike Range | Description |
|-------|------|-------|--------------|-------------|
| 1 | Base | 1 | $25,650 | Center strike CALL option |
| 2 | Test | 10 | $25,150 - $26,150 | Wide range for testing (±500) |
| 3 | PUT Below | 30 | $25,640 - $25,350 | Downside protection tracking |
| 4 | PUT Above | 20 | $25,660 - $25,850 | Upside PUT tracking |
| 5 | CALL Below | 20 | $25,640 - $25,450 | Downside CALL tracking |
| 6 | CALL Above | 20 | $25,660 - $25,850 | Upside CALL tracking |

**Total**: **~101 different option contracts** monitored simultaneously (nearly doubled coverage!)

**Visual Coverage Map:**
```
        PUTs Below (30)    CALLs Below (20)
              ↓                  ↓
    $25,350 ←──────── $25,650 ────────→ $25,850
                         ↑
                   Center Strike
                         ↑
              ↑                  ↑
        PUTs Above (20)    CALLs Above (20)
```

---

## 📊 Data Being Collected

Each time an option with volume > 20 trades, the following data is saved:

| Column | Description | Example |
|--------|-------------|---------|
| **Timestamp** | When the data was recorded | 2024-12-26 14:30:15 |
| **Symbol** | Full option ticker symbol | AM.O:NDXP251226C25500000 |
| **Option_Type** | CALL or PUT | CALL |
| **Strike_Price** | Exercise price of the option | $25,500 |
| **Close_Price** | Last traded price | $125.50 |
| **Volume** | Number of contracts in this update | 45 |
| **Accumulated_Volume** | Total volume for the day | 1,250 |
| **High** | Highest price so far today | $130.00 |
| **Low** | Lowest price so far today | $120.00 |
| **Open** | Opening price | $122.00 |
| **VWAP** | Volume-weighted average price | $125.25 |

---

## 🔧 How It Works - Step by Step

### Startup Process:
1. **Initialize Google Sheets** connection
2. **Create WebSocket** client
3. **Calculate today's date** in the required format (YYMMDD)
4. **Subscribe to all option contracts** (~101 total across 6 groups)
5. **Start listening** for market data

### During Operation:
1. **Receive** real-time price updates via WebSocket
2. **Parse** the symbol to identify option type and strike price
3. **Check** if it's an NDXP option
4. **Check** if volume > 20
5. **Format** the data into a row
6. **Append** to Google Sheet
7. **Print** confirmation to console

### Shutdown:
- Automatically stops at 3:00 PM CST
- Can be manually stopped with Ctrl+C
- Shows total messages received

---

## 🛡️ Error Handling & Reliability

### Built-in Safety Features:
- **Retry Logic**: Up to 100 retries if connection drops
- **Market Hours Check**: Won't run outside trading hours
- **Credential Validation**: Checks for service account file
- **Graceful Shutdown**: Handles interruptions cleanly
- **Heartbeat Messages**: Shows activity every 10 messages

### What Happens If:
- **No credentials file**: Shows error and instructions
- **Connection drops**: Automatically reconnects with exponential backoff
- **Google Sheets error**: Logs error but continues monitoring
- **Market closes**: Stops automatically

---

## 📁 Project Files

| File | Purpose |
|------|---------|
| `main.py` | Main application code (258 lines) |
| `requirements.txt` | Python dependencies needed |
| `service_account.json` | Google Sheets credentials (not in repo) |
| `GOOGLE_SHEETS_SETUP.md` | Instructions for setting up Google Sheets |
| `README.md` | Basic project information |
| `CODEBASE_EXPLANATION.md` | This document - comprehensive codebase guide |

---

## 🔑 Key Configuration Values

Located at the top of `main.py`:

```python
MASSIVE_API_KEY = "COYGxJhf5qJVI3RXykycEawX9OVVKrUF"  # Your Massive.io API key
GOOGLE_SHEET_NAME = "Dataintab"                      # Name of your Google Sheet
CREDENTIALS_FILE = "service_account.json"            # Google credentials
current_strike = 25650                               # Center strike price ($25,650)
```

**⚠️ Note**: The API key is now populated in the code (previously empty).

---

## 💡 Use Cases

This tool is useful for:
- **Options Traders**: Track real-time options activity
- **Market Analysis**: Collect data for later analysis
- **Volume Monitoring**: Identify actively traded strikes
- **Price Discovery**: See where the market is trading
- **Historical Records**: Build a database of options prices

---

## 🚀 How to Use

1. **Setup Google Sheets** (follow GOOGLE_SHEETS_SETUP.md)
2. **Add your Massive.io API key** to `main.py`
3. **Run**: `python main.py`
4. **Monitor**: Watch console for live updates
5. **Check**: Open your "Dataintab" Google Sheet to see data

---

## 📝 Summary

This is a **professional-grade options monitoring tool** that bridges live market data with Google Sheets for easy analysis. It's designed to run hands-free during market hours, automatically collecting and organizing options trading data for the NASDAQ-100 Index.

**In Simple Terms**: It's like having a robot that watches the stock options market all day and writes down everything important in a spreadsheet for you to review later.

---

## 🔄 What Changed in the Latest Update?

### Previous Version vs. Current Version

| Aspect | Before | After | Impact |
|--------|--------|-------|--------|
| **Center Strike** | $25,500 | $25,650 | Adjusted to current market level |
| **Total Contracts** | ~52 | ~101 | Nearly **doubled** coverage |
| **Subscription Groups** | 4 groups | 6 groups | Better organization |
| **CALL Coverage** | Only above center | Above AND below | More comprehensive |
| **PUT Coverage** | Only below center | Above AND below | More comprehensive |
| **API Key** | Empty string | Configured | Ready to run |

### Why These Changes Matter:

1. **Better Market Coverage**: With ~101 contracts instead of ~52, you're capturing nearly twice as much market activity
2. **Symmetrical Tracking**: Both CALLs and PUTs are now tracked above and below the center strike, giving you a complete picture
3. **Current Market Alignment**: Strike price updated to $25,650 to match current NDX levels
4. **Ready to Deploy**: API key is now configured, so the system is ready to run immediately

### What Stayed the Same:

✅ Volume threshold (>20) for saving to Google Sheets
✅ Market hours monitoring (until 3:00 PM CST)
✅ Single WebSocket connection for efficiency
✅ Automatic retry logic and error handling
✅ Real-time data streaming and logging

