<template>
  <div class="about-page">
    <div class="page-header">
      <h1>关于我们</h1>
      <p>专业的法学研究绘图工具平台</p>
    </div>

    <div class="about-content">
      <!-- 项目介绍 -->
      <div class="section">
        <h2>项目介绍</h2>
        <p>
          法学研究绘图工具是一个专为法学研究人员、教师、学生和律师设计的专业绘图平台。
          我们致力于为法学学术研究提供高质量的图表制作工具，帮助用户更好地表达和展示法律概念、
          关系和流程。
        </p>
      </div>

      <!-- 核心功能 -->
      <div class="section">
        <h2>核心功能</h2>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">
              <el-icon><Edit /></el-icon>
            </div>
            <h3>智能绘图</h3>
            <p>基于AI技术的智能绘图功能，支持文本转图表，自动生成专业的法律图表</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">
              <el-icon><Files /></el-icon>
            </div>
            <h3>模板管理</h3>
            <p>丰富的法律研究模板库，支持自定义模板上传和管理</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">
              <el-icon><Share /></el-icon>
            </div>
            <h3>作品分享</h3>
            <p>支持作品展示和分享，促进学术交流和知识传播</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">
              <el-icon><Download /></el-icon>
            </div>
            <h3>多格式导出</h3>
            <p>支持PNG、SVG、PDF等多种格式导出，满足不同使用场景</p>
          </div>
        </div>
      </div>

      <!-- 技术特色 -->
      <div class="section">
        <h2>技术特色</h2>
        <div class="tech-list">
          <div class="tech-item">
            <h4>现代化前端技术</h4>
            <p>基于Vue 3、Element Plus等现代前端技术栈，提供流畅的用户体验</p>
          </div>
          <div class="tech-item">
            <h4>AI智能辅助</h4>
            <p>集成大语言模型，提供智能内容分析和图表生成建议</p>
          </div>
          <div class="tech-item">
            <h4>响应式设计</h4>
            <p>支持多设备访问，在桌面端和移动端都能提供良好的使用体验</p>
          </div>
          <div class="tech-item">
            <h4>云端部署</h4>
            <p>基于GitHub Pages的静态部署，确保稳定性和可访问性</p>
          </div>
        </div>
      </div>

      <!-- 使用场景 -->
      <div class="section">
        <h2>使用场景</h2>
        <div class="scenarios-grid">
          <div class="scenario-card">
            <h3>学术研究</h3>
            <ul>
              <li>论文图表制作</li>
              <li>研究框架展示</li>
              <li>文献关系梳理</li>
              <li>方法论流程图</li>
            </ul>
          </div>
          <div class="scenario-card">
            <h3>教学演示</h3>
            <ul>
              <li>课程内容展示</li>
              <li>案例分析图表</li>
              <li>法律概念解释</li>
              <li>知识点梳理</li>
            </ul>
          </div>
          <div class="scenario-card">
            <h3>实务工作</h3>
            <ul>
              <li>案件分析图表</li>
              <li>法律文书配图</li>
              <li>流程说明图</li>
              <li>关系分析图</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- 团队信息 -->
      <div class="section">
        <h2>开发团队</h2>
        <p>
          我们是一支专注于法学研究和教育技术开发的团队，致力于为法学领域提供专业的数字化工具。
          团队成员包括法学研究者、教育工作者和技术开发者，确保产品的专业性和实用性。
        </p>
      </div>

      <!-- 联系方式 -->
      <div class="section">
        <h2>联系我们</h2>
        <div class="contact-info">
          <div class="contact-item">
            <el-icon><Message /></el-icon>
            <span>邮箱：contact@legal-drawing.com</span>
          </div>
          <div class="contact-item">
            <el-icon><Link /></el-icon>
            <span>官网：https://legal-drawing.com</span>
          </div>
          <div class="contact-item">
            <el-icon><Location /></el-icon>
            <span>地址：北京市海淀区中关村大街1号</span>
          </div>
        </div>
      </div>

      <!-- 版本信息 -->
      <div class="section">
        <h2>版本信息</h2>
        <div class="version-info">
          <p><strong>当前版本：</strong>v3.0.0</p>
          <p><strong>更新日期：</strong>2024年1月</p>
          <p><strong>技术支持：</strong>Vue 3 + Element Plus + Fabric.js</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Edit, Files, Share, Download, Message, Link, Location } from '@element-plus/icons-vue'
