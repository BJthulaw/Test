<template>
  <div class="drawing-page">
    <!-- 导航栏 -->
    <nav-header />
    
    <!-- 主要内容 -->
    <div class="drawing-container">
      <!-- 左侧工具栏 -->
      <div class="toolbar-panel">
        <div class="toolbar-section">
          <h3 class="section-title">模板选择</h3>
          <el-select 
            v-model="selectedTemplate" 
            placeholder="选择模板"
            @change="onTemplateChange"
            style="width: 100%"
          >
            <el-option
              v-for="template in templates"
              :key="template.id"
              :label="template.name"
              :value="template.id"
            >
              <div class="template-option">
                <img :src="template.thumbnail" :alt="template.name" />
                <div class="template-info">
                  <div class="template-name">{{ template.name }}</div>
                  <div class="template-category">{{ template.category }}</div>
                </div>
              </div>
            </el-option>
          </el-select>
        </div>

        <div class="toolbar-section">
          <h3 class="section-title">绘图工具</h3>
          <div class="tool-buttons">
            <el-button-group>
              <el-button @click="setTool('select')" :type="currentTool === 'select' ? 'primary' : ''">
                <el-icon><Pointer /></el-icon>
                选择
              </el-button>
              <el-button @click="setTool('text')" :type="currentTool === 'text' ? 'primary' : ''">
                <el-icon><Edit /></el-icon>
                文本
              </el-button>
              <el-button @click="setTool('shape')" :type="currentTool === 'shape' ? 'primary' : ''">
                <el-icon><Box /></el-icon>
                形状
              </el-button>
              <el-button @click="setTool('line')" :type="currentTool === 'line' ? 'primary' : ''">
                <el-icon><Connection /></el-icon>
                连线
              </el-button>
            </el-button-group>
          </div>
        </div>

        <div class="toolbar-section">
          <h3 class="section-title">样式设置</h3>
          <div class="style-controls">
            <div class="control-item">
              <label>字体大小</label>
              <el-slider v-model="textSize" :min="12" :max="72" />
            </div>
            <div class="control-item">
              <label>线条粗细</label>
              <el-slider v-model="lineWidth" :min="1" :max="10" />
            </div>
            <div class="control-item">
              <label>填充颜色</label>
              <el-color-picker v-model="fillColor" />
            </div>
            <div class="control-item">
              <label>边框颜色</label>
              <el-color-picker v-model="strokeColor" />
            </div>
          </div>
        </div>

        <div class="toolbar-section">
          <h3 class="section-title">AI助手</h3>
          <div class="ai-controls">
            <el-switch v-model="aiEnabled" active-text="启用AI" />
            <el-button 
              v-if="aiEnabled" 
              type="primary" 
              size="small" 
              @click="generateWithAI"
              :loading="aiLoading"
            >
              <el-icon><MagicStick /></el-icon>
              AI生成
            </el-button>
          </div>
          <el-input
            v-if="aiEnabled"
            v-model="aiPrompt"
            type="textarea"
            placeholder="描述您想要生成的图表内容..."
            :rows="3"
            style="margin-top: 10px"
          />
        </div>

        <div class="toolbar-section">
          <h3 class="section-title">操作</h3>
          <div class="action-buttons">
            <el-button @click="undo" :disabled="!canUndo">
              <el-icon><RefreshLeft /></el-icon>
              撤销
            </el-button>
            <el-button @click="redo" :disabled="!canRedo">
              <el-icon><RefreshRight /></el-icon>
              重做
            </el-button>
            <el-button @click="clearCanvas">
              <el-icon><Delete /></el-icon>
              清空
            </el-button>
          </div>
        </div>
      </div>

      <!-- 中央绘图区域 -->
      <div class="canvas-panel">
        <div class="canvas-header">
          <div class="canvas-title">
            <el-input v-model="canvasTitle" placeholder="图表标题" />
          </div>
          <div class="canvas-actions">
            <el-button @click="saveProject">
              <el-icon><FolderAdd /></el-icon>
              保存
            </el-button>
            <el-button @click="exportImage">
              <el-icon><Download /></el-icon>
              导出
            </el-button>
            <el-button @click="previewCanvas">
              <el-icon><View /></el-icon>
              预览
            </el-button>
          </div>
        </div>
        
        <div class="canvas-container">
          <canvas 
            ref="canvasRef"
            class="drawing-canvas"
            @mousedown="onMouseDown"
            @mousemove="onMouseMove"
            @mouseup="onMouseUp"
            @wheel="onWheel"
          ></canvas>
        </div>

        <div class="canvas-footer">
          <div class="zoom-controls">
            <el-button @click="zoomOut" :disabled="zoom <= 0.5">
              <el-icon><ZoomOut /></el-icon>
            </el-button>
            <span class="zoom-level">{{ Math.round(zoom * 100) }}%</span>
            <el-button @click="zoomIn" :disabled="zoom >= 3">
              <el-icon><ZoomIn /></el-icon>
            </el-button>
            <el-button @click="resetZoom">
              <el-icon><FullScreen /></el-icon>
            </el-button>
          </div>
        </div>
      </div>

      <!-- 右侧属性面板 -->
      <div class="properties-panel">
        <div class="properties-section">
          <h3 class="section-title">元素属性</h3>
          <div v-if="selectedElement" class="element-properties">
            <div class="property-item">
              <label>位置 X</label>
              <el-input-number v-model="selectedElement.left" @change="updateElement" />
            </div>
            <div class="property-item">
              <label>位置 Y</label>
              <el-input-number v-model="selectedElement.top" @change="updateElement" />
            </div>
            <div class="property-item">
              <label>宽度</label>
              <el-input-number v-model="selectedElement.width" @change="updateElement" />
            </div>
            <div class="property-item">
              <label>高度</label>
              <el-input-number v-model="selectedElement.height" @change="updateElement" />
            </div>
            <div class="property-item">
              <label>旋转</label>
              <el-slider v-model="selectedElement.angle" :min="0" :max="360" @change="updateElement" />
            </div>
            <div class="property-item">
              <label>透明度</label>
              <el-slider v-model="selectedElement.opacity" :min="0" :max="1" :step="0.1" @change="updateElement" />
            </div>
          </div>
          <div v-else class="no-selection">
            <el-icon><InfoFilled /></el-icon>
            <p>选择一个元素查看属性</p>
          </div>
        </div>

        <div class="properties-section">
          <h3 class="section-title">图层管理</h3>
          <div class="layers-list">
            <div 
              v-for="(layer, index) in layers" 
              :key="layer.id"
              class="layer-item"
              :class="{ 'active': selectedElement?.id === layer.id }"
              @click="selectLayer(layer)"
            >
              <div class="layer-info">
                <el-icon><component :is="layer.icon" /></el-icon>
                <span>{{ layer.name }}</span>
              </div>
              <div class="layer-actions">
                <el-button size="small" @click="moveLayer(index, -1)" :disabled="index === 0">
                  <el-icon><ArrowUp /></el-icon>
                </el-button>
                <el-button size="small" @click="moveLayer(index, 1)" :disabled="index === layers.length - 1">
                  <el-icon><ArrowDown /></el-icon>
                </el-button>
                <el-button size="small" @click="deleteLayer(layer)" type="danger">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 导出对话框 -->
    <el-dialog v-model="exportDialogVisible" title="导出图表" width="500px">
      <div class="export-options">
        <div class="export-format">
          <label>导出格式</label>
          <el-radio-group v-model="exportFormat">
            <el-radio label="png">PNG</el-radio>
            <el-radio label="jpg">JPG</el-radio>
            <el-radio label="pdf">PDF</el-radio>
            <el-radio label="svg">SVG</el-radio>
          </el-radio-group>
        </div>
        <div class="export-size">
          <label>导出尺寸</label>
          <el-select v-model="exportSize">
            <el-option label="原始尺寸" value="original" />
            <el-option label="A4纸张" value="a4" />
            <el-option label="自定义" value="custom" />
          </el-select>
        </div>
        <div v-if="exportSize === 'custom'" class="custom-size">
          <el-input-number v-model="customWidth" placeholder="宽度" />
          <span>×</span>
          <el-input-number v-model="customHeight" placeholder="高度" />
        </div>
      </div>
      <template #footer>
        <el-button @click="exportDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmExport">导出</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { fabric } from 'fabric'
