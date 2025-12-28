import { useState } from 'react'
import { formatNumber } from '../services/googleSheets'
import './DataTable.css'

function DataTable({ data, loading }) {
  const [sortField, setSortField] = useState('Timestamp')
  const [sortDirection, setSortDirection] = useState('desc')
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 50

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')
    } else {
      setSortField(field)
      setSortDirection('desc')
    }
  }

  const sortedData = [...data].sort((a, b) => {
    let aVal = a[sortField]
    let bVal = b[sortField]

    // Handle numeric fields
    if (['Volume', 'Accumulated_Volume', 'Close_Price', 'High', 'Low', 'Open', 'VWAP'].includes(sortField)) {
      aVal = parseFloat(aVal) || 0
      bVal = parseFloat(bVal) || 0
    }

    if (aVal < bVal) return sortDirection === 'asc' ? -1 : 1
    if (aVal > bVal) return sortDirection === 'asc' ? 1 : -1
    return 0
  })

  const totalPages = Math.ceil(sortedData.length / itemsPerPage)
  const startIndex = (currentPage - 1) * itemsPerPage
  const paginatedData = sortedData.slice(startIndex, startIndex + itemsPerPage)

  if (loading && data.length === 0) {
    return (
      <div className="table-container">
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Loading data...</p>
        </div>
      </div>
    )
  }

  if (data.length === 0) {
    return (
      <div className="table-container">
        <div className="empty-state">
          <span className="empty-icon">📭</span>
          <h3>No Data Available</h3>
          <p>Waiting for options data from the backend...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="table-container">
      <div className="table-header">
        <h2>📊 Live Options Data</h2>
        <div className="table-info">
          Showing {startIndex + 1}-{Math.min(startIndex + itemsPerPage, sortedData.length)} of {sortedData.length} trades
        </div>
      </div>

      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              <th onClick={() => handleSort('Timestamp')}>
                Time {sortField === 'Timestamp' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('Option_Type')}>
                Type {sortField === 'Option_Type' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('Strike_Price')}>
                Strike {sortField === 'Strike_Price' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('Close_Price')}>
                Price {sortField === 'Close_Price' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('Volume')}>
                Volume {sortField === 'Volume' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('Accumulated_Volume')}>
                Total Vol {sortField === 'Accumulated_Volume' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('High')}>
                High {sortField === 'High' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('Low')}>
                Low {sortField === 'Low' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
            </tr>
          </thead>
          <tbody>
            {paginatedData.map((row, index) => (
              <tr key={index} className="fade-in">
                <td className="time-cell">
                  {row.Timestamp ? new Date(row.Timestamp).toLocaleTimeString() : '-'}
                </td>
                <td>
                  <span className={`type-badge ${row.Option_Type?.toLowerCase()}`}>
                    {row.Option_Type === 'CALL' ? '📞' : '📉'} {row.Option_Type}
                  </span>
                </td>
                <td className="strike-cell">{row.Strike_Price}</td>
                <td className="price-cell">${parseFloat(row.Close_Price || 0).toFixed(2)}</td>
                <td className="volume-cell">
                  <span className={`volume-badge ${parseInt(row.Volume) > 100 ? 'high' : ''}`}>
                    {formatNumber(row.Volume)}
                  </span>
                </td>
                <td>{formatNumber(row.Accumulated_Volume)}</td>
                <td className="price-cell">${parseFloat(row.High || 0).toFixed(2)}</td>
                <td className="price-cell">${parseFloat(row.Low || 0).toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div className="pagination">
          <button
            onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
            disabled={currentPage === 1}
            className="page-btn"
          >
            ← Previous
          </button>
          <span className="page-info">
            Page {currentPage} of {totalPages}
          </span>
          <button
            onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
            disabled={currentPage === totalPages}
            className="page-btn"
          >
            Next →
          </button>
        </div>
      )}
    </div>
  )
}

export default DataTable

