<template>
  <div id="app" :class="{ 'dark-mode': isDarkMode }">
    <el-config-provider :locale="zhCn" :size="size">
      <router-view />
    </el-config-provider>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useThemeStore } from '@/store/theme'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

const themeStore = useThemeStore()
const isDarkMode = ref(false)
const size = ref('default')

onMounted(() => {
  // 初始化主题
  isDarkMode.value = themeStore.isDarkMode
  themeStore.$subscribe((mutation, state) => {
    isDarkMode.value = state.isDarkMode
  })
  
  // 监听系统主题变化
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
  const handleThemeChange = (e) => {
    if (themeStore.autoTheme) {
      themeStore.setDarkMode(e.matches)
    }
  }
  mediaQuery.addEventListener('change', handleThemeChange)
})
</script>

<style lang="scss">
#app {
  font-family: 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
  overflow: hidden;
  
  &.dark-mode {
    background-color: var(--el-bg-color);
    color: var(--el-text-color-primary);
  }
}

// 全局滚动条样式
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: var(--el-fill-color-lighter);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: var(--el-border-color);
  border-radius: 4px;
  
  &:hover {
    background: var(--el-border-color-darker);
  }
}

// 全局动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}

.slide-fade-enter-from {
  transform: translateX(-20px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}

// 响应式设计
@media (max-width: 768px) {
  #app {
    font-size: 14px;
  }
}
</style> 