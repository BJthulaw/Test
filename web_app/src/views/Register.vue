<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-header">
        <h1>注册账户</h1>
        <p>加入法学研究绘图工具，开启专业绘图之旅</p>
      </div>
      
      <el-form
        ref="registerForm"
        :model="registerData"
        :rules="registerRules"
        class="register-form"
        @submit.prevent="handleRegister"
      >
        <el-form-item prop="username">
          <el-input
            v-model="registerData.username"
            placeholder="用户名"
            size="large"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item prop="email">
          <el-input
            v-model="registerData.email"
            placeholder="邮箱地址"
            size="large"
            prefix-icon="Message"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="registerData.password"
            type="password"
            placeholder="密码"
            size="large"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item prop="confirmPassword">
          <el-input
            v-model="registerData.confirmPassword"
            type="password"
            placeholder="确认密码"
            size="large"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item prop="role">
          <el-select
            v-model="registerData.role"
            placeholder="选择用户类型"
            size="large"
            style="width: 100%"
          >
            <el-option label="学生" value="student" />
            <el-option label="教师" value="teacher" />
            <el-option label="研究员" value="researcher" />
            <el-option label="律师" value="lawyer" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        
        <el-form-item>
          <el-checkbox v-model="agreeTerms">
            我已阅读并同意 <el-link type="primary">服务条款</el-link> 和 <el-link type="primary">隐私政策</el-link>
          </el-checkbox>
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="register-button"
            :loading="loading"
            :disabled="!agreeTerms"
            @click="handleRegister"
          >
            注册
          </el-button>
        </el-form-item>
        
        <div class="register-divider">
          <span>已有账户？</span>
        </div>
        
        <el-form-item>
          <el-button
            size="large"
            class="login-button"
            @click="goToLogin"
          >
            立即登录
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { ElMessage } from 'element-plus'
import { User, Message, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

// 响应式数据
const registerForm = ref(null)
const loading = ref(false)
const agreeTerms = ref(false)

const registerData = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  role: ''
})

const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerData.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择用户类型', trigger: 'change' }
  ]
}

// 方法
const handleRegister = async () => {
  if (!registerForm.value) return
  
  try {
    await registerForm.value.validate()
    loading.value = true
    
    // 调用注册接口
    const success = await userStore.register(registerData)
    
    if (success) {
      ElMessage.success('注册成功，请登录')
      router.push('/login')
    } else {
      ElMessage.error('注册失败，请重试')
    }
  } catch (error) {
    console.error('注册失败:', error)
    ElMessage.error('注册失败，请重试')
  } finally {
    loading.value = false
  }
}

const goToLogin = () => {
  router.push('/login')
}
</script>

<style scoped lang="scss">
.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: $spacing-lg;
}

.register-container {
  background: $background-light;
  border-radius: $border-radius-large;
  padding: $spacing-xxl;
  box-shadow: $box-shadow-dark;
  width: 100%;
  max-width: 450px;
}

.register-header {
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

.register-form {
  .register-button {
    width: 100%;
    height: 48px;
    font-size: $font-size-large;
    font-weight: $font-weight-medium;
  }
  
  .login-button {
    width: 100%;
    height: 48px;
    font-size: $font-size-large;
  }
}

.register-divider {
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

@media (max-width: $breakpoint-sm) {
  .register-page {
    padding: $spacing-md;
  }
  
  .register-container {
    padding: $spacing-xl;
  }
}
</style> 