import NavHeader from '@/components/layout/NavHeader.vue'
import { useDrawingStore } from '@/store/drawing'
import { useAIStore } from '@/store/ai'

const router = useRouter()
const drawingStore = useDrawingStore()
const aiStore = useAIStore()

// 画布相关
const canvasRef = ref(null)
const canvas = ref(null)

// 工具状态
const currentTool = ref('select')
const selectedTemplate = ref(null)
const canvasTitle = ref('')

// 样式控制
const textSize = ref(16)
const lineWidth = ref(2)
const fillColor = ref('#409EFF')
const strokeColor = ref('#000000')

// AI功能
const aiEnabled = ref(false)
const aiLoading = ref(false)
const aiPrompt = ref('')

// 缩放控制
const zoom = ref(1)
const canUndo = ref(false)
const canRedo = ref(false)

// 选中元素
const selectedElement = ref(null)
const layers = ref([])

// 导出相关
const exportDialogVisible = ref(false)
const exportFormat = ref('png')
const exportSize = ref('original')
const customWidth = ref(800)
const customHeight = ref(600)

// 模板数据
const templates = ref([
  {
    id: 1,
    name: '法律问题分析流程图',
    category: '流程图',
    thumbnail: '/templates/legal-flowchart.png'
  },
  {
    id: 2,
    name: '司法程序流程图',
    category: '流程图',
    thumbnail: '/templates/judicial-process.png'
  },
  {
    id: 3,
    name: '法律条文适用范围图',
    category: '示意图',
    thumbnail: '/templates/legal-scope.png'
  }
])

