# 📊 NDX Options Monitor - Complete Solution

A full-stack application for monitoring NDX options in real-time with a beautiful dashboard.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Complete System                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────┐ │
│  │   Python     │      │   Google     │      │  React   │ │
│  │   Backend    │─────▶│   Sheets     │◀─────│Dashboard │ │
│  │  (Railway)   │      │   (Storage)  │      │ (Vercel) │ │
│  └──────────────┘      └──────────────┘      └──────────┘ │
│   WebSocket Data         Real-time DB         Live UI      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Features

### Backend (Python)
- ✅ Real-time WebSocket connection to Massive.com
- ✅ Monitors CALL and PUT options for NDX
- ✅ Filters data by volume threshold (>20)
- ✅ Automatically stores data in Google Sheets
- ✅ Runs 24/7 on Railway
- ✅ Auto-reconnection on failures

### Frontend (React Dashboard)
- ✅ Live data table with sorting and pagination
- ✅ Auto-refresh every 5 seconds
- ✅ Volume charts (CALL vs PUT)
- ✅ Smart filters (type, volume, strike price)
- ✅ Real-time statistics cards
- ✅ Mobile-responsive design
- ✅ Dark theme optimized for trading

## 📁 Project Structure

```
personal-trader/
├── main.py                   # Python WebSocket client
├── requirements.txt          # Python dependencies
├── railway.json              # Railway deployment config
├── Procfile                  # Process definition
├── service_account.json      # Google credentials (not in git)
│
├── frontend/                 # React Dashboard
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API services
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vercel.json
│
├── DEPLOYMENT_GUIDE.md      # Complete deployment guide
└── README.md                # This file
```

## 🎯 Quick Start

### Option 1: Deploy Everything (Recommended)

Follow the complete guide: **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**

### Option 2: Run Locally

#### Backend
```bash
pip install -r requirements.txt
python main.py
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📊 Data Structure

Google Sheet columns:
- Timestamp
- Symbol
- Option_Type (CALL/PUT)
- Strike_Price
- Close_Price
- Volume
- Accumulated_Volume
- High, Low, Open, VWAP

## 💰 Cost

| Service | Monthly Cost |
|---------|--------------|
| Railway (Backend) | $5 |
| Vercel (Frontend) | $0 (Free) |
| Google Sheets | $0 (Free) |
| **Total** | **$5/month** |

## 🔧 Configuration

### Backend (`main.py`)
- Volume threshold: >20 (line 115)
- Strike range: ±500 points
- Market hours: Until 3:00 PM CST

### Frontend (`.env`)
- Auto-refresh: 5 seconds
- Items per page: 50
- Chart: Top 20 strikes

## 🛠️ Tech Stack

### Backend
- Python 3.11
- Massive.com WebSocket API
- Google Sheets API
- gspread

### Frontend
- React 18
- Vite
- Recharts
- Google Sheets API

## 📝 License

ISC

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📞 Support

For deployment help, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)