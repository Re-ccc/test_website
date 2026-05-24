import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { User } from '@/types'
import { authApi, userApi } from '@/api'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  const isLoggedIn = ref(!!token.value)
  const follows = ref<User[]>([])

  async function login(username: string, password: string) {
    try {
      const data = await authApi.login({ username, password })
      token.value = data.access_token
      localStorage.setItem('token', data.access_token)
      isLoggedIn.value = true
      await loadProfile()
      return true
    } catch {
      return false
    }
  }

  async function register(username: string, password: string, nickname?: string) {
    try {
      await authApi.register({ username, password, nickname })
      return true
    } catch {
      return false
    }
  }

  async function loadProfile() {
    try {
      const data = await userApi.getProfile()
      user.value = data
    } catch {
      user.value = null
    }
  }

  async function logout() {
    token.value = null
    user.value = null
    isLoggedIn.value = false
    localStorage.removeItem('token')
  }

  async function follow(userId: number) {
    try {
      const data = await userApi.followUser(userId)
      await loadProfile()
      return data
    } catch {
      return null
    }
  }

  async function loadMyFollows() {
    try {
      follows.value = await userApi.getMyFollows()
    } catch {
      follows.value = []
    }
  }

  return {
    user,
    token,
    isLoggedIn,
    follows,
    login,
    register,
    loadProfile,
    logout,
    follow,
    loadMyFollows,
  }
})