// 初始化画布
const initCanvas = () => {
  canvas.value = new fabric.Canvas(canvasRef.value, {
    width: 800,
    height: 600,
    backgroundColor: '#ffffff'
  })

  // 监听选择事件
  canvas.value.on('selection:created', onSelectionCreated)
  canvas.value.on('selection:cleared', onSelectionCleared)
  canvas.value.on('object:modified', onObjectModified)

  // 加载默认模板
  if (templates.value.length > 0) {
    selectedTemplate.value = templates.value[0].id
    loadTemplate(templates.value[0])
  }
}

// 工具设置
const setTool = (tool) => {
  currentTool.value = tool
  canvas.value.isDrawingMode = tool === 'line'
  
  if (tool === 'select') {
    canvas.value.defaultCursor = 'default'
  } else {
    canvas.value.defaultCursor = 'crosshair'
  }
}

// 模板相关
const onTemplateChange = (templateId) => {
  const template = templates.value.find(t => t.id === templateId)
  if (template) {
    loadTemplate(template)
  }
}

const loadTemplate = (template) => {
  // 清空画布
  canvas.value.clear()
  
  // 加载模板内容
  // 这里可以根据模板类型加载不同的预设内容
  addTemplateContent(template)
  
  // 更新图层列表
  updateLayers()
}

const addTemplateContent = (template) => {
  // 添加标题
  const title = new fabric.Text(template.name, {
    left: 50,
    top: 30,
    fontSize: 24,
    fontFamily: 'Arial',
    fill: '#333333'
  })
  canvas.value.add(title)
  
  // 根据模板类型添加不同的预设内容
  if (template.category === '流程图') {
    addFlowchartElements()
  } else if (template.category === '示意图') {
    addDiagramElements()
  }
}

