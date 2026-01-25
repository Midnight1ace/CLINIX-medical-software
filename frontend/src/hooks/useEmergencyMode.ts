import { useState, useCallback } from 'react'
import { usePatientStore } from '@/store/patientStore'

export function useEmergencyMode() {
  const [isActive, setIsActive] = useState(false)
  const { patient } = usePatientStore()

  const toggleEmergencyMode = useCallback(() => {
    setIsActive(!isActive)
  }, [isActive])

  const activateEmergencyMode = useCallback(() => {
    setIsActive(true)
  }, [])

  const deactivateEmergencyMode = useCallback(() => {
    setIsActive(false)
  }, [])

  return {
    isActive,
    patient,
    toggleEmergencyMode,
    activateEmergencyMode,
    deactivateEmergencyMode,
  }
}
