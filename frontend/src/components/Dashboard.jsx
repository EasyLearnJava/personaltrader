import { useState, useMemo } from 'react'
import Header from './Header'
import StatsCards from './StatsCards'
import Filters from './Filters'
import DataTable from './DataTable'
import VolumeChart from './VolumeChart'
import './Dashboard.css'

function Dashboard({ data, loading, error, lastUpdate, currentStrike, liveNdxPrice, nextRefreshSeconds, onRefresh }) {
  const [filterType, setFilterType] = useState('ALL')
  const [minVolume, setMinVolume] = useState(0)
  const [searchStrike, setSearchStrike] = useState('')

  // Filter data based on user selections
  const filteredData = useMemo(() => {
    return data.filter(row => {
      // Filter by option type
      if (filterType !== 'ALL' && row.Option_Type !== filterType) {
        return false
      }

      // Filter by minimum volume
      const volume = parseInt(row.Volume) || 0
      if (volume < minVolume) {
        return false
      }

      // Filter by strike price search
      if (searchStrike) {
        // Remove all non-numeric characters from both the search and the strike price
        const cleanSearch = searchStrike.replace(/[^0-9]/g, '')
        const cleanStrike = row.Strike_Price?.replace(/[^0-9]/g, '') || ''
        if (!cleanStrike.includes(cleanSearch)) {
          return false
        }
      }

      return true
    })
  }, [data, filterType, minVolume, searchStrike])

  // Calculate statistics
  const stats = useMemo(() => {
    const totalTrades = filteredData.length
    const uniqueStrikes = new Set(filteredData.map(r => r.Strike_Price)).size
    const totalVolume = filteredData.reduce((sum, r) => sum + (parseInt(r.Volume) || 0), 0)
    const avgVolume = totalTrades > 0 ? Math.floor(totalVolume / totalTrades) : 0

    const callCount = filteredData.filter(r => r.Option_Type === 'CALL').length
    const putCount = filteredData.filter(r => r.Option_Type === 'PUT').length

    return {
      totalTrades,
      uniqueStrikes,
      avgVolume,
      totalVolume,
      callCount,
      putCount,
      currentStrike,
      liveNdxPrice,
      nextRefreshSeconds,
      lastUpdate
    }
  }, [filteredData, currentStrike, liveNdxPrice, nextRefreshSeconds, lastUpdate])

  if (error) {
    return (
      <div className="dashboard">
        <Header lastUpdate={lastUpdate} onRefresh={onRefresh} />
        <div className="error-container">
          <div className="error-message">
            <span className="error-icon">⚠️</span>
            <h2>Error Loading Data</h2>
            <p>{error}</p>
            <button onClick={onRefresh} className="retry-button">
              Retry
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="dashboard">
      <Header lastUpdate={lastUpdate} onRefresh={onRefresh} loading={loading} />
      
      <div className="dashboard-content">
        <StatsCards stats={stats} />
        
        <Filters
          filterType={filterType}
          setFilterType={setFilterType}
          minVolume={minVolume}
          setMinVolume={setMinVolume}
          searchStrike={searchStrike}
          setSearchStrike={setSearchStrike}
        />

        <div className="charts-section">
          <VolumeChart data={filteredData} />
        </div>

        <DataTable data={filteredData} loading={loading} />
      </div>
    </div>
  )
}

export default Dashboard