const addFlowchartElements = () => {
  // 添加流程图元素
  const elements = [
    { text: '开始', left: 350, top: 50 },
    { text: '分析问题', left: 350, top: 150 },
    { text: '查找法条', left: 200, top: 250 },
    { text: '适用法律', left: 500, top: 250 },
    { text: '得出结论', left: 350, top: 350 },
    { text: '结束', left: 350, top: 450 }
  ]
  
  elements.forEach((el, index) => {
    const rect = new fabric.Rect({
      left: el.left,
      top: el.top,
      width: 120,
      height: 60,
      fill: '#e3f2fd',
      stroke: '#1976d2',
      strokeWidth: 2,
      rx: 8,
      ry: 8
    })
    
    const text = new fabric.Text(el.text, {
      left: el.left + 60,
      top: el.top + 30,
      fontSize: 14,
      fontFamily: 'Arial',
      fill: '#333333',
      originX: 'center',
      originY: 'center'
    })
    
    canvas.value.add(rect)
    canvas.value.add(text)
    
    // 添加连接线
    if (index < elements.length - 1) {
      const line = new fabric.Line([
        el.left + 60, el.top + 60,
        elements[index + 1].left + 60, elements[index + 1].top
      ], {
        stroke: '#666666',
        strokeWidth: 2,
        selectable: false
      })
      canvas.value.add(line)
    }
  })
}

const addDiagramElements = () => {
  // 添加示意图元素
  const circle = new fabric.Circle({
    left: 400,
    top: 300,
    radius: 100,
    fill: '#ffebee',
    stroke: '#f44336',
    strokeWidth: 3
  })
  
  const text = new fabric.Text('核心概念', {
    left: 400,
    top: 300,
    fontSize: 18,
    fontFamily: 'Arial',
    fill: '#333333',
    originX: 'center',
    originY: 'center'
  })
  
  canvas.value.add(circle)
  canvas.value.add(text)
}

// 鼠标事件处理
const onMouseDown = (e) => {
  if (currentTool.value === 'text') {
    addText(e)
  } else if (currentTool.value === 'shape') {
    addShape(e)
  }
}

const onMouseMove = (e) => {
  // 处理绘制过程
}

const onMouseUp = (e) => {
  // 完成绘制
}

const onWheel = (e) => {
  e.preventDefault()
  const delta = e.deltaY > 0 ? 0.9 : 1.1
  zoom.value = Math.max(0.5, Math.min(3, zoom.value * delta))
  canvas.value.setZoom(zoom.value)
}

// 添加元素
const addText = (e) => {
  const pointer = canvas.value.getPointer(e)
  const text = new fabric.IText('双击编辑文本', {
    left: pointer.x,
    top: pointer.y,
    fontSize: textSize.value,
    fontFamily: 'Arial',
    fill: fillColor.value
  })
  canvas.value.add(text)
  canvas.value.setActiveObject(text)
  updateLayers()
}

const addShape = (e) => {
  const pointer = canvas.value.getPointer(e)
  const rect = new fabric.Rect({
    left: pointer.x,
    top: pointer.y,
    width: 100,
    height: 60,
    fill: fillColor.value,
    stroke: strokeColor.value,
    strokeWidth: lineWidth.value
  })
  canvas.value.add(rect)
  canvas.value.setActiveObject(rect)
  updateLayers()
}

// 选择事件处理
const onSelectionCreated = (e) => {
  selectedElement.value = e.target
}

const onSelectionCleared = () => {
  selectedElement.value = null
}

const onObjectModified = () => {
  updateLayers()
}

// 更新元素
const updateElement = () => {
  if (selectedElement.value) {
    canvas.value.renderAll()
  }
}

// 图层管理
const updateLayers = () => {
  layers.value = canvas.value.getObjects().map((obj, index) => ({
    id: obj.id || index,
    name: obj.text || `${obj.type} ${index + 1}`,
    icon: getLayerIcon(obj.type),
    object: obj
  }))
}

