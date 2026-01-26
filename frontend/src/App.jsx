import { useState } from 'react'
import './App.css'
import Login from './pages/Login'
import PatientSearch from './pages/PatientSearch'
import PatientSnapshot from './pages/PatientSnapshot'
import EmergencyMode from './pages/EmergencyMode'
import AISummary from './pages/AISummary'
import FileBrowser from './pages/FileBrowser'

const API_BASE = 'http://localhost:8000'

function App() {
  const [currentPage, setCurrentPage] = useState('login')
  const [authToken, setAuthToken] = useState(null)
  const [userInfo, setUserInfo] = useState(null)
  const [selectedPatient, setSelectedPatient] = useState(null)
  const [showFileBrowser, setShowFileBrowser] = useState(false)

  const handleLogin = async (credentials) => {
    try {
      const response = await fetch(`${API_BASE}/api/v1/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials)
      })

      if (!response.ok) {
        throw new Error('Login failed')
      }

      const data = await response.json()
      setAuthToken(data.token)
      setUserInfo(data)
      setCurrentPage('search')
      return { success: true }
    } catch (error) {
      return { success: false, error: error.message }
    }
  }

  const handleLogout = async () => {
    if (authToken) {
      try {
        await fetch(`${API_BASE}/api/v1/auth/logout`, {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${authToken}` }
        })
      } catch (error) {
        console.error('Logout error:', error)
      }
    }
    setAuthToken(null)
    setUserInfo(null)
    setSelectedPatient(null)
    setCurrentPage('login')
  }

  const handlePatientSelect = (patient) => {
    setSelectedPatient(patient)
    setCurrentPage('snapshot')
  }

  const navigateTo = (page) => {
    setCurrentPage(page)
  }

  const renderPage = () => {
    switch (currentPage) {
      case 'login':
        return <Login onLogin={handleLogin} />
      
      case 'search':
        return (
          <PatientSearch
            token={authToken}
            userInfo={userInfo}
            onPatientSelect={handlePatientSelect}
            onLogout={handleLogout}
          />
        )
      
      case 'snapshot':
        return (
          <PatientSnapshot
            token={authToken}
            userInfo={userInfo}
            patient={selectedPatient}
            onBack={() => navigateTo('search')}
            onEmergencyMode={() => navigateTo('emergency')}
            onViewAISummary={() => navigateTo('ai-summary')}
            onLogout={handleLogout}
          />
        )
      
      case 'emergency':
        return (
          <EmergencyMode
            token={authToken}
            patient={selectedPatient}
            onExit={() => navigateTo('snapshot')}
          />
        )
      
      case 'ai-summary':
        return (
          <AISummary
            token={authToken}
            patient={selectedPatient}
            onBack={() => navigateTo('snapshot')}
            onOpenFileBrowser={() => setShowFileBrowser(true)}
          />
        )
      
      default:
        return <Login onLogin={handleLogin} />
    }
  }

  const handleFileSelect = (file) => {
    console.log('Selected file:', file)
    setShowFileBrowser(false)
  }

  return (
    <div className="app">
      {renderPage()}
      {showFileBrowser && authToken && (
        <FileBrowser
          token={authToken}
          onFileSelect={handleFileSelect}
          onClose={() => setShowFileBrowser(false)}
        />
      )}
    </div>
  )
}

export default App
