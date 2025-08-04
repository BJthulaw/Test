<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-header">
        <h1>法学研究绘图工具</h1>
        <p>专业的学术绘图平台</p>
      </div>
      
      <el-form
        ref="loginForm"
        :model="loginData"
        :rules="loginRules"
        class="login-form"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginData.username"
            placeholder="用户名/邮箱"
            size="large"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="loginData.password"
            type="password"
            placeholder="密码"
            size="large"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <div class="login-options">
            <el-checkbox v-model="rememberMe">记住我</el-checkbox>
            <el-link type="primary">忘记密码？</el-link>
          </div>
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="login-button"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
        
        <div class="login-divider">
          <span>或</span>
        </div>
        
        <el-form-item>
          <el-button
            size="large"
            class="register-button"
            @click="goToRegister"
          >
            注册新账户
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="login-footer">
        <p>登录即表示同意我们的 <el-link type="primary">服务条款</el-link> 和 <el-link type="primary">隐私政策</el-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

// 响应式数据
const loginForm = ref(null)
const loading = ref(false)
const rememberMe = ref(false)

const loginData = reactive({
  username: '',
  password: ''
})

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, message: '用户名至少3个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6个字符', trigger: 'blur' }
  ]
}

// 方法
const handleLogin = async () => {
  if (!loginForm.value) return
  
  try {
    await loginForm.value.validate()
    loading.value = true
    
    // 调用登录接口
    const success = await userStore.login(loginData)
    
    if (success) {
      ElMessage.success('登录成功')
      router.push('/')
    } else {
      ElMessage.error('用户名或密码错误')
    }
  } catch (error) {
    console.error('登录失败:', error)
    ElMessage.error('登录失败，请重试')
  } finally {
    loading.value = false
  }
}

const goToRegister = () => {
  router.push('/register')
}
</script>

<style scoped lang="scss">
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: $spacing-lg;
}

.login-container {
  background: $background-light;
  border-radius: $border-radius-large;
  padding: $spacing-xxl;
  box-shadow: $box-shadow-dark;
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: $spacing-xl;
  
  h1 {
    color: $text-primary;
    margin-bottom: $spacing-sm;
    font-size: 24px;
    font-weight: $font-weight-bold;
  }
  
  p {
    color: $text-secondary;
    font-size: $font-size-large;
  }
}

.login-form {
  .login-options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
  }
  
  .login-button {
    width: 100%;
    height: 48px;
    font-size: $font-size-large;
    font-weight: $font-weight-medium;
  }
  
  .register-button {
    width: 100%;
    height: 48px;
    font-size: $font-size-large;
  }
}

.login-divider {
  text-align: center;
  margin: $spacing-lg 0;
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 0;
    right: 0;
    height: 1px;
    background: $border-light;
  }
  
  span {
    background: $background-light;
    padding: 0 $spacing-md;
    color: $text-secondary;
    font-size: $font-size-small;
  }
}

.login-footer {
  text-align: center;
  margin-top: $spacing-xl;
  
  p {
    color: $text-secondary;
    font-size: $font-size-small;
    line-height: 1.5;
  }
}

@media (max-width: $breakpoint-sm) {
  .login-page {
    padding: $spacing-md;
  }
  
  .login-container {
    padding: $spacing-xl;
  }
}
</style> 