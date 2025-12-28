# 🚀 Complete Deployment Guide

This guide will help you deploy both the **Python backend** (Railway) and **React frontend** (Vercel).

---

## 📋 Prerequisites

Before you begin, make sure you have:

- ✅ GitHub account
- ✅ Railway account (sign up at [railway.app](https://railway.app))
- ✅ Vercel account (sign up at [vercel.com](https://vercel.com))
- ✅ Google Cloud account with Sheets API enabled
- ✅ Your `service_account.json` file from Google Cloud

---

## 🔧 Part 1: Google Sheets Setup

### Step 1: Enable Google Sheets API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **Google Sheets API**
4. Create a **Service Account**
5. Download the JSON credentials file as `service_account.json`

### Step 2: Share Your Google Sheet

1. Open your Google Sheet named "Dataintab"
2. Click **Share** button
3. Add the service account email (found in `service_account.json`)
4. Give it **Editor** permissions

### Step 3: Make Sheet Publicly Readable (for Frontend)

1. Click **Share** → **Get link**
2. Change to **Anyone with the link can view**
3. Copy the Sheet ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID_HERE/edit
   ```

### Step 4: Get Google API Key (for Frontend)

1. In Google Cloud Console, go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **API Key**
3. Copy the API key
4. Restrict it to **Google Sheets API** only (recommended)

---

## 🐍 Part 2: Deploy Python Backend to Railway

### Step 1: Push Code to GitHub

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit with backend and frontend"

# Add your GitHub repository
git remote add origin https://github.com/EasyLearnJava/personaltrader.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Click **New Project** → **Deploy from GitHub repo**
3. Select your repository: `EasyLearnJava/personaltrader`
4. Railway will auto-detect the Python project

### Step 3: Configure Environment Variables

In Railway dashboard, go to **Variables** tab and add:

```
MASSIVE_API_KEY=COYGxJhf5qJVI3RXykycEawX9OVVKrUF
GOOGLE_SHEET_NAME=Dataintab
```

### Step 4: Upload Service Account JSON

Option A: Upload as file
1. In Railway, go to **Settings** → **Service**
2. Upload `service_account.json`

Option B: Add as environment variable
1. Copy entire content of `service_account.json`
2. Add as variable: `GOOGLE_SERVICE_ACCOUNT_JSON=<paste JSON here>`
3. Update `main.py` to read from env var (see code below)

### Step 5: Deploy

Railway will automatically deploy. Check logs to verify it's running.

---

## ⚛️ Part 3: Deploy React Frontend to Vercel

### Step 1: Install Dependencies Locally (Optional Test)

```bash
cd frontend
npm install
```

### Step 2: Create Environment File

Create `frontend/.env`:

```env
VITE_GOOGLE_SHEET_ID=your_sheet_id_here
VITE_GOOGLE_API_KEY=your_google_api_key_here
VITE_REFRESH_INTERVAL=5000
```

### Step 3: Test Locally (Optional)

```bash
npm run dev
# Open http://localhost:5173
```

### Step 4: Deploy to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click **Add New** → **Project**
3. Import your GitHub repository
4. Configure:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### Step 5: Add Environment Variables in Vercel

In Vercel project settings → **Environment Variables**:

```
VITE_GOOGLE_SHEET_ID=your_sheet_id_here
VITE_GOOGLE_API_KEY=your_google_api_key_here
VITE_REFRESH_INTERVAL=5000
```

### Step 6: Deploy

Click **Deploy**. Vercel will build and deploy your frontend.

---

## ✅ Verification Checklist

### Backend (Railway)
- [ ] Railway deployment successful
- [ ] Logs show "🔗 Initializing SINGLE WebSocket connection"
- [ ] No errors in Railway logs
- [ ] Data appearing in Google Sheets

### Frontend (Vercel)
- [ ] Vercel deployment successful
- [ ] Dashboard loads without errors
- [ ] Data from Google Sheets displays correctly
- [ ] Auto-refresh working (every 5 seconds)
- [ ] Filters and charts working

---

## 🔍 Troubleshooting

### Backend Issues

**Problem**: "service_account.json not found"
- **Solution**: Upload the file to Railway or add as environment variable

**Problem**: "Permission denied" on Google Sheets
- **Solution**: Share the sheet with service account email

**Problem**: No data in Google Sheets
- **Solution**: Check if volume threshold is met (>20). Lower it in `main.py` for testing

### Frontend Issues

**Problem**: "Failed to fetch data"
- **Solution**: Verify Google Sheet is publicly readable and API key is correct

**Problem**: Blank dashboard
- **Solution**: Check browser console for errors. Verify environment variables in Vercel

**Problem**: Data not updating
- **Solution**: Check if backend is running on Railway and writing to sheets

---

## 📊 Monitoring

### Railway (Backend)
- Check logs: Railway Dashboard → Deployments → Logs
- Monitor resource usage: Railway Dashboard → Metrics

### Vercel (Frontend)
- Check deployment logs: Vercel Dashboard → Deployments
- Monitor analytics: Vercel Dashboard → Analytics

---

## 💰 Cost Estimate

| Service | Plan | Monthly Cost |
|---------|------|--------------|
| Railway | Hobby | $5 |
| Vercel | Free | $0 |
| Google Sheets API | Free | $0 |
| **Total** | | **$5/month** |

---

## 🎉 Success!

Once deployed:
- Backend runs 24/7 on Railway collecting options data
- Frontend hosted on Vercel displays live data
- Both read/write to the same Google Sheet

**Your Dashboard URL**: `https://your-project.vercel.app`

---

## 📞 Support

If you encounter issues:
1. Check Railway logs for backend errors
2. Check Vercel deployment logs for frontend errors
3. Verify Google Sheets permissions
4. Check browser console for JavaScript errors

