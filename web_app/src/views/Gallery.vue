<template>
  <div class="gallery-page">
    <div class="page-header">
      <h1>作品展示</h1>
      <p>浏览和分享优秀的法学研究绘图作品</p>
    </div>

    <div class="gallery-container">
      <!-- 筛选器 -->
      <div class="gallery-filters">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-select v-model="filter.category" placeholder="选择分类" clearable>
              <el-option label="法律研究" value="legal" />
              <el-option label="学术论文" value="academic" />
              <el-option label="案例分析" value="case" />
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-select v-model="filter.style" placeholder="选择风格" clearable>
              <el-option label="流程图" value="flowchart" />
              <el-option label="关系图" value="relationship" />
              <el-option label="框架图" value="framework" />
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-input v-model="filter.keyword" placeholder="搜索关键词" />
          </el-col>
          <el-col :span="6">
            <el-button type="primary" @click="applyFilters">筛选</el-button>
            <el-button @click="resetFilters">重置</el-button>
          </el-col>
        </el-row>
      </div>

      <!-- 作品网格 -->
      <div class="gallery-grid">
        <div v-for="work in filteredWorks" :key="work.id" class="work-card">
          <div class="work-preview" @click="previewWork(work)">
            <img :src="work.preview" :alt="work.title" />
            <div class="work-overlay">
              <el-button type="primary" size="small">查看详情</el-button>
            </div>
          </div>
          <div class="work-info">
            <h3>{{ work.title }}</h3>
            <p>{{ work.description }}</p>
            <div class="work-meta">
              <span class="author">作者: {{ work.author }}</span>
              <span class="date">{{ work.createDate }}</span>
            </div>
            <div class="work-actions">
              <el-button size="small" @click="likeWork(work)">
                <el-icon><heart /></el-icon>
                {{ work.likes }}
              </el-button>
              <el-button size="small" @click="downloadWork(work)">
                <el-icon><download /></el-icon>
                下载
              </el-button>
              <el-button size="small" @click="shareWork(work)">
                <el-icon><share /></el-icon>
                分享
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div class="gallery-pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[12, 24, 48, 96]"
          :total="totalWorks"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <!-- 作品详情对话框 -->
    <el-dialog v-model="previewVisible" title="作品详情" width="70%">
      <div class="work-detail" v-if="previewWork">
        <div class="work-image">
          <img :src="previewWork.preview" :alt="previewWork.title" />
        </div>
        <div class="work-detail-info">
          <h2>{{ previewWork.title }}</h2>
          <p class="description">{{ previewWork.description }}</p>
          <div class="detail-meta">
            <p><strong>作者:</strong> {{ previewWork.author }}</p>
            <p><strong>创建时间:</strong> {{ previewWork.createDate }}</p>
            <p><strong>分类:</strong> {{ previewWork.category }}</p>
            <p><strong>风格:</strong> {{ previewWork.style }}</p>
          </div>
          <div class="detail-actions">
            <el-button type="primary" @click="useAsTemplate(previewWork)">
              用作模板
            </el-button>
            <el-button @click="downloadWork(previewWork)">
              下载原图
            </el-button>
            <el-button @click="shareWork(previewWork)">
              分享作品
            </el-button>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Heart, Download, Share } from '@element-plus/icons-vue'

const router = useRouter()

// 响应式数据
const currentPage = ref(1)
const pageSize = ref(12)
const totalWorks = ref(100)
const previewVisible = ref(false)
const previewWork = ref(null)

const filter = reactive({
  category: '',
  style: '',
  keyword: ''
})

// 模拟作品数据
const works = ref([
  {
    id: 1,
    title: '知识产权保护流程图',
    description: '详细展示知识产权保护的完整流程和法律依据',
    author: '张教授',
    createDate: '2024-01-15',
    category: 'legal',
    style: 'flowchart',
    preview: '/works/ip-protection.png',
    likes: 45
  },
  {
    id: 2,
    title: '学术研究框架图',
    description: '法学研究方法论的整体框架展示',
    author: '李研究员',
    createDate: '2024-01-10',
    category: 'academic',
    style: 'framework',
    preview: '/works/research-framework.png',
    likes: 32
  },
  {
    id: 3,
    title: '合同法律关系分析',
    description: '合同各方的权利义务关系分析图',
    author: '王律师',
    createDate: '2024-01-08',
    category: 'legal',
    style: 'relationship',
    preview: '/works/contract-relationship.png',
    likes: 28
  }
])

