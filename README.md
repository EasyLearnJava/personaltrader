# 📊 NDX Options Monitor - Render.com All-in-One

Real-time NDX options monitoring with Python WebSocket backend and React dashboard - **single deployment on Render.com**.

## ✨ Features

- 🔄 Real-time WebSocket data streaming
- 📊 Dynamic strike adjustment (every 10 mins)
- 📈 Beautiful React dashboard
- 📝 Google Sheets integration
- 🎯 Smart reconnection (>100 point changes)
- 🌐 Single Render.com deployment

## 🏗️ Architecture

```
Render.com Web Service:
├── Node.js (Port 3000) → Serves React Frontend
└── Python Backend → WebSocket Data Collector
```

**Data Flow:** `Polygon.io → Python → Google Sheets → React Dashboard`

## 📁 Project Structure

```
├── backend/
│   ├── main.py              # Python WebSocket client
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/                 # React components
│   └── package.json         # Frontend dependencies
├── server.js                # Express server
├── package.json             # Root dependencies
└── render.yaml              # Render configuration
```

## 🚀 Quick Deploy to Render.com

### Prerequisites
- GitHub account
- Render.com account (free tier available)
- Google Cloud with Sheets API enabled
- Service Account JSON credentials

### Step 1: Prepare Google Sheets

1. Create Google Sheet named `Dataintab`
2. Enable Google Sheets API in Google Cloud Console
3. Create Service Account and download JSON
4. Share sheet with service account email (Editor permissions)

📖 See [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md) for details.

### Step 2: Deploy to Render

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy to Render.com"
   git push origin main
   ```

2. **Create Render Service**
   - Go to [render.com](https://render.com)
   - Click **New +** → **Web Service**
   - Connect repository: `EasyLearnJava/personaltrader`

3. **Configure Service**
   - **Name**: `ndx-options-monitor`
   - **Runtime**: `Python 3`
   - **Build Command**:
     ```
     pip install -r backend/requirements.txt && cd frontend && npm install && npm run build && cd .. && npm install
     ```
   - **Start Command**:
     ```
     node server.js
     ```

4. **Add Environment Variables**

   In Render dashboard, add these environment variables:

   ```
   POLYGON_API_KEY=wsWMG2p9vhDDjVxAHSRz6qbSR_a7B1wL
   GOOGLE_SHEET_NAME=Dataintab
   GOOGLE_SERVICE_ACCOUNT_JSON=<paste entire JSON content>
   ```

   **Important:** Copy the entire content of your `service_account.json` file and paste as one line.

5. **Deploy!**
   - Click **Create Web Service**
   - Wait 5-10 minutes for first deployment
   - Access at: `https://ndx-options-monitor.onrender.com`

## 💰 Cost

| Service | Plan | Cost |
|---------|------|------|
| Render.com | Starter | $7/month |
| Google Sheets | Free | $0 |
| **Total** | | **$7/month** |

*Free tier available but spins down after inactivity. Starter plan recommended for 24/7 operation.*

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `POLYGON_API_KEY` | Polygon.io API key | ✅ Yes |
| `GOOGLE_SHEET_NAME` | Google Sheet name | ✅ Yes |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Service account JSON | ✅ Yes |

### Backend Settings

- Volume threshold: `>20`
- Strike check: Every `10 minutes`
- Reconnection: When strike changes `>100 points`
- Market hours: Until `3:00 PM CST`

## 📊 Dashboard Features

- ✅ Live data table with sorting & pagination
- ✅ Real-time statistics cards
- ✅ Volume charts (CALL vs PUT)
- ✅ Smart filters (type, volume, strike)
- ✅ Auto-refresh every 5 seconds
- ✅ Mobile-responsive design
- ✅ Dark theme for trading

## 🛠️ Local Development

```bash
# Install all dependencies
npm install
cd frontend && npm install && cd ..
pip install -r backend/requirements.txt

# Start server (runs both frontend and backend)
npm start
```

Access at: `http://localhost:3000`

## 🔍 Monitoring

View logs in Render dashboard to see:
- Python backend startup
- WebSocket connections
- Data collection
- Strike adjustments

## 🛠️ Tech Stack

- **Backend**: Python 3.11, Polygon.io API, Google Sheets API
- **Frontend**: React 18, Vite, Recharts
- **Server**: Node.js 18, Express.js
- **Deployment**: Render.com

## 📝 License

ISC