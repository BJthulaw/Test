import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // 状态
  const isDarkMode = ref(localStorage.getItem('darkMode') === 'true')
  const autoTheme = ref(localStorage.getItem('autoTheme') !== 'false')
  const primaryColor = ref(localStorage.getItem('primaryColor') || '#409EFF')
  const fontSize = ref(localStorage.getItem('fontSize') || 'medium')

  // 设置暗色模式
  const setDarkMode = (dark) => {
    isDarkMode.value = dark
    localStorage.setItem('darkMode', dark.toString())
    
    // 应用主题
    applyTheme()
  }

  // 设置自动主题
  const setAutoTheme = (auto) => {
    autoTheme.value = auto
    localStorage.setItem('autoTheme', auto.toString())
    
    if (auto) {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
      setDarkMode(mediaQuery.matches)
    }
  }

  // 设置主色调
  const setPrimaryColor = (color) => {
    primaryColor.value = color
    localStorage.setItem('primaryColor', color)
    applyPrimaryColor()
  }

  // 设置字体大小
  const setFontSize = (size) => {
    fontSize.value = size
    localStorage.setItem('fontSize', size)
    applyFontSize()
  }

  // 应用主题
  const applyTheme = () => {
    const html = document.documentElement
    if (isDarkMode.value) {
      html.classList.add('dark')
    } else {
      html.classList.remove('dark')
    }
  }

  // 应用主色调
  const applyPrimaryColor = () => {
    const root = document.documentElement
    root.style.setProperty('--el-color-primary', primaryColor.value)
    
    // 生成主色调的变体
    const color = primaryColor.value
    const rgb = hexToRgb(color)
    if (rgb) {
      const { r, g, b } = rgb
      
      // 生成不同亮度的变体
      const variants = {
        '--el-color-primary-light-3': `rgba(${r}, ${g}, ${b}, 0.3)`,
        '--el-color-primary-light-5': `rgba(${r}, ${g}, ${b}, 0.5)`,
        '--el-color-primary-light-7': `rgba(${r}, ${g}, ${b}, 0.7)`,
        '--el-color-primary-light-8': `rgba(${r}, ${g}, ${b}, 0.8)`,
        '--el-color-primary-light-9': `rgba(${r}, ${g}, ${b}, 0.9)`,
        '--el-color-primary-dark-2': `rgb(${Math.max(0, r - 20)}, ${Math.max(0, g - 20)}, ${Math.max(0, b - 20)})`
      }
      
      Object.entries(variants).forEach(([key, value]) => {
        root.style.setProperty(key, value)
      })
    }
  }

  // 应用字体大小
  const applyFontSize = () => {
    const root = document.documentElement
    const sizes = {
      small: '14px',
      medium: '16px',
      large: '18px'
    }
    root.style.setProperty('--el-font-size-base', sizes[fontSize.value] || sizes.medium)
  }

  // 十六进制转RGB
  const hexToRgb = (hex) => {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
    return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
    } : null
  }

  // 初始化主题
  const initTheme = () => {
    // 应用保存的主题设置
    applyTheme()
    applyPrimaryColor()
    applyFontSize()
    
    // 监听系统主题变化
    if (autoTheme.value) {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
      const handleThemeChange = (e) => {
        if (autoTheme.value) {
          setDarkMode(e.matches)
        }
      }
      mediaQuery.addEventListener('change', handleThemeChange)
    }
  }

  // 重置主题
  const resetTheme = () => {
    setDarkMode(false)
    setAutoTheme(true)
    setPrimaryColor('#409EFF')
    setFontSize('medium')
  }

  return {
    // 状态
    isDarkMode,
    autoTheme,
    primaryColor,
    fontSize,
    
    // 方法
    setDarkMode,
    setAutoTheme,
    setPrimaryColor,
    setFontSize,
    initTheme,
    resetTheme
  }
}) 