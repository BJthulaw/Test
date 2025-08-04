import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { userApi } from '@/api/user'

export const useUserStore = defineStore('user', () => {
  // 状态
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || '')
  const loading = ref(false)
  const error = ref('')

  // 计算属性
  const isLoggedIn = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isVip = computed(() => user.value?.role === 'vip' || isAdmin.value)
  const userInfo = computed(() => user.value || {})

  // 登录
  const login = async (credentials) => {
    try {
      loading.value = true
      error.value = ''
      
      const response = await userApi.login(credentials)
      const { token: newToken, user: userData } = response.data
      
      token.value = newToken
      user.value = userData
      
      localStorage.setItem('token', newToken)
      localStorage.setItem('user', JSON.stringify(userData))
      
      return { success: true }
    } catch (err) {
      error.value = err.message || '登录失败'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // 注册
  const register = async (userData) => {
    try {
      loading.value = true
      error.value = ''
      
      const response = await userApi.register(userData)
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.message || '注册失败'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // 登出
  const logout = () => {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  // 获取用户信息
  const fetchUserInfo = async () => {
    if (!token.value) return
    
    try {
      loading.value = true
      const response = await userApi.getProfile()
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(response.data))
    } catch (err) {
      console.error('获取用户信息失败:', err)
      logout()
    } finally {
      loading.value = false
    }
  }

  // 更新用户信息
  const updateProfile = async (profileData) => {
    try {
      loading.value = true
      error.value = ''
      
      const response = await userApi.updateProfile(profileData)
      user.value = { ...user.value, ...response.data }
      localStorage.setItem('user', JSON.stringify(user.value))
      
      return { success: true }
    } catch (err) {
      error.value = err.message || '更新失败'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // 初始化
  const init = async () => {
    if (token.value) {
      const savedUser = localStorage.getItem('user')
      if (savedUser) {
        try {
          user.value = JSON.parse(savedUser)
        } catch (err) {
          console.error('解析用户信息失败:', err)
          logout()
        }
      }
      
      // 验证token有效性
      await fetchUserInfo()
    }
  }

  return {
    // 状态
    user,
    token,
    loading,
    error,
    
    // 计算属性
    isLoggedIn,
    isAdmin,
    isVip,
    userInfo,
    
    // 方法
    login,
    register,
    logout,
    fetchUserInfo,
    updateProfile,
    init
  }
}) 