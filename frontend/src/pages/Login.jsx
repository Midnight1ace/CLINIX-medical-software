import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import LanguageSelector from '../components/LanguageSelector'

function Login({ onLogin }) {
  const { t } = useTranslation()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    const result = await onLogin({
      username,
      password,
      hospital_id: 'HOSP_001'
    })

    setLoading(false)

    if (!result.success) {
      setError(t('login.invalidCredentials'))
    }
  }

  return (
    <div className="login-container">
      <div className="language-selector-top">
        <LanguageSelector />
      </div>
      <div className="login-card">
        <div className="login-header">
          <h1>{t('app.title')}</h1>
          <p>{t('app.subtitle')}</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="username">{t('login.username')}</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder={t('login.usernamePlaceholder')}
              required
              autoFocus
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">{t('login.password')}</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder={t('login.passwordPlaceholder')}
              required
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? t('login.loggingIn') : t('login.login')}
          </button>
        </form>

        <div className="demo-credentials">
          <p><strong>Demo Credentials:</strong></p>
          <p>Doctor: <code>dr_johnson</code> / <code>demo123</code></p>
          <p>Pharmacist: <code>pharm_smith</code> / <code>demo123</code></p>
        </div>
      </div>
    </div>
  )
}

export default Login