const getLayerIcon = (type) => {
  const icons = {
    'text': 'Edit',
    'rect': 'Box',
    'circle': 'CircleCheck',
    'line': 'Connection',
    'path': 'Crop'
  }
  return icons[type] || 'Box'
}

const selectLayer = (layer) => {
  canvas.value.setActiveObject(layer.object)
}

const moveLayer = (index, direction) => {
  const newIndex = index + direction
  if (newIndex >= 0 && newIndex < layers.value.length) {
    const obj = layers.value[index].object
    canvas.value.moveTo(obj, newIndex)
    updateLayers()
  }
}

const deleteLayer = (layer) => {
  canvas.value.remove(layer.object)
  updateLayers()
}

// 操作功能
const undo = () => {
  // 实现撤销功能
}

const redo = () => {
  // 实现重做功能
}

const clearCanvas = async () => {
  try {
    await ElMessageBox.confirm('确定要清空画布吗？', '提示', {
      type: 'warning'
    })
    canvas.value.clear()
    updateLayers()
  } catch {
    // 用户取消
  }
}

// AI功能
const generateWithAI = async () => {
  if (!aiPrompt.value.trim()) {
    ElMessage.warning('请输入描述内容')
    return
  }
  
  aiLoading.value = true
  try {
    const result = await aiStore.generateDrawing(aiPrompt.value, selectedTemplate.value)
    // 处理AI生成的结果
    applyAIGeneratedContent(result)
    ElMessage.success('AI生成完成')
  } catch (error) {
    ElMessage.error('AI生成失败：' + error.message)
  } finally {
    aiLoading.value = false
  }
}

const applyAIGeneratedContent = (result) => {
  // 应用AI生成的内容到画布
  // 这里需要根据AI返回的数据结构来实现
}

// 保存和导出
const saveProject = () => {
  const projectData = {
    title: canvasTitle.value,
    template: selectedTemplate.value,
    canvas: canvas.value.toJSON(),
    timestamp: new Date().toISOString()
  }
  
  drawingStore.saveProject(projectData)
  ElMessage.success('项目已保存')
}

const exportImage = () => {
  exportDialogVisible.value = true
}

const confirmExport = () => {
  const dataURL = canvas.value.toDataURL({
    format: exportFormat.value,
    quality: 1
  })
  
  const link = document.createElement('a')
  link.download = `${canvasTitle.value || '图表'}.${exportFormat.value}`
  link.href = dataURL
  link.click()
  
  exportDialogVisible.value = false
  ElMessage.success('导出成功')
}

const previewCanvas = () => {
  // 实现预览功能
}

// 缩放控制
const zoomIn = () => {
  zoom.value = Math.min(3, zoom.value * 1.2)
  canvas.value.setZoom(zoom.value)
}

const zoomOut = () => {
  zoom.value = Math.max(0.5, zoom.value / 1.2)
  canvas.value.setZoom(zoom.value)
}

const resetZoom = () => {
  zoom.value = 1
  canvas.value.setZoom(1)
  canvas.value.setViewportTransform([1, 0, 0, 1, 0, 0])
}

// 生命周期
onMounted(async () => {
  await nextTick()
  initCanvas()
})

onUnmounted(() => {
  if (canvas.value) {
    canvas.value.dispose()
  }
})
</script>

<style lang="scss" scoped>
.drawing-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.drawing-container {
  flex: 1;
  display: flex;
  margin-top: 64px;
  height: calc(100vh - 64px);
}

// 左侧工具栏
.toolbar-panel {
  width: 280px;
  background: var(--el-bg-color);
  border-right: 1px solid var(--el-border-color-lighter);
  padding: 20px;
  overflow-y: auto;

  .toolbar-section {
    margin-bottom: 30px;

    .section-title {
      font-size: 16px;
      font-weight: 600;
      margin-bottom: 15px;
      color: var(--el-text-color-primary);
    }

    .tool-buttons {
      .el-button-group {
        width: 100%;
        
        .el-button {
          flex: 1;
        }
      }
    }

    .style-controls {
      .control-item {
        margin-bottom: 15px;

        label {
          display: block;
          margin-bottom: 5px;
          font-size: 14px;
          color: var(--el-text-color-regular);
        }
      }
    }

    .ai-controls {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 10px;
    }

    .action-buttons {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;

      .el-button {
        flex: 1;
        min-width: 0;
      }
    }
  }
}

