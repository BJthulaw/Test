<template>
  <div class="home">
    <!-- 导航栏 -->
    <nav-header />
    
    <!-- 主要内容 -->
    <div class="main-content">
      <!-- 英雄区域 -->
      <section class="hero-section">
        <div class="hero-content">
          <h1 class="hero-title">
            法学研究科研绘图工具
            <span class="subtitle">专业学术绘图平台</span>
          </h1>
          <p class="hero-description">
            专为法学研究人员设计的智能绘图工具，支持模板管理、AI辅助绘图、多格式导出等功能，
            让您的学术论文配图更加专业、美观、规范。
          </p>
          <div class="hero-actions">
            <el-button type="primary" size="large" @click="startDrawing">
              <el-icon><Edit /></el-icon>
              开始绘图
            </el-button>
            <el-button size="large" @click="browseTemplates">
              <el-icon><Grid /></el-icon>
              浏览模板
            </el-button>
            <el-button size="large" @click="tryAI">
              <el-icon><MagicStick /></el-icon>
              体验AI助手
            </el-button>
          </div>
        </div>
        <div class="hero-image">
          <img src="@/assets/images/hero-illustration.svg" alt="法学研究绘图" />
        </div>
      </section>

      <!-- 功能特色 -->
      <section class="features-section">
        <h2 class="section-title">核心功能</h2>
        <div class="features-grid">
          <div class="feature-card" v-for="feature in features" :key="feature.id">
            <div class="feature-icon">
              <el-icon :size="48">
                <component :is="feature.icon" />
              </el-icon>
            </div>
            <h3 class="feature-title">{{ feature.title }}</h3>
            <p class="feature-description">{{ feature.description }}</p>
          </div>
        </div>
      </section>

      <!-- 模板展示 -->
      <section class="templates-section">
        <div class="section-header">
          <h2 class="section-title">精选模板</h2>
          <el-button type="primary" @click="browseTemplates">
            查看更多
            <el-icon><ArrowRight /></el-icon>
          </el-button>
        </div>
        <div class="templates-grid">
          <template-card
            v-for="template in featuredTemplates"
            :key="template.id"
            :template="template"
            @click="viewTemplate(template)"
          />
        </div>
      </section>

      <!-- 使用统计 -->
      <section class="stats-section">
        <div class="stats-grid">
          <div class="stat-item" v-for="stat in stats" :key="stat.label">
            <div class="stat-number">{{ stat.value }}</div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
        </div>
      </section>

      <!-- 用户评价 -->
      <section class="testimonials-section">
        <h2 class="section-title">用户评价</h2>
        <div class="testimonials-grid">
          <div class="testimonial-card" v-for="testimonial in testimonials" :key="testimonial.id">
            <div class="testimonial-content">
              <p>{{ testimonial.content }}</p>
            </div>
            <div class="testimonial-author">
              <img :src="testimonial.avatar" :alt="testimonial.name" />
              <div class="author-info">
                <div class="author-name">{{ testimonial.name }}</div>
                <div class="author-title">{{ testimonial.title }}</div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- 页脚 -->
    <app-footer />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import NavHeader from '@/components/layout/NavHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import TemplateCard from '@/components/template/TemplateCard.vue'

const router = useRouter()
const userStore = useUserStore()

// 功能特色数据
const features = ref([
  {
    id: 1,
    icon: 'Grid',
    title: '模板管理',
    description: '支持多种格式模板上传，按法学领域分类管理，提供丰富的预设模板库'
  },
  {
    id: 2,
    icon: 'MagicStick',
    title: 'AI辅助绘图',
    description: '集成大语言模型，智能分析文本内容，自动生成专业学术图表'
  },
  {
    id: 3,
    icon: 'Download',
    title: '多格式导出',
    description: '支持PNG、PDF、SVG等多种格式导出，满足不同期刊投稿要求'
  },
  {
    id: 4,
    icon: 'Setting',
    title: '风格定制',
    description: '提供多种法学论文专用绘图风格，适配不同期刊的排版规范'
  },
  {
    id: 5,
    icon: 'DataAnalysis',
    title: '资源采集',
    description: '自动爬取学术资源，建立法学绘图知识库，提供合规使用指导'
  },
  {
    id: 6,
    icon: 'User',
    title: '权限管理',
    description: '多角色权限控制，支持个人模板库、管理员后台等功能'
  }
])

// 精选模板数据
const featuredTemplates = ref([
  {
    id: 1,
    name: '法律问题分析流程图',
    category: '流程图',
    field: '通用',
    thumbnail: '/templates/legal-flowchart.png',
    downloads: 1234,
    rating: 4.8
  },
  {
    id: 2,
    name: '司法程序流程图',
    category: '流程图',
    field: '诉讼法',
    thumbnail: '/templates/judicial-process.png',
    downloads: 856,
    rating: 4.9
  },
  {
    id: 3,
    name: '法律条文适用范围图',
    category: '示意图',
    field: '实体法',
    thumbnail: '/templates/legal-scope.png',
    downloads: 567,
    rating: 4.7
  },
  {
    id: 4,
    name: '案例比较分析图',
    category: '对比图',
    field: '案例研究',
    thumbnail: '/templates/case-comparison.png',
    downloads: 789,
    rating: 4.6
  }
])

