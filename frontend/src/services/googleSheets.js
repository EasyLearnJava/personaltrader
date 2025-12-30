/**
 * Options Data API Service
 * Fetches real-time options data from the Python backend API
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

/**
 * Fetch options data from the backend API
 */
export async function fetchGoogleSheetData() {
  try {
    const url = `${API_BASE_URL}/options`

    const response = await fetch(url)

    if (!response.ok) {
      throw new Error(`Failed to fetch data: ${response.statusText}`)
    }

    const result = await response.json()

    // Return data array (already in object format from backend)
    return result.data || []

  } catch (error) {
    console.error('Error fetching options data:', error)
    throw error
  }
}

/**
 * Fetch health status from backend
 */
export async function fetchHealthStatus() {
  try {
    const url = `${API_BASE_URL}/health`
    const response = await fetch(url)

    if (!response.ok) {
      throw new Error(`Health check failed: ${response.statusText}`)
    }

    return await response.json()
  } catch (error) {
    console.error('Error fetching health status:', error)
    throw error
  }
}

/**
 * Parse strike price from formatted string like "$25,650"
 */
export function parseStrikePrice(strikeStr) {
  if (!strikeStr) return 0
  return parseInt(strikeStr.replace(/[$,]/g, ''))
}

/**
 * Format number with commas
 */
export function formatNumber(num) {
  if (!num) return '0'
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

/**
 * Calculate time ago from timestamp
 */
export function timeAgo(timestamp) {
  if (!timestamp) return 'Unknown'
  
  const now = new Date()
  const then = new Date(timestamp)
  const seconds = Math.floor((now - then) / 1000)
  
  if (seconds < 60) return `${seconds}s ago`
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`
  return `${Math.floor(seconds / 86400)}d ago`
}

