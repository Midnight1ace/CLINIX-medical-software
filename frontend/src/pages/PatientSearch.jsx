import { useState } from 'react'
import FileUpload from './FileUpload'
import FileBrowser from './FileBrowser'

const API_BASE = 'http://localhost:8000'

function PatientSearch({ token, userInfo, onPatientSelect, onLogout }) {
  const [searchMethod, setSearchMethod] = useState('PATIENT_ID')
  const [searchValue, setSearchValue] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [showFileBrowser, setShowFileBrowser] = useState(false)

  const handleSearch = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await fetch(
        `${API_BASE}/api/v1/patients/search?method=${searchMethod}&value=${encodeURIComponent(searchValue)}`,
        {
          headers: { 'Authorization': `Bearer ${token}` }
        }
      )

      if (!response.ok) {
        throw new Error('Search failed')
      }

      const data = await response.json()
      setSearchResults(data.results)
    } catch (err) {
      setError('Search failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleSelectPatient = async (patientId) => {
    try {
      const response = await fetch(
        `${API_BASE}/api/v1/patients/${patientId}/snapshot`,
        {
          headers: { 'Authorization': `Bearer ${token}` }
        }
      )

      if (!response.ok) {
        throw new Error('Failed to load patient data')
      }

      const data = await response.json()
      onPatientSelect(data)
    } catch (err) {
      setError('Failed to load patient data')
    }
  }

  return (
    <div className="page-container">
      <header className="page-header">
        <div className="header-content">
          <h1>Patient Search</h1>
          <div className="user-info">
            <span>{userInfo.name} ({userInfo.role})</span>
            <button onClick={() => setShowFileBrowser(true)} className="btn-secondary">📁 Browse Files</button>
            <button onClick={onLogout} className="btn-secondary">Logout</button>
          </div>
        </div>
      </header>

      <div className="content">
        <div className="search-container">
          <form onSubmit={handleSearch} className="search-form">
            <div className="form-row">
              <div className="form-group">
                <label>Search Method</label>
                <select 
                  value={searchMethod} 
                  onChange={(e) => setSearchMethod(e.target.value)}
                  className="form-select"
                >
                  <option value="PATIENT_ID">Patient ID</option>
                  <option value="NATIONAL_ID">National ID</option>
                  <option value="PARTIAL_NAME">Name</option>
                  <option value="QR_CODE">QR Code</option>
                  <option value="BARCODE">Barcode</option>
                </select>
              </div>

              <div className="form-group flex-grow">
                <label>Search Value</label>
                <input
                  type="text"
                  value={searchValue}
                  onChange={(e) => setSearchValue(e.target.value)}
                  placeholder="Enter search term"
                  required
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label>&nbsp;</label>
                <button type="submit" className="btn-primary" disabled={loading}>
                  {loading ? 'Searching...' : 'Search'}
                </button>
              </div>
            </div>
          </form>

          {error && <div className="error-message">{error}</div>}

          <div className="demo-info">
            <p><strong>Demo Patient IDs:</strong></p>
            <p>PAT_987654 - John Smith (64M)</p>
            <p>PAT_654321 - Mary Johnson (69F)</p>
          </div>

          {searchResults.length > 0 && (
            <div className="search-results">
              <h2>Search Results ({searchResults.length})</h2>
              {searchResults.map((result) => (
                <div key={result.patient_id} className="result-card">
                  <div className="result-info">
                    <h3>{result.name}</h3>
                    <p>Patient ID: {result.patient_id}</p>
                    <p>DOB: {result.date_of_birth} (Age: {result.age})</p>
                    <p>Gender: {result.gender}</p>
                    <p className="match-score">Match: {(result.match_score * 100).toFixed(0)}% - {result.match_reason}</p>
                  </div>
                  <button 
                    onClick={() => handleSelectPatient(result.patient_id)}
                    className="btn-primary"
                  >
                    Select Patient
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        <div style={{ marginTop: '30px', background: '#e8f4f8', padding: '20px', borderRadius: '12px', border: '3px solid #3498db' }}>
          <h3 style={{ fontSize: '20px', color: '#2c3e50', marginBottom: '10px' }}>📄 Upload Patient Records</h3>
          <p style={{ fontSize: '14px', color: '#7f8c8d', marginBottom: '20px' }}>Drag and drop medical documents to add new patient records to the system</p>
          <FileUpload token={token} patientId="NEW_PATIENT" />
        </div>
      </div>

      {showFileBrowser && (
        <FileBrowser
          token={token}
          onFileSelect={() => setShowFileBrowser(false)}
          onClose={() => setShowFileBrowser(false)}
        />
      )}
    </div>
  )
}

export default PatientSearch
