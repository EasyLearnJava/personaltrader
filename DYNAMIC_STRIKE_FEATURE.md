# 🎯 Dynamic Strike Adjustment Feature

## 🚀 What's New

Your NDX Options Monitor now has **intelligent dynamic strike adjustment**!

### ✨ Key Features

1. **Auto-Fetch NDX Price** - Uses Polygon.io API to get current NDX index price
2. **Smart Reconnection** - Only reconnects when strike changes significantly
3. **10-Minute Monitoring** - Checks NDX price every 10 minutes
4. **Threshold-Based** - Reconnects only if strike changes by >100 points
5. **Zero Downtime** - Continues collecting data while monitoring

---

## 🔄 How It Works

### **Initial Connection**
```
1. Fetch current NDX price from Polygon.io
2. Calculate strike (round to nearest 10)
3. Connect to WebSocket
4. Subscribe to ~111 option contracts
5. Start collecting data
6. Start background monitoring thread
```

### **Every 10 Minutes**
```
1. Background thread wakes up
2. Fetch current NDX price
3. Calculate new strike
4. Compare with current strike

   IF change > 100 points:
      → Close WebSocket
      → Reconnect with new strike
      → Resume data collection
   
   ELSE:
      → Continue current connection
      → Keep collecting data
```

---

## 📊 Example Scenarios

### **Scenario 1: Small Movement (No Reconnection)**

```
9:00 AM - NDX at $25,650 → Strike: 25,650 → Connect
9:10 AM - NDX at $25,680 → Strike: 25,680 → Change: 30 points → Continue
9:20 AM - NDX at $25,720 → Strike: 25,720 → Change: 40 points → Continue
9:30 AM - NDX at $25,740 → Strike: 25,740 → Change: 20 points → Continue
```

**Result:** No reconnection needed. Continues monitoring same strikes.

---

### **Scenario 2: Large Movement (Reconnection Triggered)**

```
9:00 AM - NDX at $25,650 → Strike: 25,650 → Connect
9:10 AM - NDX at $25,680 → Strike: 25,680 → Change: 30 points → Continue
9:20 AM - NDX at $25,780 → Strike: 25,780 → Change: 130 points → RECONNECT!
9:20 AM - Close connection
9:20 AM - Reconnect with strike 25,780
9:30 AM - NDX at $25,800 → Strike: 25,800 → Change: 20 points → Continue
```

**Result:** Reconnected at 9:20 AM due to >100 point change.

---

## 🔧 Configuration

### **API Key**
The code now uses **Polygon.io API** instead of Massive.com:

```python
POLYGON_API_KEY = "wsWMG2p9vhDDjVxAHSRz6qbSR_a7B1wL"
```

### **Reconnection Threshold**
Currently set to **100 points**. To change:

```python
# In check_strike_and_reconnect() function
if strike_change > 100:  # Change this value
    reconnect_flag = True
```

### **Check Interval**
Currently checks every **10 minutes**. To change:

```python
# In check_strike_and_reconnect() function
time.sleep(600)  # 600 seconds = 10 minutes
```

---

## 📈 Benefits

### **1. Always Relevant Strikes**
- Monitors options near current NDX price
- Automatically adjusts as market moves
- No manual intervention needed

### **2. Efficient Resource Usage**
- Only reconnects when necessary (>100 point change)
- Avoids unnecessary reconnections
- Reduces API calls

### **3. Better Data Quality**
- Captures high-volume strikes
- Follows market movement
- More relevant trading data

### **4. Automatic Operation**
- Set it and forget it
- Runs 24/7 without manual updates
- Adapts to market conditions

---

## 🔍 Monitoring & Logs

### **What You'll See in Logs**

**Initial Connection:**
```
✅ Fetched NDX price: $25,647.32 → Strike: $25,650
📅 Today's Date: December 30, 2025
📅 Expiry Code: 251230
📊 Initial NDX Strike Level: $25,650
✅ Started 10-minute strike monitoring thread
```

**10-Minute Check (No Change):**
```
🔍 10-Minute Strike Check:
   Current Strike: $25,650
   New Strike: $25,680
   Change: $30
✅ Strike change ≤100 points. Continuing current connection.
```

**10-Minute Check (Reconnection):**
```
🔍 10-Minute Strike Check:
   Current Strike: $25,650
   New Strike: $25,780
   Change: $130
⚠️ Strike changed by >100 points! Triggering reconnection...

🔄 RECONNECTION TRIGGERED!
   Old Strike: $25,650
   New Strike: $25,780
   Closing current connection...
✅ Connection closed. Will reconnect with new strike...
```

---

## 🎯 Strike Calculation Logic

### **Rounding to Nearest 10**
```python
NDX Price: $25,647.32
↓
Round to nearest 10: $25,650
↓
Strike: 25650
```

### **Subscription Range**
With strike at **25,650**, you monitor:

| Type | Range | Count |
|------|-------|-------|
| PUTs Below | 25,350 - 25,640 | 30 |
| PUTs Above | 25,660 - 25,850 | 20 |
| CALLs Below | 25,450 - 25,640 | 20 |
| CALLs Above | 25,660 - 25,850 | 20 |
| Test Range | 25,150 - 26,150 | 10 |
| **Total** | | **~111 contracts** |

---

## 🚨 Error Handling

### **If Polygon API Fails**
```python
⚠️ Error fetching NDX price: Connection timeout
⚠️ Using fallback strike: $25,650
```

Falls back to default strike (25,650) and continues operation.

### **If Reconnection Fails**
- Retries with exponential backoff
- Maximum 100 retry attempts
- Logs all errors for debugging

---

## 💡 Tips

1. **Monitor Logs** - Watch for reconnection events
2. **Adjust Threshold** - Change from 100 to 50 or 200 based on your needs
3. **Check Interval** - Reduce to 5 minutes for faster response
4. **API Limits** - Polygon free tier: 5 calls/minute (plenty for 10-min checks)

---

## 🔄 Upgrade from Old Version

### **What Changed**

| Old Version | New Version |
|-------------|-------------|
| Hard-coded strike: 25650 | Dynamic strike from API |
| Never reconnects | Smart reconnection |
| Massive.com API key | Polygon.io API key |
| Manual updates needed | Fully automatic |

### **Migration Steps**

1. ✅ Code already updated
2. ✅ Update Railway environment variable:
   - Remove: `MASSIVE_API_KEY`
   - Add: `POLYGON_API_KEY=wsWMG2p9vhDDjVxAHSRz6qbSR_a7B1wL`
3. ✅ Redeploy to Railway
4. ✅ Monitor logs to verify dynamic strike is working

---

## 📞 Questions?

See the main documentation:
- `README.md` - Project overview
- `DEPLOYMENT_GUIDE.md` - Deployment instructions
- `QUICKSTART.md` - Quick start guide

---

**Happy Trading! 📊🚀**

Your NDX Options Monitor now intelligently adapts to market movements!

