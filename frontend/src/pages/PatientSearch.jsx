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
  const [showUpload, setShowUpload] = useState(false)

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
        <div className="search-layout">
          <div className="search-main">
            <div className="search-container">
              <div className="search-header">
                <div>
                  <h2 className="panel-title">Find a Patient</h2>
                  <p className="panel-subtitle-muted">Use ID, name, or barcode to locate a record quickly.</p>
                </div>
                <button
                  type="button"
                  onClick={() => setShowUpload(!showUpload)}
                  className="btn-secondary"
                >
                  {showUpload ? 'Hide Upload' : 'Upload Records'}
                </button>
              </div>

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

              {showUpload && (
                <div className="upload-panel">
                  <h3 className="panel-title">Upload Patient Records</h3>
                  <p className="panel-subtitle-muted">Drag and drop medical documents to add new patient records.</p>
                  <FileUpload token={token} patientId="NEW_PATIENT" />
                </div>
              )}

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
          </div>

          <div className="search-side">
            <div className="panel-card">
              <h3 className="panel-title">Quick Start (Local)</h3>
              <p className="panel-subtitle-muted">Start backend and frontend in two terminals.</p>
              <div className="code-block">
                <span className="code-title">Terminal 1 (Backend)</span>
                <code>cd backend</code>
                <code>venv\Scripts\activate</code>
                <code>pip install -r requirements.txt</code>
                <code>python main_aiohttp.py</code>
              </div>
              <div className="code-block">
                <span className="code-title">Terminal 2 (Frontend)</span>
                <code>cd frontend</code>
                <code>npm install</code>
                <code>npm run dev</code>
              </div>
              <div className="panel-note">
                Open: <strong>http://localhost:5173</strong>
              </div>
            </div>

            <div className="panel-card">
              <h3 className="panel-title">Common Tasks</h3>
              <div className="task-list">
                <div className="task-item">Search a patient by ID or name.</div>
                <div className="task-item">Upload documents to create new records.</div>
                <div className="task-item">Open a patient and view AI Summary.</div>
                <div className="task-item">Enable Emergency Mode in critical cases.</div>
              </div>
            </div>

            <div className="panel-card">
              <h3 className="panel-title">Demo Patient IDs</h3>
              <div className="demo-list">
                <div className="demo-item">
                  <strong>PAT_987654</strong> — John Smith (64M)
                </div>
                <div className="demo-item">
                  <strong>PAT_654321</strong> — Mary Johnson (69F)
                </div>
              </div>
            </div>

            <div className="panel-card">
              <h3 className="panel-title">Optional Services</h3>
              <div className="panel-note">
                PostgreSQL, OCR, and Fanar LLM can be enabled via <strong>backend/.env</strong>.
              </div>
              <div className="code-block">
                <code>DATABASE_URL=postgresql://user:password@localhost:5432/clinix</code>
                <code>LLM_PROVIDER=fanar</code>
                <code>FANAR_LLM_URL=...</code>
              </div>
            </div>
          </div>
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
