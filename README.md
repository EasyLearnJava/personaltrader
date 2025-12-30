# 📊 NDX Options Monitor - Real-Time Dashboard

Real-time NDX options monitoring with Python WebSocket backend and React dashboard - **single deployment on Render.com**.

## ✨ Features

- 🔄 Real-time WebSocket data streaming from Polygon.io
- 📊 Dynamic strike adjustment (every 10 mins)
- 📈 Beautiful React dashboard with live updates
- 💾 In-memory data storage (last 1000 records)
- 🎯 Smart reconnection (>100 point changes)
- 🌐 Single Render.com deployment
- 🚀 No external database required

## 🏗️ Architecture

```text
Render.com Web Service:
├── Node.js Express (Port 3000)
│   ├── Serves React Frontend
│   └── Proxies API requests
└── Python Flask (Port 5000)
    ├── WebSocket Client (Polygon.io)
    ├── In-Memory Data Store
    └── REST API (/api/options)
```

**Data Flow:** `Polygon.io → Python WebSocket → In-Memory Storage → Flask API → React Dashboard`

## 📁 Project Structure

```text
├── backend/
│   ├── main.py              # Python WebSocket + Flask API
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/                 # React components
│   └── package.json         # Frontend dependencies
├── server.js                # Express server (proxy)
├── package.json             # Root dependencies
└── render.yaml              # Render configuration
```

## 🚀 Quick Deploy to Render.com

### Prerequisites

- GitHub account
- Render.com account (free tier available)
- Polygon.io API key

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Deploy to Render.com"
git push origin main
```

### Step 2: Deploy to Render

1. **Create Render Service**
   - Go to [render.com](https://render.com)
   - Click **New +** → **Web Service**
   - Connect repository: `EasyLearnJava/personaltrader`

2. **Configure Service**
   - **Name**: `ndx-options-monitor`
   - **Runtime**: `Python 3`
   - **Build Command**:
     ```bash
     pip install -r backend/requirements.txt && cd frontend && npm install && npm run build && cd .. && npm install
     ```
   - **Start Command**:
     ```bash
     node server.js
     ```

3. **Add Environment Variable**
   - **Key**: `POLYGON_API_KEY`
   - **Value**: Your Polygon.io API key

4. **Deploy!** 🎉

## 🌐 API Endpoints

- `GET /api/options` - Get all options data
- `GET /api/health` - Health check

## 💻 Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- Polygon.io API key

### Setup

1. **Clone repository**
   ```bash
   git clone https://github.com/EasyLearnJava/personaltrader.git
   cd TApp
   ```

2. **Install dependencies**
   ```bash
   # Python dependencies
   pip install -r backend/requirements.txt
   
   # Node.js dependencies
   npm install
   cd frontend && npm install && cd ..
   ```

3. **Set environment variable**
   ```bash
   export POLYGON_API_KEY=your_api_key_here
   ```

4. **Build frontend**
   ```bash
   cd frontend && npm run build && cd ..
   ```

5. **Run the app**
   ```bash
   node server.js
   ```

6. **Open browser**
   - Frontend: http://localhost:3000
   - API: http://localhost:5000/api/options

## 📊 How It Works

1. **Python Backend** connects to Polygon.io WebSocket
2. **Real-time data** flows in for NDX options
3. **Data stored** in memory (last 1000 records)
4. **Flask API** serves data at `/api/options`
5. **React Dashboard** fetches and displays data
6. **Auto-refresh** every 5 seconds

## 💰 Cost

- **Render.com Starter**: $7/month (24/7 uptime)
- **Polygon.io**: Free tier available
- **Total**: **$7/month**

## 📖 Documentation

- [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) - Detailed deployment guide
- [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md) - Architecture summary
- [RENDER_API_SETUP.md](RENDER_API_SETUP.md) - Render API integration

## 🤝 Contributing

Pull requests welcome! For major changes, please open an issue first.

## 📄 License

ISC