// 中央绘图区域
.canvas-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--el-fill-color-lighter);

  .canvas-header {
    padding: 15px 20px;
    background: var(--el-bg-color);
    border-bottom: 1px solid var(--el-border-color-lighter);
    display: flex;
    justify-content: space-between;
    align-items: center;

    .canvas-title {
      flex: 1;
      max-width: 300px;
    }

    .canvas-actions {
      display: flex;
      gap: 10px;
    }
  }

  .canvas-container {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    overflow: auto;

    .drawing-canvas {
      border: 1px solid var(--el-border-color);
      background: white;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
  }

  .canvas-footer {
    padding: 10px 20px;
    background: var(--el-bg-color);
    border-top: 1px solid var(--el-border-color-lighter);

    .zoom-controls {
      display: flex;
      align-items: center;
      gap: 10px;

      .zoom-level {
        min-width: 60px;
        text-align: center;
        font-size: 14px;
        color: var(--el-text-color-regular);
      }
    }
  }
}

// 右侧属性面板
.properties-panel {
  width: 280px;
  background: var(--el-bg-color);
  border-left: 1px solid var(--el-border-color-lighter);
  padding: 20px;
  overflow-y: auto;

  .properties-section {
    margin-bottom: 30px;

    .section-title {
      font-size: 16px;
      font-weight: 600;
      margin-bottom: 15px;
      color: var(--el-text-color-primary);
    }

    .element-properties {
      .property-item {
        margin-bottom: 15px;

        label {
          display: block;
          margin-bottom: 5px;
          font-size: 14px;
          color: var(--el-text-color-regular);
        }

        .el-input-number {
          width: 100%;
        }
      }
    }

    .no-selection {
      text-align: center;
      color: var(--el-text-color-placeholder);
      padding: 40px 0;

      .el-icon {
        font-size: 48px;
        margin-bottom: 10px;
      }
    }

    .layers-list {
      .layer-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px;
        border-radius: 6px;
        cursor: pointer;
        transition: background-color 0.2s ease;

        &:hover {
          background: var(--el-fill-color-light);
        }

        &.active {
          background: var(--el-color-primary-light-9);
          color: var(--el-color-primary);
        }

        .layer-info {
          display: flex;
          align-items: center;
          gap: 8px;
          flex: 1;
        }

        .layer-actions {
          display: flex;
          gap: 4px;
        }
      }
    }
  }
}

// 模板选项样式
.template-option {
  display: flex;
  align-items: center;
  gap: 10px;

  img {
    width: 40px;
    height: 30px;
    object-fit: cover;
    border-radius: 4px;
  }

  .template-info {
    flex: 1;

    .template-name {
      font-weight: 500;
    }

    .template-category {
      font-size: 12px;
      color: var(--el-text-color-placeholder);
    }
  }
}

// 导出对话框
.export-options {
  .export-format,
  .export-size {
    margin-bottom: 20px;

    label {
      display: block;
      margin-bottom: 10px;
      font-weight: 500;
    }
  }

  .custom-size {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 10px;

    span {
      color: var(--el-text-color-regular);
    }
  }
}

// 响应式设计
@media (max-width: 1200px) {
  .toolbar-panel,
  .properties-panel {
    width: 240px;
  }
}

@media (max-width: 768px) {
  .drawing-container {
    flex-direction: column;
  }

  .toolbar-panel,
  .properties-panel {
    width: 100%;
    height: auto;
    max-height: 200px;
  }

  .canvas-panel {
    flex: 1;
  }
}
</style> 