// 计算属性
const filteredWorks = computed(() => {
  let result = works.value

  if (filter.category) {
    result = result.filter(work => work.category === filter.category)
  }

  if (filter.style) {
    result = result.filter(work => work.style === filter.style)
  }

  if (filter.keyword) {
    result = result.filter(work => 
      work.title.includes(filter.keyword) || 
      work.description.includes(filter.keyword)
    )
  }

  return result
})

// 方法
const applyFilters = () => {
  currentPage.value = 1
  ElMessage.success('筛选条件已应用')
}

const resetFilters = () => {
  filter.category = ''
  filter.style = ''
  filter.keyword = ''
  currentPage.value = 1
  ElMessage.info('筛选条件已重置')
}

const previewWork = (work) => {
  previewWork.value = work
  previewVisible.value = true
}

const likeWork = (work) => {
  work.likes++
  ElMessage.success('点赞成功')
}

const downloadWork = (work) => {
  ElMessage.success(`开始下载: ${work.title}`)
}

const shareWork = (work) => {
  ElMessage.success(`分享链接已复制: ${work.title}`)
}

const useAsTemplate = (work) => {
  router.push({
    path: '/drawing',
    query: { template: work.id }
  })
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
}

const handleCurrentChange = (page) => {
  currentPage.value = page
}
</script>

<style scoped lang="scss">
.gallery-page {
  padding: $spacing-lg;
  
  .page-header {
    margin-bottom: $spacing-xl;
    
    h1 {
      color: $text-primary;
      margin-bottom: $spacing-sm;
    }
    
    p {
      color: $text-secondary;
      font-size: $font-size-large;
    }
  }
  
  .gallery-container {
    background: $background-light;
    border-radius: $border-radius-large;
    padding: $spacing-lg;
    box-shadow: $box-shadow-light;
  }
  
  .gallery-filters {
    margin-bottom: $spacing-xl;
    padding-bottom: $spacing-lg;
    border-bottom: 1px solid $border-light;
  }
  
  .gallery-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: $spacing-lg;
    margin-bottom: $spacing-xl;
  }
  
  .work-card {
    border: 1px solid $border-light;
    border-radius: $border-radius-base;
    overflow: hidden;
    transition: $transition-base;
    
    &:hover {
      box-shadow: $box-shadow-base;
      transform: translateY(-2px);
    }
    
    .work-preview {
      position: relative;
      height: 200px;
      cursor: pointer;
      
      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
      
      .work-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0;
        transition: $transition-base;
      }
      
      &:hover .work-overlay {
        opacity: 1;
      }
    }
    
    .work-info {
      padding: $spacing-md;
      
      h3 {
        margin: 0 0 $spacing-sm 0;
        color: $text-primary;
        font-size: $font-size-large;
      }
      
      p {
        color: $text-secondary;
        margin-bottom: $spacing-md;
        line-height: 1.5;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }
      
      .work-meta {
        display: flex;
        justify-content: space-between;
        margin-bottom: $spacing-md;
        font-size: $font-size-small;
        color: $text-secondary;
      }
      
      .work-actions {
        display: flex;
        gap: $spacing-sm;
      }
    }
  }
  
  .gallery-pagination {
    display: flex;
    justify-content: center;
    margin-top: $spacing-xl;
  }
  
  .work-detail {
    display: flex;
    gap: $spacing-xl;
    
    .work-image {
      flex: 1;
      
      img {
        width: 100%;
        border-radius: $border-radius-base;
      }
    }
    
    .work-detail-info {
      flex: 1;
      
      h2 {
        margin-bottom: $spacing-md;
        color: $text-primary;
      }
      
      .description {
        color: $text-secondary;
        line-height: 1.6;
        margin-bottom: $spacing-lg;
      }
      
      .detail-meta {
        margin-bottom: $spacing-xl;
        
        p {
          margin-bottom: $spacing-sm;
          color: $text-regular;
        }
      }
      
      .detail-actions {
        display: flex;
        gap: $spacing-md;
      }
    }
  }
}

@media (max-width: $breakpoint-sm) {
  .gallery-page {
    padding: $spacing-md;
    
    .gallery-grid {
      grid-template-columns: 1fr;
    }
    
    .work-detail {
      flex-direction: column;
    }
  }
}
</style> 