</script>

<style scoped lang="scss">
.about-page {
  padding: $spacing-lg;
  max-width: 1200px;
  margin: 0 auto;
  
  .page-header {
    text-align: center;
    margin-bottom: $spacing-xxl;
    
    h1 {
      color: $text-primary;
      margin-bottom: $spacing-sm;
      font-size: 32px;
      font-weight: $font-weight-bold;
    }
    
    p {
      color: $text-secondary;
      font-size: $font-size-large;
    }
  }
  
  .about-content {
    .section {
      margin-bottom: $spacing-xxl;
      
      h2 {
        color: $text-primary;
        margin-bottom: $spacing-lg;
        font-size: 24px;
        font-weight: $font-weight-bold;
        border-bottom: 2px solid $primary-color;
        padding-bottom: $spacing-sm;
      }
      
      p {
        color: $text-regular;
        line-height: 1.8;
        font-size: $font-size-large;
      }
    }
    
    .features-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: $spacing-lg;
      margin-top: $spacing-lg;
    }
    
    .feature-card {
      background: $background-light;
      padding: $spacing-lg;
      border-radius: $border-radius-base;
      text-align: center;
      box-shadow: $box-shadow-light;
      transition: $transition-base;
      
      &:hover {
        transform: translateY(-4px);
        box-shadow: $box-shadow-base;
      }
      
      .feature-icon {
        width: 60px;
        height: 60px;
        background: $primary-color;
        border-radius: $border-radius-round;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto $spacing-md;
        
        .el-icon {
          font-size: 24px;
          color: white;
        }
      }
      
      h3 {
        color: $text-primary;
        margin-bottom: $spacing-sm;
        font-size: $font-size-large;
        font-weight: $font-weight-medium;
      }
      
      p {
        color: $text-secondary;
        font-size: $font-size-base;
        line-height: 1.6;
      }
    }
    
    .tech-list {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: $spacing-lg;
      margin-top: $spacing-lg;
    }
    
    .tech-item {
      background: $background-light;
      padding: $spacing-lg;
      border-radius: $border-radius-base;
      border-left: 4px solid $primary-color;
      
      h4 {
        color: $text-primary;
        margin-bottom: $spacing-sm;
        font-size: $font-size-large;
        font-weight: $font-weight-medium;
      }
      
      p {
        color: $text-secondary;
        line-height: 1.6;
      }
    }
    
    .scenarios-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: $spacing-lg;
      margin-top: $spacing-lg;
    }
    
    .scenario-card {
      background: $background-light;
      padding: $spacing-lg;
      border-radius: $border-radius-base;
      box-shadow: $box-shadow-light;
      
      h3 {
        color: $text-primary;
        margin-bottom: $spacing-md;
        font-size: $font-size-large;
        font-weight: $font-weight-medium;
      }
      
      ul {
        list-style: none;
        padding: 0;
        
        li {
          color: $text-secondary;
          padding: $spacing-xs 0;
          position: relative;
          padding-left: $spacing-md;
          
          &::before {
            content: '•';
            color: $primary-color;
            position: absolute;
            left: 0;
            font-weight: bold;
          }
        }
      }
    }
    
    .contact-info {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: $spacing-lg;
      margin-top: $spacing-lg;
    }
    
    .contact-item {
      display: flex;
      align-items: center;
      gap: $spacing-sm;
      padding: $spacing-md;
      background: $background-light;
      border-radius: $border-radius-base;
      
      .el-icon {
        color: $primary-color;
        font-size: 20px;
      }
      
      span {
        color: $text-regular;
        font-size: $font-size-large;
      }
    }
    
    .version-info {
      background: $background-light;
      padding: $spacing-lg;
      border-radius: $border-radius-base;
      margin-top: $spacing-lg;
      
      p {
        margin-bottom: $spacing-sm;
        color: $text-regular;
        
        &:last-child {
          margin-bottom: 0;
        }
      }
    }
  }
}

@media (max-width: $breakpoint-sm) {
  .about-page {
    padding: $spacing-md;
    
    .page-header h1 {
      font-size: 24px;
    }
    
    .about-content .section h2 {
      font-size: 20px;
    }
    
    .features-grid,
    .tech-list,
    .scenarios-grid,
    .contact-info {
      grid-template-columns: 1fr;
    }
  }
}
</style> 