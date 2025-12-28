import { useMemo } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { parseStrikePrice } from '../services/googleSheets'
import './VolumeChart.css'

function VolumeChart({ data }) {
  const chartData = useMemo(() => {
    // Group by strike price and option type
    const grouped = {}

    data.forEach(row => {
      const strike = row.Strike_Price
      if (!strike) return

      if (!grouped[strike]) {
        grouped[strike] = {
          strike,
          strikeNum: parseStrikePrice(strike),
          CALL: 0,
          PUT: 0
        }
      }

      const volume = parseInt(row.Volume) || 0
      if (row.Option_Type === 'CALL') {
        grouped[strike].CALL += volume
      } else if (row.Option_Type === 'PUT') {
        grouped[strike].PUT += volume
      }
    })

    // Convert to array and sort by strike price
    return Object.values(grouped)
      .sort((a, b) => a.strikeNum - b.strikeNum)
      .slice(0, 20) // Show top 20 strikes
  }, [data])

  if (chartData.length === 0) {
    return null
  }

  return (
    <div className="volume-chart-container">
      <div className="chart-header">
        <h2>📊 Volume by Strike Price</h2>
        <p className="chart-subtitle">Top 20 most active strikes</p>
      </div>

      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#2d3748" />
          <XAxis 
            dataKey="strike" 
            angle={-45}
            textAnchor="end"
            height={80}
            tick={{ fill: '#9ca3af', fontSize: 12 }}
          />
          <YAxis tick={{ fill: '#9ca3af', fontSize: 12 }} />
          <Tooltip 
            contentStyle={{
              backgroundColor: '#1e2139',
              border: '2px solid #2d3748',
              borderRadius: '8px',
              color: '#e4e6eb'
            }}
          />
          <Legend 
            wrapperStyle={{ paddingTop: '20px' }}
            iconType="circle"
          />
          <Bar dataKey="CALL" fill="#10b981" name="CALL Volume" />
          <Bar dataKey="PUT" fill="#ef4444" name="PUT Volume" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export default VolumeChart

