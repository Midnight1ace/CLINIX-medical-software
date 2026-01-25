import { useAuthStore } from '@/store/authStore'

export function useAuth() {
  const { user, token, setAuth, logout } = useAuthStore()

  return {
    user,
    token,
    isAuthenticated: !!token,
    setAuth,
    logout,
  }
}
