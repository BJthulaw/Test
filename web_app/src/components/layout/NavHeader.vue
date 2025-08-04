<template>
  <header class="nav-header" :class="{ 'scrolled': isScrolled }">
    <div class="nav-container">
      <!-- Logo -->
      <div class="nav-logo" @click="goHome">
        <img src="@/assets/images/logo.svg" alt="法学研究绘图工具" />
        <span class="logo-text">法学研究绘图工具</span>
      </div>

      <!-- 导航菜单 -->
      <nav class="nav-menu" :class="{ 'mobile-open': isMobileMenuOpen }">
        <router-link 
          v-for="item in menuItems" 
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ 'active': currentPath === item.path }"
          @click="closeMobileMenu"
        >
          <el-icon><component :is="item.icon" /></el-icon>
          <span>{{ item.name }}</span>
        </router-link>
      </nav>

      <!-- 右侧工具栏 -->
      <div class="nav-toolbar">
        <!-- 主题切换 -->
        <el-button
          circle
          @click="toggleTheme"
          :title="isDarkMode ? '切换到亮色模式' : '切换到暗色模式'"
        >
          <el-icon>
            <component :is="isDarkMode ? 'Sunny' : 'Moon'" />
          </el-icon>
        </el-button>

        <!-- 用户菜单 -->
        <template v-if="userStore.isLoggedIn">
          <el-dropdown @command="handleUserCommand">
            <div class="user-avatar">
              <el-avatar :src="userStore.userInfo.avatar" :size="32">
                {{ userStore.userInfo.name?.charAt(0) }}
              </el-avatar>
              <span class="user-name">{{ userStore.userInfo.name }}</span>
              <el-icon><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>
                  个人中心
                </el-dropdown-item>
                <el-dropdown-item command="works" v-if="userStore.isVip">
                  <el-icon><Folder /></el-icon>
                  我的作品
                </el-dropdown-item>
                <el-dropdown-item command="templates" v-if="userStore.isVip">
                  <el-icon><Grid /></el-icon>
                  我的模板
                </el-dropdown-item>
                <el-dropdown-item command="admin" v-if="userStore.isAdmin">
                  <el-icon><Setting /></el-icon>
                  管理后台
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>

        <!-- 登录/注册按钮 -->
        <template v-else>
          <el-button @click="goLogin">登录</el-button>
          <el-button type="primary" @click="goRegister">注册</el-button>
        </template>

        <!-- 移动端菜单按钮 -->
        <el-button
          class="mobile-menu-btn"
          circle
          @click="toggleMobileMenu"
        >
          <el-icon>
            <component :is="isMobileMenuOpen ? 'Close' : 'Menu'" />
          </el-icon>
        </el-button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/store/user'
import { useThemeStore } from '@/store/theme'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const themeStore = useThemeStore()

// 响应式数据
const isScrolled = ref(false)
const isMobileMenuOpen = ref(false)

// 计算属性
const isDarkMode = computed(() => themeStore.isDarkMode)
const currentPath = computed(() => route.path)

// 菜单项配置
const menuItems = [
  { name: '首页', path: '/', icon: 'House' },
  { name: '模板库', path: '/templates', icon: 'Grid' },
  { name: '绘图工作台', path: '/drawing', icon: 'Edit' },
  { name: 'AI助手', path: '/ai-assistant', icon: 'MagicStick' },
  { name: '资源库', path: '/resources', icon: 'DataAnalysis' },
  { name: '作品展示', path: '/gallery', icon: 'Picture' },
  { name: '帮助中心', path: '/help', icon: 'QuestionFilled' }
]

// 方法
const goHome = () => {
  router.push('/')
}

const goLogin = () => {
  router.push('/login')
}

const goRegister = () => {
  router.push('/register')
}

const toggleTheme = () => {
  themeStore.setDarkMode(!isDarkMode.value)
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}

const handleUserCommand = async (command) => {
  switch (command) {
    case 'profile':
      router.push('/user')
      break
    case 'works':
      router.push('/user?tab=works')
      break
    case 'templates':
      router.push('/user?tab=templates')
      break
    case 'admin':
      router.push('/admin')
      break
    case 'logout':
      await handleLogout()
      break
  }
}

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要退出登录吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    userStore.logout()
    ElMessage.success('已退出登录')
    router.push('/')
  } catch {
    // 用户取消
  }
}

// 滚动监听
const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
}

// 生命周期
onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  // 初始化主题
  themeStore.initTheme()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style lang="scss" scoped>
.nav-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--el-border-color-lighter);
  transition: all 0.3s ease;

  &.scrolled {
    background: rgba(255, 255, 255, 0.98);
    box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
  }

  .nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .nav-logo {
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    transition: transform 0.2s ease;

    &:hover {
      transform: scale(1.05);
    }

    img {
      height: 32px;
      width: auto;
    }

    .logo-text {
      font-size: 1.2rem;
      font-weight: 600;
      color: var(--el-text-color-primary);
    }
  }

  .nav-menu {
    display: flex;
    align-items: center;
    gap: 8px;

    .nav-item {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 8px 16px;
      border-radius: 8px;
      text-decoration: none;
      color: var(--el-text-color-regular);
      font-weight: 500;
      transition: all 0.2s ease;

      &:hover {
        background: var(--el-color-primary-light-9);
        color: var(--el-color-primary);
      }

      &.active {
        background: var(--el-color-primary);
        color: white;
      }

      .el-icon {
        font-size: 16px;
      }
    }
  }

  .nav-toolbar {
    display: flex;
    align-items: center;
    gap: 12px;

    .user-avatar {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 4px 8px;
      border-radius: 20px;
      cursor: pointer;
      transition: background-color 0.2s ease;

      &:hover {
        background: var(--el-fill-color-light);
      }

      .user-name {
        font-size: 14px;
        color: var(--el-text-color-primary);
        max-width: 100px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
    }

    .mobile-menu-btn {
      display: none;
    }
  }
}

// 暗色模式
:deep(.dark) .nav-header {
  background: rgba(18, 18, 18, 0.95);

  &.scrolled {
    background: rgba(18, 18, 18, 0.98);
  }
}

// 移动端适配
@media (max-width: 768px) {
  .nav-header {
    .nav-container {
      padding: 0 16px;
    }

    .nav-logo {
      .logo-text {
        display: none;
      }
    }

    .nav-menu {
      position: fixed;
      top: 64px;
      left: 0;
      right: 0;
      background: var(--el-bg-color);
      border-bottom: 1px solid var(--el-border-color-lighter);
      flex-direction: column;
      padding: 20px;
      transform: translateY(-100%);
      opacity: 0;
      visibility: hidden;
      transition: all 0.3s ease;

      &.mobile-open {
        transform: translateY(0);
        opacity: 1;
        visibility: visible;
      }

      .nav-item {
        width: 100%;
        justify-content: flex-start;
        padding: 12px 16px;
      }
    }

    .nav-toolbar {
      .user-avatar {
        .user-name {
          display: none;
        }
      }

      .mobile-menu-btn {
        display: flex;
      }
    }
  }
}

// 动画
.nav-header {
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    transform: translateY(-100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style> 