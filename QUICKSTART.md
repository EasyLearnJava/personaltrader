# ⚡ Quick Start Guide

Get your NDX Options Monitor up and running in 10 minutes!

## 🎯 What You'll Get

- ✅ Python backend running on Railway (24/7)
- ✅ React dashboard hosted on Vercel
- ✅ Real-time data flowing through Google Sheets

---

## 📋 Before You Start

Make sure you have:
1. ✅ GitHub account
2. ✅ Railway account ([railway.app](https://railway.app))
3. ✅ Vercel account ([vercel.com](https://vercel.com))
4. ✅ Google Cloud account
5. ✅ Your `service_account.json` file

---

## 🚀 Step-by-Step Deployment

### Step 1: Google Sheets Setup (5 minutes)

1. **Create Google Sheet**
   - Name it: `Dataintab`
   - Note the Sheet ID from URL

2. **Enable Google Sheets API**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Enable "Google Sheets API"
   - Create Service Account
   - Download `service_account.json`

3. **Share Sheet**
   - Share `Dataintab` with service account email
   - Give Editor permissions
   - Make sheet publicly viewable (for dashboard)

4. **Get API Key**
   - In Google Cloud Console → Credentials
   - Create API Key
   - Restrict to Google Sheets API

---

### Step 2: Deploy Backend to Railway (3 minutes)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Complete NDX Options Monitor"
   git push origin main
   ```

2. **Deploy on Railway**
   - Go to [railway.app](https://railway.app)
   - New Project → Deploy from GitHub
   - Select: `EasyLearnJava/personaltrader`

3. **Add Environment Variables**
   ```
   POLYGON_API_KEY=wsWMG2p9vhDDjVxAHSRz6qbSR_a7B1wL
   GOOGLE_SHEET_NAME=Dataintab
   ```

4. **Upload Service Account**
   - Upload `service_account.json` in Railway settings

5. **Deploy!**
   - Railway auto-deploys
   - Check logs to verify it's running

---

### Step 3: Deploy Frontend to Vercel (2 minutes)

1. **Deploy on Vercel**
   - Go to [vercel.com](https://vercel.com)
   - New Project → Import from GitHub
   - Select: `EasyLearnJava/personaltrader`
   - Root Directory: `frontend`

2. **Add Environment Variables**
   ```
   VITE_GOOGLE_SHEET_ID=your_sheet_id_here
   VITE_GOOGLE_API_KEY=your_api_key_here
   VITE_REFRESH_INTERVAL=5000
   ```

3. **Deploy!**
   - Vercel builds and deploys
   - Get your dashboard URL

---

## ✅ Verification

### Check Backend (Railway)
1. Open Railway logs
2. Look for: "🔗 Initializing SINGLE WebSocket connection"
3. Verify data appearing in Google Sheets

### Check Frontend (Vercel)
1. Open your Vercel URL
2. Dashboard should load with data
3. Auto-refresh every 5 seconds

---

## 🎉 You're Done!

Your complete system is now live:
- **Backend**: Running 24/7 on Railway
- **Frontend**: Hosted on Vercel
- **Data**: Synced via Google Sheets

**Dashboard URL**: `https://your-project.vercel.app`

---

## 🔧 Troubleshooting

### No data in dashboard?
- Check if backend is running (Railway logs)
- Verify Google Sheet is publicly readable
- Check browser console for errors

### Backend not connecting?
- Verify `service_account.json` is uploaded
- Check Google Sheet permissions
- Review Railway logs for errors

### Need help?
See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

---

## 💰 Monthly Cost: $5

- Railway: $5/month
- Vercel: Free
- Google Sheets: Free

---

## 📞 Next Steps

1. Customize volume threshold in `main.py`
2. Adjust auto-refresh interval in frontend
3. Add more filters and charts
4. Set up alerts for high-volume trades

Enjoy your real-time NDX Options Monitor! 📊🚀