// 统计数据
const stats = ref([
  { label: '注册用户', value: '10,000+' },
  { label: '模板数量', value: '500+' },
  { label: '生成图表', value: '50,000+' },
  { label: '用户评价', value: '4.8/5.0' }
])

// 用户评价数据
const testimonials = ref([
  {
    id: 1,
    content: '这个工具大大提高了我的论文配图效率，AI功能特别实用，生成的图表质量很高。',
    name: '张教授',
    title: '北京大学法学院',
    avatar: '/avatars/user1.jpg'
  },
  {
    id: 2,
    content: '模板库很丰富，特别是法律流程图模板，完全符合学术规范要求。',
    name: '李研究员',
    title: '中国社会科学院',
    avatar: '/avatars/user2.jpg'
  },
  {
    id: 3,
    content: '界面设计专业，操作简单，导出功能完善，强烈推荐给法学研究者。',
    name: '王博士',
    title: '清华大学法学院',
    avatar: '/avatars/user3.jpg'
  }
])

// 方法
const startDrawing = () => {
  if (userStore.isLoggedIn) {
    router.push('/drawing')
  } else {
    router.push('/login')
  }
}

const browseTemplates = () => {
  router.push('/templates')
}

const tryAI = () => {
  if (userStore.isLoggedIn) {
    router.push('/ai-assistant')
  } else {
    router.push('/login')
  }
}

const viewTemplate = (template) => {
  router.push(`/templates/${template.id}`)
}

onMounted(() => {
  // 初始化用户状态
  userStore.init()
})
</script>

<style lang="scss" scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

// 英雄区域
.hero-section {
  display: flex;
  align-items: center;
  min-height: 600px;
  padding: 80px 0;
  gap: 60px;

  .hero-content {
    flex: 1;

    .hero-title {
      font-size: 3rem;
      font-weight: 700;
      color: var(--el-text-color-primary);
      margin-bottom: 20px;
      line-height: 1.2;

      .subtitle {
        display: block;
        font-size: 1.5rem;
        font-weight: 400;
        color: var(--el-text-color-regular);
        margin-top: 10px;
      }
    }

    .hero-description {
      font-size: 1.2rem;
      color: var(--el-text-color-regular);
      margin-bottom: 40px;
      line-height: 1.6;
    }

    .hero-actions {
      display: flex;
      gap: 20px;
      flex-wrap: wrap;
    }
  }

  .hero-image {
    flex: 1;
    text-align: center;

    img {
      max-width: 100%;
      height: auto;
    }
  }
}

// 功能特色
.features-section {
  padding: 80px 0;

  .section-title {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 600;
    margin-bottom: 60px;
    color: var(--el-text-color-primary);
  }

  .features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 40px;
  }

  .feature-card {
    background: var(--el-bg-color);
    padding: 40px;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease;

    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
    }

    .feature-icon {
      color: var(--el-color-primary);
      margin-bottom: 20px;
    }

    .feature-title {
      font-size: 1.5rem;
      font-weight: 600;
      margin-bottom: 15px;
      color: var(--el-text-color-primary);
    }

    .feature-description {
      color: var(--el-text-color-regular);
      line-height: 1.6;
    }
  }
}

// 模板展示
.templates-section {
  padding: 80px 0;

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 40px;

    .section-title {
      font-size: 2.5rem;
      font-weight: 600;
      color: var(--el-text-color-primary);
    }
  }

  .templates-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 30px;
  }
}

// 统计数据
.stats-section {
  padding: 80px 0;
  background: var(--el-color-primary);
  margin: 0 -20px;
  padding-left: 20px;
  padding-right: 20px;

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 40px;
    text-align: center;
  }

  .stat-item {
    color: white;

    .stat-number {
      font-size: 3rem;
      font-weight: 700;
      margin-bottom: 10px;
    }

    .stat-label {
      font-size: 1.1rem;
      opacity: 0.9;
    }
  }
}

// 用户评价
.testimonials-section {
  padding: 80px 0;

  .section-title {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 600;
    margin-bottom: 60px;
    color: var(--el-text-color-primary);
  }

  .testimonials-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 30px;
  }

  .testimonial-card {
    background: var(--el-bg-color);
    padding: 30px;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);

    .testimonial-content {
      margin-bottom: 20px;
      font-style: italic;
      color: var(--el-text-color-regular);
      line-height: 1.6;
    }

    .testimonial-author {
      display: flex;
      align-items: center;
      gap: 15px;

      img {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        object-fit: cover;
      }

      .author-info {
        .author-name {
          font-weight: 600;
          color: var(--el-text-color-primary);
        }

        .author-title {
          font-size: 0.9rem;
          color: var(--el-text-color-regular);
        }
      }
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .hero-section {
    flex-direction: column;
    text-align: center;
    padding: 40px 0;

    .hero-title {
      font-size: 2rem;

      .subtitle {
        font-size: 1.2rem;
      }
    }

    .hero-actions {
      justify-content: center;
    }
  }

  .features-grid,
  .templates-grid,
  .testimonials-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .section-title {
    font-size: 2rem !important;
  }
}
</style> 