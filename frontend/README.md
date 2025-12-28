# 📊 NDX Options Dashboard

Real-time dashboard for monitoring NDX options data collected by the Python backend.

## Features

- 📈 **Live Data Table** - Real-time options data from Google Sheets
- 🔄 **Auto-Refresh** - Updates every 5 seconds
- 📊 **Volume Charts** - Visual representation of CALL/PUT activity
- 🎯 **Smart Filters** - Filter by type, volume, and strike price
- 📱 **Mobile Responsive** - Works on all devices
- 🌙 **Dark Theme** - Trading-optimized UI

## Quick Start

### Install Dependencies

```bash
npm install
```

### Configure Environment

Create `.env` file:

```env
VITE_GOOGLE_SHEET_ID=your_sheet_id_here
VITE_GOOGLE_API_KEY=your_google_api_key_here
VITE_REFRESH_INTERVAL=5000
```

### Run Development Server

```bash
npm run dev
```

Open [http://localhost:5173](http://localhost:5173)

### Build for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Deployment

See [DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md) for complete deployment instructions.

### Deploy to Vercel

1. Push code to GitHub
2. Import project in Vercel
3. Set root directory to `frontend`
4. Add environment variables
5. Deploy!

## Technology Stack

- **React 18** - UI framework
- **Vite** - Build tool
- **Recharts** - Charting library
- **Google Sheets API** - Data source

## License

ISC

