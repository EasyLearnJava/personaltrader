/**
 * Google Sheets API Service
 * Fetches data from the Google Sheet where Python backend writes data
 */

const SHEET_ID = import.meta.env.VITE_GOOGLE_SHEET_ID || 'YOUR_SHEET_ID'
const API_KEY = import.meta.env.VITE_GOOGLE_API_KEY || 'YOUR_API_KEY'
const SHEET_NAME = 'Sheet1' // Change if your sheet has a different name

/**
 * Fetch data from Google Sheets using the Sheets API v4
 * Make sure the Google Sheet is publicly readable or API key has access
 */
export async function fetchGoogleSheetData() {
  try {
    const url = `https://sheets.googleapis.com/v4/spreadsheets/${SHEET_ID}/values/${SHEET_NAME}?key=${API_KEY}`
    
    const response = await fetch(url)
    
    if (!response.ok) {
      throw new Error(`Failed to fetch data: ${response.statusText}`)
    }
    
    const result = await response.json()
    const rows = result.values || []
    
    if (rows.length === 0) {
      return []
    }
    
    // First row is headers
    const headers = rows[0]
    
    // Convert rows to objects
    const data = rows.slice(1).map(row => {
      const obj = {}
      headers.forEach((header, index) => {
        obj[header] = row[index] || ''
      })
      return obj
    })
    
    // Sort by timestamp (newest first)
    return data.reverse()
    
  } catch (error) {
    console.error('Error fetching Google Sheets data:', error)
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

