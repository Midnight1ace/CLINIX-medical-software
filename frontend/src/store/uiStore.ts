import { create } from 'zustand'

interface UIState {
  emergencyMode: boolean
  sidebarOpen: boolean
  toggleEmergencyMode: () => void
  toggleSidebar: () => void
}

export const useUIStore = create<UIState>((set) => ({
  emergencyMode: false,
  sidebarOpen: true,

  toggleEmergencyMode: () => {
    set((state) => ({ emergencyMode: !state.emergencyMode }))
  },

  toggleSidebar: () => {
    set((state) => ({ sidebarOpen: !state.sidebarOpen }))
  },
}))
