import { formatNumber } from '../services/googleSheets'
import './StatsCards.css'

function StatsCards({ stats }) {
  // Format countdown timer
  const formatCountdown = (seconds) => {
    if (seconds === null || seconds === undefined) return 'Loading...'
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const cards = [
    {
      title: 'Current Strike',
      value: stats.currentStrike ? `$${formatNumber(Math.round(stats.currentStrike))}` : 'Loading...',
      icon: '🎲',
      color: 'orange'
    },
    {
      title: 'Live NDX Price',
      value: stats.liveNdxPrice ? `$${formatNumber(Math.round(stats.liveNdxPrice))}` : 'Loading...',
      icon: '⚡',
      color: 'cyan'
    },
    {
      title: 'Next Refresh',
      value: formatCountdown(stats.nextRefreshSeconds),
      icon: '⏱️',
      color: 'teal'
    },
    {
      title: 'CALL Options',
      value: formatNumber(stats.callCount),
      icon: '📞',
      color: 'green'
    },
    {
      title: 'PUT Options',
      value: formatNumber(stats.putCount),
      icon: '📉',
      color: 'red'
    }
  ]

  return (
    <div className="stats-cards">
      {cards.map((card, index) => (
        <div key={index} className={`stat-card stat-card-${card.color} fade-in`}>
          <div className="stat-icon">{card.icon}</div>
          <div className="stat-content">
            <div className="stat-title">{card.title}</div>
            <div className="stat-value">{card.value}</div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default StatsCards

