import { formatNumber } from '../services/googleSheets'
import './StatsCards.css'

function StatsCards({ stats }) {
  const cards = [
    {
      title: 'Total Trades',
      value: formatNumber(stats.totalTrades),
      icon: '📈',
      color: 'blue'
    },
    {
      title: 'Active Strikes',
      value: formatNumber(stats.uniqueStrikes),
      icon: '🎯',
      color: 'purple'
    },
    {
      title: 'Avg Volume',
      value: formatNumber(stats.avgVolume),
      icon: '📊',
      color: 'green'
    },
    {
      title: 'Total Volume',
      value: formatNumber(stats.totalVolume),
      icon: '💹',
      color: 'yellow'
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

