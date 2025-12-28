import { useState, useEffect } from 'react'
import Dashboard from './components/Dashboard'
import { fetchGoogleSheetData } from './services/googleSheets'
import './App.css'

function App() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [lastUpdate, setLastUpdate] = useState(null)

  const loadData = async () => {
    try {
      setLoading(true)
      const sheetData = await fetchGoogleSheetData()
      setData(sheetData)
      setLastUpdate(new Date())
      setError(null)
    } catch (err) {
      console.error('Error loading data:', err)
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
    
    // Auto-refresh every 5 seconds
    const interval = setInterval(loadData, 5000)
    
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="app">
      <Dashboard 
        data={data}
        loading={loading}
        error={error}
        lastUpdate={lastUpdate}
        onRefresh={loadData}
      />
    </div>
  )
}

export default App

