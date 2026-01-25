import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/store/authStore'

export default function Header() {
  const navigate = useNavigate()
  const { user, logout } = useAuthStore()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className="app-header">
      <div className="header-content">
        <div className="logo">
          <h1>AI Patient Records</h1>
        </div>
        
        <nav className="header-nav">
          <button onClick={() => navigate('/search')}>Search</button>
          {user && <span className="user-info">{user.first_name} {user.last_name}</span>}
          <button onClick={handleLogout} className="logout-btn">Logout</button>
        </nav>
      </div>
    </header>
  )
}
