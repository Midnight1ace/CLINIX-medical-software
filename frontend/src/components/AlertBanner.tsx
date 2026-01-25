import { Alert } from '@/types'

interface AlertBannerProps {
  alerts: Alert[]
}

export default function AlertBanner({ alerts }: AlertBannerProps) {
  if (!alerts || alerts.length === 0) return null

  const criticalAlerts = alerts.filter(a => a.severity === 'critical')

  return (
    <div className="alert-banner">
      <div className="alert-content">
        <h2>⚠️ CRITICAL ALERTS</h2>
        {criticalAlerts.map((alert) => (
          <div key={alert.id} className={`alert-item alert-${alert.severity}`}>
            <strong>{alert.title}</strong>
            {alert.description && <p>{alert.description}</p>}
          </div>
        ))}
      </div>
    </div>
  )
}
