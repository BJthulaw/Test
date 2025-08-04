import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: '/api/ai',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 添加API密钥到请求头
    if (config.data?.apiKey) {
      config.headers['Authorization'] = `Bearer ${config.data.apiKey}`
      delete config.data.apiKey
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response) {
      // 服务器返回错误状态码
      const { status, data } = error.response
      switch (status) {
        case 401:
          throw new Error('API密钥无效或已过期')
        case 403:
          throw new Error('没有权限访问此服务')
        case 429:
          throw new Error('请求过于频繁，请稍后再试')
        case 500:
          throw new Error('服务器内部错误')
        default:
          throw new Error(data?.message || `请求失败 (${status})`)
      }
    } else if (error.request) {
      // 网络错误
      throw new Error('网络连接失败，请检查网络设置')
    } else {
      // 其他错误
      throw new Error(error.message || '未知错误')
    }
  }
)

// AI API接口
export const aiApi = {
  // 生成绘图内容
  generateDrawing: async (params) => {
    const response = await api.post('/generate-drawing', {
      prompt: params.prompt,
      templateId: params.templateId,
      model: params.model || 'qwen-turbo',
      options: {
        style: 'academic',
        format: 'json',
        includeMetadata: true
      }
    })
    return response
  },

  // 分析文本结构
  analyzeText: async (params) => {
    const response = await api.post('/analyze-text', {
      text: params.text,
      model: params.model || 'qwen-turbo',
      analysisType: 'structure',
      options: {
        extractEntities: true,
        identifyRelationships: true,
        suggestLayout: true
      }
    })
    return response
  },

  // 增强图表内容
  enhanceContent: async (params) => {
    const response = await api.post('/enhance-content', {
      content: params.content,
      type: params.type || 'general',
      model: params.model || 'qwen-turbo',
      options: {
        improveClarity: true,
        addDetails: true,
        optimizeStructure: true
      }
    })
    return response
  },

  // 建议图表类型
  suggestChartType: async (params) => {
    const response = await api.post('/suggest-chart-type', {
      description: params.description,
      model: params.model || 'qwen-turbo',
      options: {
        considerContext: true,
        suggestAlternatives: true
      }
    })
    return response
  },

  // 优化配色方案
  optimizeColors: async (params) => {
    const response = await api.post('/optimize-colors', {
      chartData: params.chartData,
      style: params.style || 'academic',
      model: params.model || 'qwen-turbo',
      options: {
        accessibility: true,
        printFriendly: true,
        brandConsistency: false
      }
    })
    return response
  },

  // 生成图注和说明
  generateCaption: async (params) => {
    const response = await api.post('/generate-caption', {
      chartData: params.chartData,
      language: params.language || 'zh-CN',
      model: params.model || 'qwen-turbo',
      options: {
        includeTitle: true,
        includeDescription: true,
        includeNotes: true,
        academicStyle: true
      }
    })
    return response
  },

  // 批量处理
  batchProcess: async (params) => {
    const response = await api.post('/batch-process', {
      tasks: params.tasks,
      model: params.model || 'qwen-turbo',
      options: {
        parallel: false,
        retryOnError: true,
        maxRetries: 3
      }
    })
    return response
  },

  // 获取模型列表
  getModels: async () => {
    const response = await api.get('/models')
    return response
  },

  // 检查API状态
  checkStatus: async () => {
    const response = await api.get('/status')
    return response
  },

  // 获取使用统计
  getUsageStats: async () => {
    const response = await api.get('/usage-stats')
    return response
  }
}

// 模拟API响应（用于开发环境）
const mockResponses = {
  generateDrawing: {
    data: {
      nodes: [
        { id: 1, text: '法律问题', x: 100, y: 100, type: 'rectangle' },
        { id: 2, text: '法律分析', x: 100, y: 200, type: 'rectangle' },
        { id: 3, text: '法律适用', x: 100, y: 300, type: 'rectangle' }
      ],
      connections: [
        { from: 1, to: 2, type: 'arrow' },
        { from: 2, to: 3, type: 'arrow' }
      ],
      style: {
        primaryColor: '#1976d2',
        secondaryColor: '#e3f2fd',
        fontFamily: 'Arial',
        fontSize: 14
      }
    }
  },
  analyzeText: {
    data: {
      structure: 'hierarchy',
      entities: ['法律问题', '法律分析', '法律适用'],
      relationships: [
        { from: '法律问题', to: '法律分析', type: 'leads_to' },
        { from: '法律分析', to: '法律适用', type: 'leads_to' }
      ],
      suggestedLayout: 'vertical_flow'
    }
  },
  enhanceContent: {
    data: {
      enhancedContent: '基于法律问题的分析框架，包括问题识别、法律分析和法律适用三个主要阶段。'
    }
  },
  suggestChartType: {
    data: {
      suggestedType: 'flowchart',
      confidence: 0.85,
      alternatives: ['hierarchy', 'timeline']
    }
  },
  optimizeColors: {
    data: {
      colorScheme: {
        primary: '#1976d2',
        secondary: '#e3f2fd',
        accent: '#ff9800',
        background: '#ffffff',
        text: '#333333'
      }
    }
  },
  generateCaption: {
    data: {
      caption: '图1 法律问题分析流程图\n\n本图展示了法律问题分析的基本流程，包括问题识别、法律分析和法律适用三个主要阶段。'
    }
  }
}

// 开发环境下的模拟API
if (process.env.NODE_ENV === 'development') {
  // 重写API方法以返回模拟数据
  Object.keys(aiApi).forEach(method => {
    if (mockResponses[method]) {
      const originalMethod = aiApi[method]
      aiApi[method] = async (params) => {
        // 模拟网络延迟
        await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000))
        
        // 模拟错误（10%概率）
        if (Math.random() < 0.1) {
          throw new Error('模拟API错误')
        }
        
        return {
          data: mockResponses[method].data,
          status: 200,
          statusText: 'OK'
        }
      }
    }
  })
}

export default aiApi 