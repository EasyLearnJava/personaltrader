import { useState, useEffect } from 'react'
import { timeAgo } from '../services/googleSheets'
import './Header.css'

function Header({ lastUpdate, onRefresh, loading }) {
  const [currentTime, setCurrentTime] = useState(new Date())

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date())
    }, 1000)

    return () => clearInterval(timer)
  }, [])

  const formatTime = (date) => {
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      timeZone: 'America/Chicago'
    })
  }

  return (
    <header className="header">
      <div className="header-content">
        <div className="header-left">
          <h1 className="header-title">
            <span className="header-icon">📊</span>
            NDX Options Monitor
          </h1>
          <div className="header-subtitle">
            Real-time options data from Google Sheets
          </div>
        </div>

        <div className="header-right">
          <div className="time-display">
            <div className="time-label">CST Time</div>
            <div className="time-value">{formatTime(currentTime)}</div>
          </div>

          <div className="status-display">
            <div className={`status-indicator ${loading ? 'loading' : 'live'}`}>
              <span className="status-dot"></span>
              {loading ? 'Updating...' : 'LIVE'}
            </div>
            {lastUpdate && (
              <div className="last-update">
                Updated {timeAgo(lastUpdate)}
              </div>
            )}
          </div>

          <button 
            onClick={onRefresh} 
            className="refresh-button"
            disabled={loading}
          >
            <span className={`refresh-icon ${loading ? 'spinning' : ''}`}>🔄</span>
            Refresh
          </button>
        </div>
      </div>
    </header>
  )
}

export default Header

