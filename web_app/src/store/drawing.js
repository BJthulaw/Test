import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useDrawingStore = defineStore('drawing', () => {
  // 状态
  const projects = ref([])
  const currentProject = ref(null)
  const projectHistory = ref([])
  const historyIndex = ref(-1)

  // 计算属性
  const hasProjects = computed(() => projects.value.length > 0)
  const canUndo = computed(() => historyIndex.value > 0)
  const canRedo = computed(() => historyIndex.value < projectHistory.value.length - 1)

  // 保存项目
  const saveProject = (projectData) => {
    const project = {
      id: Date.now().toString(),
      ...projectData,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }

    // 检查是否已存在同名项目
    const existingIndex = projects.value.findIndex(p => p.title === project.title)
    if (existingIndex >= 0) {
      projects.value[existingIndex] = project
    } else {
      projects.value.push(project)
    }

    // 保存到本地存储
    saveToLocalStorage()
    
    return project
  }

  // 加载项目
  const loadProject = (projectId) => {
    const project = projects.value.find(p => p.id === projectId)
    if (project) {
      currentProject.value = project
      return project
    }
    return null
  }

  // 删除项目
  const deleteProject = (projectId) => {
    const index = projects.value.findIndex(p => p.id === projectId)
    if (index >= 0) {
      projects.value.splice(index, 1)
      saveToLocalStorage()
      
      // 如果删除的是当前项目，清空当前项目
      if (currentProject.value?.id === projectId) {
        currentProject.value = null
      }
    }
  }

  // 更新项目
  const updateProject = (projectId, updates) => {
    const project = projects.value.find(p => p.id === projectId)
    if (project) {
      Object.assign(project, updates, {
        updatedAt: new Date().toISOString()
      })
      saveToLocalStorage()
    }
  }

  // 历史记录管理
  const addToHistory = (canvasState) => {
    // 移除当前位置之后的历史记录
    projectHistory.value = projectHistory.value.slice(0, historyIndex.value + 1)
    
    // 添加新的状态
    projectHistory.value.push(JSON.stringify(canvasState))
    historyIndex.value = projectHistory.value.length - 1
    
    // 限制历史记录数量
    if (projectHistory.value.length > 50) {
      projectHistory.value.shift()
      historyIndex.value--
    }
  }

  const undo = () => {
    if (canUndo.value) {
      historyIndex.value--
      return JSON.parse(projectHistory.value[historyIndex.value])
    }
    return null
  }

  const redo = () => {
    if (canRedo.value) {
      historyIndex.value++
      return JSON.parse(projectHistory.value[historyIndex.value])
    }
    return null
  }

  // 清空历史记录
  const clearHistory = () => {
    projectHistory.value = []
    historyIndex.value = -1
  }

  // 导出项目
  const exportProject = (projectId, format = 'json') => {
    const project = projects.value.find(p => p.id === projectId)
    if (!project) return null

    switch (format) {
      case 'json':
        return JSON.stringify(project, null, 2)
      case 'html':
        return generateHTML(project)
      case 'markdown':
        return generateMarkdown(project)
      default:
        return JSON.stringify(project, null, 2)
    }
  }

  // 生成HTML
  const generateHTML = (project) => {
    return `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${project.title}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .project-info { margin-bottom: 20px; }
        .canvas-container { border: 1px solid #ccc; padding: 20px; }
    </style>
</head>
<body>
    <div class="project-info">
        <h1>${project.title}</h1>
        <p>创建时间: ${new Date(project.createdAt).toLocaleString()}</p>
        <p>更新时间: ${new Date(project.updatedAt).toLocaleString()}</p>
    </div>
    <div class="canvas-container">
        <canvas id="canvas" width="800" height="600"></canvas>
    </div>
    <script>
        // 这里可以添加画布渲染逻辑
        const canvasData = ${JSON.stringify(project.canvas)};
        // 使用Fabric.js或其他库渲染画布
    </script>
</body>
</html>`
  }

  // 生成Markdown
  const generateMarkdown = (project) => {
    return `# ${project.title}

## 项目信息
- **创建时间**: ${new Date(project.createdAt).toLocaleString()}
- **更新时间**: ${new Date(project.updatedAt).toLocaleString()}
- **模板**: ${project.template || '无'}

## 画布数据
\`\`\`json
${JSON.stringify(project.canvas, null, 2)}
\`\`\`

## 导出信息
- 导出时间: ${new Date().toLocaleString()}
- 导出格式: Markdown
`
  }

  // 本地存储
  const saveToLocalStorage = () => {
    try {
      localStorage.setItem('drawing_projects', JSON.stringify(projects.value))
    } catch (error) {
      console.error('保存项目到本地存储失败:', error)
    }
  }

  const loadFromLocalStorage = () => {
    try {
      const saved = localStorage.getItem('drawing_projects')
      if (saved) {
        projects.value = JSON.parse(saved)
      }
    } catch (error) {
      console.error('从本地存储加载项目失败:', error)
    }
  }

  // 清空所有数据
  const clearAllData = () => {
    projects.value = []
    currentProject.value = null
    projectHistory.value = []
    historyIndex.value = -1
    localStorage.removeItem('drawing_projects')
  }

  // 获取项目统计
  const getProjectStats = () => {
    const total = projects.value.length
    const recent = projects.value.filter(p => {
      const weekAgo = new Date()
      weekAgo.setDate(weekAgo.getDate() - 7)
      return new Date(p.createdAt) > weekAgo
    }).length

    const categories = {}
    projects.value.forEach(project => {
      const category = project.template || '未分类'
      categories[category] = (categories[category] || 0) + 1
    })

    return {
      total,
      recent,
      categories
    }
  }

  // 搜索项目
  const searchProjects = (query) => {
    if (!query) return projects.value
    
    const lowerQuery = query.toLowerCase()
    return projects.value.filter(project => 
      project.title.toLowerCase().includes(lowerQuery) ||
      (project.template && project.template.toLowerCase().includes(lowerQuery))
    )
  }

  // 初始化
  const init = () => {
    loadFromLocalStorage()
  }

  return {
    // 状态
    projects,
    currentProject,
    projectHistory,
    historyIndex,
    
    // 计算属性
    hasProjects,
    canUndo,
    canRedo,
    
    // 方法
    saveProject,
    loadProject,
    deleteProject,
    updateProject,
    addToHistory,
    undo,
    redo,
    clearHistory,
    exportProject,
    clearAllData,
    getProjectStats,
    searchProjects,
    init
  }
}) 