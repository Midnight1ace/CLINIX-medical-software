import React from 'react'
import axios from 'axios'

export default function Login({ onLogin }) {
  const [username, setUsername] = React.useState('dr_johnson')
  const [password, setPassword] = React.useState('demo123')
  const [error, setError] = React.useState('')
  const [loading, setLoading] = React.useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await axios.post('http://localhost:8000/api/v1/auth/login', {
        username,
        password,
        hospital_id: 'HOSP_001'
      })
      onLogin(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <h1>🏥 AI-Patient Record Intelligence</h1>
        <p className="logo-subtitle">Doctor-first clinical clarity</p>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Username:</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="e.g., dr_johnson"
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label>Password:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="password"
              disabled={loading}
            />
          </div>

          {error && <div className="error-message">❌ {error}</div>}

          <button type="submit" disabled={loading} className="btn-primary">
            {loading ? 'Logging in...' : 'LOGIN'}
          </button>
        </form>

        <div className="demo-credentials">
          <h3>Demo Credentials:</h3>
          <p><strong>Doctors:</strong> dr_johnson / demo123</p>
          <p><strong>Doctors:</strong> dr_hassan / demo123</p>
          <p><strong>Pharmacist:</strong> pharm_smith / demo123</p>
          <p><em>Password: demo123 (all users)</em></p>
        </div>

        <div className="info-box">
          <p>⏱️ Session expires: 15 minutes</p>
          <p>📋 Try searching for: PAT_987654</p>
        </div>
      </div>
    </div>
  )
}
