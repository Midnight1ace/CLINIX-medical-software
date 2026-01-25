/// <reference types="vite/client" />
import axios from 'axios'
import { AuthResponse } from '@/types'

const API_BASE_URL = (import.meta.env.VITE_API_URL as string) || 'http://localhost:5000/api'

const authClient = axios.create({
  baseURL: API_BASE_URL,
})

export const authService = {
  login: async (email: string, password: string): Promise<AuthResponse> => {
    try {
      const response = await authClient.post('/auth/login', {
        email,
        password,
      })
      return response.data
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || 'Login failed',
      }
    }
  },

  logout: async (token: string) => {
    try {
      await authClient.post('/auth/logout', {}, {
        headers: { Authorization: `Bearer ${token}` },
      })
    } catch (error) {
      console.error('Logout error:', error)
    }
  },

  verifyToken: async (token: string): Promise<boolean> => {
    try {
      const response = await authClient.post('/auth/verify-token', {
        token,
      })
      return response.data.valid
    } catch (error) {
      return false
    }
  },
}
