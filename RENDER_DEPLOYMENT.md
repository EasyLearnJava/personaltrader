# 🚀 Complete Render.com Deployment Guide

This guide walks you through deploying the entire NDX Options Monitor as a **single web service** on Render.com.

---

## 📋 What You'll Deploy

**Single Render.com Web Service** containing:
- ✅ Node.js Express server (serves React frontend)
- ✅ Python WebSocket backend (runs in background)
- ✅ React dashboard (built and served statically)

**Cost:** $7/month (Starter plan) or Free tier (with spin-down)

---

## 🎯 Prerequisites

Before starting, ensure you have:

1. ✅ **GitHub Account** - To host your code
2. ✅ **Render.com Account** - Sign up at [render.com](https://render.com)
3. ✅ **Google Cloud Account** - For Sheets API
4. ✅ **Service Account JSON** - From Google Cloud Console
5. ✅ **Polygon.io API Key** - Already have: `wsWMG2p9vhDDjVxAHSRz6qbSR_a7B1wL`

---

## 📝 Step 1: Prepare Google Sheets

### 1.1 Create Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new sheet
3. Name it: **`Dataintab`**
4. Note the Sheet ID from URL (optional, for reference)

### 1.2 Set Up Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing
3. Enable **Google Sheets API**:
   - Go to "APIs & Services" → "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

### 1.3 Create Service Account

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Fill in details:
   - **Name**: `ndx-options-monitor`
   - **Description**: `Service account for NDX options data`
4. Click "Create and Continue"
5. Skip optional steps, click "Done"

### 1.4 Generate JSON Key

1. Click on the service account you just created
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Choose **JSON** format
5. Click "Create"
6. **Save the downloaded JSON file** - you'll need this!

### 1.5 Share Sheet with Service Account

1. Open your `service_account.json` file
2. Copy the `client_email` value (looks like: `name@project.iam.gserviceaccount.com`)
3. Go back to your Google Sheet
4. Click "Share" button
5. Paste the service account email
6. Set permission to **Editor**
7. Uncheck "Notify people"
8. Click "Share"

✅ **Google Sheets setup complete!**

---

## 🔧 Step 2: Prepare Your Code

### 2.1 Push to GitHub

```bash
# Navigate to your project
cd TApp

# Add all files
git add .

# Commit changes
git commit -m "Prepare for Render.com deployment"

# Push to GitHub
git push origin main
```

### 2.2 Verify File Structure

Make sure your repository has:

```
TApp/
├── backend/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── server.js
├── package.json
├── render.yaml
└── README.md
```

---

## 🌐 Step 3: Deploy to Render.com

### 3.1 Create New Web Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** button (top right)
3. Select **"Web Service"**

### 3.2 Connect Repository

1. Click **"Connect a repository"**
2. Authorize Render to access your GitHub
3. Find and select: **`EasyLearnJava/personaltrader`**
4. Click **"Connect"**

### 3.3 Configure Service

Fill in the following settings:

| Setting | Value |
|---------|-------|
| **Name** | `ndx-options-monitor` |
| **Region** | Oregon (or closest to you) |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | See below ⬇️ |
| **Start Command** | `node server.js` |

**Build Command** (copy exactly):
```bash
pip install -r backend/requirements.txt && cd frontend && npm install && npm run build && cd .. && npm install
```

### 3.4 Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add these **3 variables**:

#### Variable 1: POLYGON_API_KEY
```
Key: POLYGON_API_KEY
Value: wsWMG2p9vhDDjVxAHSRz6qbSR_a7B1wL
```

#### Variable 2: GOOGLE_SHEET_NAME
```
Key: GOOGLE_SHEET_NAME
Value: Dataintab
```

#### Variable 3: GOOGLE_SERVICE_ACCOUNT_JSON
```
Key: GOOGLE_SERVICE_ACCOUNT_JSON
Value: <paste entire JSON content here>
```

**Important for Variable 3:**
1. Open your downloaded `service_account.json` file
2. Copy **ALL** the content (entire JSON object)
3. Paste it as a **single line** in the value field
4. Make sure it starts with `{` and ends with `}`

Example format:
```json
{"type":"service_account","project_id":"your-project",...}
```

### 3.5 Select Plan

- **Free Tier**: Spins down after 15 mins of inactivity (not recommended for 24/7)
- **Starter Plan**: $7/month, always running (recommended)

Choose based on your needs.

### 3.6 Deploy!

1. Click **"Create Web Service"**
2. Render will start building your app
3. Watch the logs in real-time
4. First deployment takes **5-10 minutes**

---

## ✅ Step 4: Verify Deployment

### 4.1 Check Build Logs

You should see:
```
Installing Python dependencies...
Building frontend...
Installing Node.js dependencies...
Build successful!
```

### 4.2 Check Runtime Logs

After deployment, you should see:
```
✅ Frontend server running on port 3000
🐍 Starting Python backend...
✅ Fetched NDX price: $25,647.32 → Strike: $25,650
📡 SUBSCRIBING ALL TICKERS VIA SINGLE WEBSOCKET CONNECTION
✅ TOTAL SUBSCRIPTIONS: 111 tickers
```

### 4.3 Access Your App

Your app will be available at:
```
https://ndx-options-monitor.onrender.com
```

(Replace with your actual Render URL)

---

## 🎉 Success!

Your app is now live! You should see:
- ✅ React dashboard loading
- ✅ Data appearing in Google Sheets
- ✅ Real-time updates every 5 seconds

---

## 🔍 Troubleshooting

### Build Fails

**Error:** `pip: command not found`
- **Fix:** Make sure Runtime is set to "Python 3"

**Error:** `npm: command not found`
- **Fix:** Render auto-installs Node.js with Python runtime

### Python Backend Not Starting

**Check logs for:**
```
❌ No Google credentials found
```
- **Fix:** Verify `GOOGLE_SERVICE_ACCOUNT_JSON` is set correctly
- Make sure it's the entire JSON content, not a file path

### No Data in Dashboard

1. Check Google Sheet - is data appearing there?
2. Check browser console for errors
3. Verify sheet is publicly readable or shared with service account

### App Spins Down (Free Tier)

- Free tier spins down after 15 minutes of inactivity
- Upgrade to Starter plan ($7/month) for 24/7 operation

---

## 🔄 Updating Your App

To deploy updates:

```bash
git add .
git commit -m "Update description"
git push origin main
```

Render will automatically rebuild and redeploy!

---

## 📊 Monitoring

### View Logs
1. Go to Render dashboard
2. Click on your service
3. Click "Logs" tab
4. See real-time logs from both Node.js and Python

### Check Health
Visit: `https://your-app.onrender.com/api/health`

Should return:
```json
{"status":"ok","message":"Server is running"}
```

---

## 💡 Tips

1. **Use Starter Plan** for production (24/7 uptime)
2. **Monitor logs** regularly for errors
3. **Check Google Sheets** to verify data collection
4. **Set up alerts** in Render for downtime notifications

---

## 🎯 Next Steps

- ✅ Monitor your app for a few hours
- ✅ Verify data is being collected
- ✅ Customize dashboard as needed
- ✅ Set up monitoring/alerts

---

**🎉 Congratulations! Your NDX Options Monitor is live on Render.com!**

