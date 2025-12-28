import './Filters.css'

function Filters({ filterType, setFilterType, minVolume, setMinVolume, searchStrike, setSearchStrike }) {
  return (
    <div className="filters">
      <div className="filters-section">
        <label className="filter-label">Option Type</label>
        <div className="filter-buttons">
          <button
            className={`filter-btn ${filterType === 'ALL' ? 'active' : ''}`}
            onClick={() => setFilterType('ALL')}
          >
            All
          </button>
          <button
            className={`filter-btn ${filterType === 'CALL' ? 'active' : ''}`}
            onClick={() => setFilterType('CALL')}
          >
            📞 CALL
          </button>
          <button
            className={`filter-btn ${filterType === 'PUT' ? 'active' : ''}`}
            onClick={() => setFilterType('PUT')}
          >
            📉 PUT
          </button>
        </div>
      </div>

      <div className="filters-section">
        <label className="filter-label">
          Min Volume: {minVolume}
        </label>
        <input
          type="range"
          min="0"
          max="500"
          step="10"
          value={minVolume}
          onChange={(e) => setMinVolume(parseInt(e.target.value))}
          className="volume-slider"
        />
      </div>

      <div className="filters-section">
        <label className="filter-label">Search Strike Price</label>
        <input
          type="text"
          placeholder="e.g., 25650"
          value={searchStrike}
          onChange={(e) => setSearchStrike(e.target.value)}
          className="search-input"
        />
      </div>

      <div className="filters-section">
        <button
          className="clear-btn"
          onClick={() => {
            setFilterType('ALL')
            setMinVolume(0)
            setSearchStrike('')
          }}
        >
          Clear Filters
        </button>
      </div>
    </div>
  )
}

export default Filters

