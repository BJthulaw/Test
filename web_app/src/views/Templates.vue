<template>
  <div class="templates-page">
    <div class="page-header">
      <h1>模板管理</h1>
      <p>管理和使用各种法学研究绘图模板</p>
    </div>

    <div class="templates-container">
      <!-- 模板分类 -->
      <div class="template-categories">
        <el-tabs v-model="activeCategory" @tab-click="handleCategoryChange">
          <el-tab-pane label="法律研究" name="legal">
            <div class="template-grid">
              <div v-for="template in legalTemplates" :key="template.id" class="template-card">
                <div class="template-preview">
                  <img :src="template.preview" :alt="template.name" />
                </div>
                <div class="template-info">
                  <h3>{{ template.name }}</h3>
                  <p>{{ template.description }}</p>
                  <div class="template-actions">
                    <el-button type="primary" size="small" @click="useTemplate(template)">
                      使用模板
                    </el-button>
                    <el-button size="small" @click="previewTemplate(template)">
                      预览
                    </el-button>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="学术论文" name="academic">
            <div class="template-grid">
              <div v-for="template in academicTemplates" :key="template.id" class="template-card">
                <div class="template-preview">
                  <img :src="template.preview" :alt="template.name" />
                </div>
                <div class="template-info">
                  <h3>{{ template.name }}</h3>
                  <p>{{ template.description }}</p>
                  <div class="template-actions">
                    <el-button type="primary" size="small" @click="useTemplate(template)">
                      使用模板
                    </el-button>
                    <el-button size="small" @click="previewTemplate(template)">
                      预览
                    </el-button>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="我的模板" name="personal">
            <div class="upload-section">
              <el-upload
                class="template-upload"
                drag
                action="#"
                :auto-upload="false"
                :on-change="handleFileChange"
                accept=".svg,.png,.jpg,.jpeg,.pdf"
              >
                <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                <div class="el-upload__text">
                  将文件拖到此处，或<em>点击上传</em>
                </div>
                <template #tip>
                  <div class="el-upload__tip">
                    支持 SVG、PNG、JPG、PDF 格式，文件大小不超过 10MB
                  </div>
                </template>
              </el-upload>
            </div>
            
            <div class="template-grid">
              <div v-for="template in personalTemplates" :key="template.id" class="template-card">
                <div class="template-preview">
                  <img :src="template.preview" :alt="template.name" />
                </div>
                <div class="template-info">
                  <h3>{{ template.name }}</h3>
                  <p>{{ template.description }}</p>
                  <div class="template-actions">
                    <el-button type="primary" size="small" @click="useTemplate(template)">
                      使用模板
                    </el-button>
                    <el-button size="small" @click="editTemplate(template)">
                      编辑
                    </el-button>
                    <el-button type="danger" size="small" @click="deleteTemplate(template)">
                      删除
                    </el-button>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>

    <!-- 模板预览对话框 -->
    <el-dialog v-model="previewVisible" title="模板预览" width="60%">
      <div class="template-preview-dialog">
        <img :src="previewTemplate.preview" :alt="previewTemplate.name" />
        <div class="preview-info">
          <h3>{{ previewTemplate.name }}</h3>
          <p>{{ previewTemplate.description }}</p>
          <div class="preview-actions">
            <el-button type="primary" @click="useTemplate(previewTemplate)">
              使用此模板
            </el-button>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'

const router = useRouter()

// 响应式数据
const activeCategory = ref('legal')
const previewVisible = ref(false)
const previewTemplate = ref({})

// 模板数据
const legalTemplates = ref([
  {
    id: 1,
    name: '法律问题分析图',
    description: '用于分析法律问题的逻辑结构',
    preview: '/templates/legal-analysis.png',
    type: 'legal'
  },
  {
    id: 2,
    name: '法律关系图',
    description: '展示法律主体之间的关系',
    preview: '/templates/legal-relationship.png',
    type: 'legal'
  }
])

const academicTemplates = ref([
  {
    id: 3,
    name: '学术研究框架图',
    description: '学术论文的研究框架展示',
    preview: '/templates/academic-framework.png',
    type: 'academic'
  },
  {
    id: 4,
    name: '文献综述关系图',
    description: '文献之间的引用和关系',
    preview: '/templates/literature-review.png',
    type: 'academic'
  }
])

const personalTemplates = ref([])

// 方法
const handleCategoryChange = (tab) => {
  console.log('切换到分类:', tab.props.name)
}

const useTemplate = (template) => {
  router.push({
    path: '/drawing',
    query: { template: template.id }
  })
}

const previewTemplate = (template) => {
  previewTemplate.value = template
  previewVisible.value = true
}

const handleFileChange = (file) => {
  console.log('文件上传:', file)
  ElMessage.success('模板上传成功')
}

const editTemplate = (template) => {
  console.log('编辑模板:', template)
}

const deleteTemplate = (template) => {
  ElMessage.warning('删除模板功能待实现')
}
</script>

<style scoped lang="scss">
.templates-page {
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
  
  .templates-container {
    background: $background-light;
    border-radius: $border-radius-large;
    padding: $spacing-lg;
    box-shadow: $box-shadow-light;
  }
  
  .template-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: $spacing-lg;
    margin-top: $spacing-lg;
  }
  
  .template-card {
    border: 1px solid $border-light;
    border-radius: $border-radius-base;
    overflow: hidden;
    transition: $transition-base;
    
    &:hover {
      box-shadow: $box-shadow-base;
      transform: translateY(-2px);
    }
    
    .template-preview {
      height: 200px;
      background: $background-color;
      display: flex;
      align-items: center;
      justify-content: center;
      
      img {
        max-width: 100%;
        max-height: 100%;
        object-fit: cover;
      }
    }
    
    .template-info {
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
      }
      
      .template-actions {
        display: flex;
        gap: $spacing-sm;
      }
    }
  }
  
  .upload-section {
    margin-bottom: $spacing-xl;
    
    .template-upload {
      width: 100%;
    }
  }
  
  .template-preview-dialog {
    display: flex;
    gap: $spacing-lg;
    
    img {
      max-width: 50%;
      border-radius: $border-radius-base;
    }
    
    .preview-info {
      flex: 1;
      
      h3 {
        margin-bottom: $spacing-md;
        color: $text-primary;
      }
      
      p {
        color: $text-secondary;
        line-height: 1.6;
        margin-bottom: $spacing-lg;
      }
    }
  }
}

@media (max-width: $breakpoint-sm) {
  .templates-page {
    padding: $spacing-md;
    
    .template-grid {
      grid-template-columns: 1fr;
    }
    
    .template-preview-dialog {
      flex-direction: column;
      
      img {
        max-width: 100%;
      }
    }
  }
}
</style> 