import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { aiApi } from '@/api/ai'

export const useAIStore = defineStore('ai', () => {
  // 状态
  const isEnabled = ref(true)
  const apiKey = ref(localStorage.getItem('ai_api_key') || '')
  const model = ref('qwen-turbo')
  const loading = ref(false)
  const error = ref('')
  const conversationHistory = ref([])
  const generatedResults = ref([])

  // 计算属性
  const isConfigured = computed(() => !!apiKey.value)
  const hasHistory = computed(() => conversationHistory.value.length > 0)
  const hasResults = computed(() => generatedResults.value.length > 0)

  // 设置API密钥
  const setApiKey = (key) => {
    apiKey.value = key
    localStorage.setItem('ai_api_key', key)
  }

  // 清除API密钥
  const clearApiKey = () => {
    apiKey.value = ''
    localStorage.removeItem('ai_api_key')
  }

  // 设置模型
  const setModel = (newModel) => {
    model.value = newModel
  }

  // 启用/禁用AI
  const toggleAI = (enabled) => {
    isEnabled.value = enabled
  }

  // 生成绘图内容
  const generateDrawing = async (prompt, templateId = null) => {
    if (!isEnabled.value) {
      throw new Error('AI功能已禁用')
    }

    if (!isConfigured.value) {
      throw new Error('请先配置AI API密钥')
    }

    loading.value = true
    error.value = ''

    try {
      const response = await aiApi.generateDrawing({
        prompt,
        templateId,
        model: model.value,
        apiKey: apiKey.value
      })

      const result = {
        id: Date.now().toString(),
        prompt,
        templateId,
        result: response.data,
        timestamp: new Date().toISOString()
      }

      generatedResults.value.push(result)
      conversationHistory.value.push({
        type: 'user',
        content: prompt,
        timestamp: new Date().toISOString()
      })

      conversationHistory.value.push({
        type: 'assistant',
        content: '已生成绘图内容',
        timestamp: new Date().toISOString()
      })

      return result
    } catch (err) {
      error.value = err.message || 'AI生成失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 分析文本结构
  const analyzeTextStructure = async (text) => {
    if (!isEnabled.value || !isConfigured.value) {
      return null
    }

    loading.value = true
    error.value = ''

    try {
      const response = await aiApi.analyzeText({
        text,
        model: model.value,
        apiKey: apiKey.value
      })

      return response.data
    } catch (err) {
      error.value = err.message || '文本分析失败'
      return null
    } finally {
      loading.value = false
    }
  }

  // 增强图表内容
  const enhanceContent = async (content, type = 'general') => {
    if (!isEnabled.value || !isConfigured.value) {
      return content
    }

    loading.value = true
    error.value = ''

    try {
      const response = await aiApi.enhanceContent({
        content,
        type,
        model: model.value,
        apiKey: apiKey.value
      })

      return response.data.enhancedContent
    } catch (err) {
      error.value = err.message || '内容增强失败'
      return content
    } finally {
      loading.value = false
    }
  }

  // 建议图表类型
  const suggestChartType = async (description) => {
    if (!isEnabled.value || !isConfigured.value) {
      return 'hierarchy'
    }

    loading.value = true
    error.value = ''

    try {
      const response = await aiApi.suggestChartType({
        description,
        model: model.value,
        apiKey: apiKey.value
      })

      return response.data.suggestedType
    } catch (err) {
      error.value = err.message || '图表类型建议失败'
      return 'hierarchy'
    } finally {
      loading.value = false
    }
  }

  // 优化配色方案
  const optimizeColors = async (chartData, style = 'academic') => {
    if (!isEnabled.value || !isConfigured.value) {
      return null
    }

    loading.value = true
    error.value = ''

    try {
      const response = await aiApi.optimizeColors({
        chartData,
        style,
        model: model.value,
        apiKey: apiKey.value
      })

      return response.data.colorScheme
    } catch (err) {
      error.value = err.message || '配色优化失败'
      return null
    } finally {
      loading.value = false
    }
  }

  // 生成图注和说明
  const generateCaption = async (chartData, language = 'zh-CN') => {
    if (!isEnabled.value || !isConfigured.value) {
      return ''
    }

    loading.value = true
    error.value = ''

    try {
      const response = await aiApi.generateCaption({
        chartData,
        language,
        model: model.value,
        apiKey: apiKey.value
      })

      return response.data.caption
    } catch (err) {
      error.value = err.message || '图注生成失败'
      return ''
    } finally {
      loading.value = false
    }
  }

  // 批量处理
  const batchProcess = async (tasks) => {
    if (!isEnabled.value || !isConfigured.value) {
      throw new Error('AI功能未配置')
    }

    loading.value = true
    error.value = ''

    try {
      const results = []
      for (const task of tasks) {
        try {
          const result = await processTask(task)
          results.push({ ...task, result, success: true })
        } catch (err) {
          results.push({ ...task, error: err.message, success: false })
        }
      }
      return results
    } catch (err) {
      error.value = err.message || '批量处理失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  // 处理单个任务
  const processTask = async (task) => {
    switch (task.type) {
      case 'generate':
        return await generateDrawing(task.prompt, task.templateId)
      case 'analyze':
        return await analyzeTextStructure(task.text)
      case 'enhance':
        return await enhanceContent(task.content, task.enhanceType)
      case 'suggest':
        return await suggestChartType(task.description)
      case 'optimize':
        return await optimizeColors(task.chartData, task.style)
      case 'caption':
        return await generateCaption(task.chartData, task.language)
      default:
        throw new Error(`未知任务类型: ${task.type}`)
    }
  }

  // 清空历史记录
  const clearHistory = () => {
    conversationHistory.value = []
  }

  // 清空生成结果
  const clearResults = () => {
    generatedResults.value = []
  }

  // 删除历史记录项
  const deleteHistoryItem = (index) => {
    conversationHistory.value.splice(index, 1)
  }

  // 删除生成结果
  const deleteResult = (id) => {
    const index = generatedResults.value.findIndex(r => r.id === id)
    if (index >= 0) {
      generatedResults.value.splice(index, 1)
    }
  }

  // 导出对话历史
  const exportHistory = (format = 'json') => {
    const data = {
      history: conversationHistory.value,
      results: generatedResults.value,
      exportTime: new Date().toISOString()
    }

    switch (format) {
      case 'json':
        return JSON.stringify(data, null, 2)
      case 'txt':
        return conversationHistory.value
          .map(item => `[${item.timestamp}] ${item.type}: ${item.content}`)
          .join('\n')
      case 'markdown':
        return generateMarkdown(data)
      default:
        return JSON.stringify(data, null, 2)
    }
  }

  // 生成Markdown格式
  const generateMarkdown = (data) => {
    let markdown = `# AI对话历史记录

导出时间: ${new Date(data.exportTime).toLocaleString()}

## 对话记录

`

    data.history.forEach((item, index) => {
      markdown += `### ${index + 1}. ${item.type === 'user' ? '用户' : 'AI助手'}\n\n`
      markdown += `**时间**: ${new Date(item.timestamp).toLocaleString()}\n\n`
      markdown += `${item.content}\n\n`
      markdown += '---\n\n'
    })

    if (data.results.length > 0) {
      markdown += `## 生成结果\n\n`
      data.results.forEach((result, index) => {
        markdown += `### ${index + 1}. ${result.prompt}\n\n`
        markdown += `**时间**: ${new Date(result.timestamp).toLocaleString()}\n\n`
        markdown += `**模板**: ${result.templateId || '无'}\n\n`
        markdown += `**结果**: ${JSON.stringify(result.result, null, 2)}\n\n`
        markdown += '---\n\n'
      })
    }

    return markdown
  }

  // 获取使用统计
  const getUsageStats = () => {
    const totalConversations = conversationHistory.value.filter(h => h.type === 'user').length
    const totalResults = generatedResults.value.length
    const recentActivity = conversationHistory.value.filter(h => {
      const weekAgo = new Date()
      weekAgo.setDate(weekAgo.getDate() - 7)
      return new Date(h.timestamp) > weekAgo
    }).length

    return {
      totalConversations,
      totalResults,
      recentActivity
    }
  }

  // 初始化
  const init = () => {
    // 从本地存储加载配置
    const savedApiKey = localStorage.getItem('ai_api_key')
    if (savedApiKey) {
      apiKey.value = savedApiKey
    }
  }

  return {
    // 状态
    isEnabled,
    apiKey,
    model,
    loading,
    error,
    conversationHistory,
    generatedResults,
    
    // 计算属性
    isConfigured,
    hasHistory,
    hasResults,
    
    // 方法
    setApiKey,
    clearApiKey,
    setModel,
    toggleAI,
    generateDrawing,
    analyzeTextStructure,
    enhanceContent,
    suggestChartType,
    optimizeColors,
    generateCaption,
    batchProcess,
    clearHistory,
    clearResults,
    deleteHistoryItem,
    deleteResult,
    exportHistory,
    getUsageStats,
    init
  }
}) 