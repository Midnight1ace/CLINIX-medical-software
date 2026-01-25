import { useCallback } from 'react'
import { useAuthStore } from '@/store/authStore'

export function useAuditLog() {
  const { user } = useAuthStore()

  const logAction = useCallback((action: string, resourceType: string, resourceId: string) => {
    if (!user) return

    const auditEvent = {
      userId: user.id,
      action,
      resourceType,
      resourceId,
      timestamp: new Date().toISOString(),
    }

    // In real app, send to backend
    console.log('Audit log:', auditEvent)
  }, [user])

  return { logAction }
}
