#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
法学研究科研绘图工具 v3.0 - 增强版
支持线框逻辑图绘制、AI智能分析、多格式模板导入和结果下载
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np
import json
import os
from datetime import datetime
import sys
from PIL import Image, ImageTk
import base64
import io

# 添加utils目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
from drawing_utils import DrawingUtils
from ai_service import AlibabaCloudAIService

class LegalResearchDrawingTool:
    def __init__(self, root):
        self.root = root
        self.root.title("法学研究科研绘图工具 v3.0 - 增强版")
        self.root.geometry("1600x1000")
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 初始化变量
        self.current_template = None
        self.drawing_data = {}
        self.canvas = None
        self.figure = None
        self.ax = None
        self.current_diagram_path = None
        
        # 初始化AI服务
        self.ai_service = AlibabaCloudAIService("sk-4dbeb6767a574dff9eeef2c40e3acc96")
        self.ai_enabled = self.ai_service.is_available()
        
        self.setup_ui()
        self.load_templates()
        
    def setup_ui(self):
        """设置用户界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 顶部工具栏
        toolbar_frame = ttk.Frame(main_frame)
        toolbar_frame.pack(fill=tk.X, pady=(0, 5))
        
        # 快速操作按钮
        ttk.Button(toolbar_frame, text="🔄 刷新", command=self.refresh_interface).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar_frame, text="💾 快速保存", command=self.quick_save).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar_frame, text="📥 下载结果", command=self.download_result).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar_frame, text="📊 预览模板", command=self.preview_template).pack(side=tk.LEFT, padx=2)
        
        # 创建水平分割的主内容区域
        content_frame = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧控制面板
        control_frame = ttk.LabelFrame(content_frame, text="控制面板", padding=10)
        content_frame.add(control_frame, weight=1)
        
        # 模板选择区域
        template_frame = ttk.LabelFrame(control_frame, text="模板选择", padding=5)
        template_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(template_frame, text="选择模板:").pack(anchor=tk.W, pady=(0, 5))
        self.template_var = tk.StringVar()
        self.template_combo = ttk.Combobox(template_frame, textvariable=self.template_var, 
                                          state="readonly", width=25)
        self.template_combo.pack(fill=tk.X, pady=(0, 5))
        self.template_combo.bind('<<ComboboxSelected>>', self.on_template_selected)
        
        # 模板描述
        self.template_desc = tk.StringVar()
        ttk.Label(template_frame, textvariable=self.template_desc, 
                 wraplength=200, foreground='gray').pack(anchor=tk.W)
        
        # 文本输入区域
        text_frame = ttk.LabelFrame(control_frame, text="文本输入", padding=5)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        ttk.Label(text_frame, text="输入文本内容:").pack(anchor=tk.W, pady=(0, 5))
        self.text_input = scrolledtext.ScrolledText(text_frame, width=30, height=12)
        self.text_input.pack(fill=tk.BOTH, expand=True)
        
        # AI功能控制
        ai_frame = ttk.LabelFrame(control_frame, text="AI智能功能", padding=5)
        ai_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.ai_var = tk.BooleanVar(value=self.ai_enabled)
        self.ai_check = ttk.Checkbutton(ai_frame, text="启用AI分析", 
                                       variable=self.ai_var, state='normal' if self.ai_enabled else 'disabled')
        self.ai_check.pack(anchor=tk.W)
        
        ai_status = "✓ AI服务可用" if self.ai_enabled else "✗ AI服务不可用"
        ttk.Label(ai_frame, text=ai_status, foreground='green' if self.ai_enabled else 'red').pack(anchor=tk.W)
        
        # 操作按钮区域
        button_frame = ttk.LabelFrame(control_frame, text="操作面板", padding=5)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 第一行按钮
        btn_row1 = ttk.Frame(button_frame)
        btn_row1.pack(fill=tk.X, pady=2)
        ttk.Button(btn_row1, text="🎨 AI智能生成", command=self.generate_diagram).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
        ttk.Button(btn_row1, text="✨ AI内容增强", command=self.enhance_content).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
        
        # 第二行按钮
        btn_row2 = ttk.Frame(button_frame)
        btn_row2.pack(fill=tk.X, pady=2)
        ttk.Button(btn_row2, text="📁 导入模板", command=self.import_template).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
        ttk.Button(btn_row2, text="💾 保存图表", command=self.save_diagram).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
        
        # 第三行按钮
        btn_row3 = ttk.Frame(button_frame)
        btn_row3.pack(fill=tk.X, pady=2)
        ttk.Button(btn_row3, text="📤 导出模板", command=self.export_template).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
        ttk.Button(btn_row3, text="🗑️ 清空画布", command=self.clear_canvas).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
        
        # 右侧绘图区域
        drawing_frame = ttk.LabelFrame(content_frame, text="绘图预览区域", padding=10)
        content_frame.add(drawing_frame, weight=3)
        
        # 创建matplotlib图形
        self.figure, self.ax = plt.subplots(figsize=(14, 10))
        self.canvas = FigureCanvasTkAgg(self.figure, drawing_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 添加工具栏
        toolbar = NavigationToolbar2Tk(self.canvas, drawing_frame)
        toolbar.update()
        
        # 底部状态栏
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_var = tk.StringVar()
        self.status_var.set("就绪 - 请选择模板并输入文本内容")
        status_bar = ttk.Label(status_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 添加进度条
        self.progress_var = tk.StringVar()
        self.progress_var.set("")
        progress_label = ttk.Label(status_frame, textvariable=self.progress_var)
        progress_label.pack(side=tk.RIGHT, padx=5)
        
    def refresh_interface(self):
        """刷新界面"""
        self.load_templates()
        self.status_var.set("界面已刷新")
        
    def quick_save(self):
        """快速保存当前图表"""
        if not self.figure:
            messagebox.showwarning("警告", "没有可保存的图表")
            return
            
        # 自动生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        template_name = self.template_var.get() if self.template_var.get() else "图表"
        filename = f"{template_name}_{timestamp}.png"
        
        # 创建输出目录
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        file_path = os.path.join(output_dir, filename)
        
        try:
            self.figure.savefig(file_path, dpi=300, bbox_inches='tight', 
                              facecolor='white', edgecolor='none')
            self.current_diagram_path = file_path
            messagebox.showinfo("成功", f"图表已快速保存到: {file_path}")
            self.status_var.set(f"快速保存成功: {filename}")
        except Exception as e:
            messagebox.showerror("错误", f"快速保存失败: {str(e)}")
            
    def download_result(self):
        """下载生成结果"""
        if not self.current_diagram_path or not os.path.exists(self.current_diagram_path):
            messagebox.showwarning("警告", "没有可下载的结果，请先生成图表")
            return
            
        # 让用户选择下载位置
        file_path = filedialog.asksaveasfilename(
            initialname=os.path.basename(self.current_diagram_path),
            defaultextension=".png",
            filetypes=[
                ("PNG文件", "*.png"), 
                ("PDF文件", "*.pdf"), 
                ("SVG文件", "*.svg"),
                ("JPG文件", "*.jpg"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            try:
                # 根据选择的格式保存
                if file_path.lower().endswith('.pdf'):
                    self.figure.savefig(file_path, format='pdf', dpi=300, bbox_inches='tight')
                elif file_path.lower().endswith('.svg'):
                    self.figure.savefig(file_path, format='svg', dpi=300, bbox_inches='tight')
                elif file_path.lower().endswith('.jpg'):
                    self.figure.savefig(file_path, format='jpg', dpi=300, bbox_inches='tight')
                else:
                    # 复制原文件
                    import shutil
                    shutil.copy2(self.current_diagram_path, file_path)
                    
                messagebox.showinfo("成功", f"结果已下载到: {file_path}")
                self.status_var.set("下载完成")
            except Exception as e:
                messagebox.showerror("错误", f"下载失败: {str(e)}")
                
    def preview_template(self):
        """预览模板"""
        if not self.current_template:
            messagebox.showwarning("警告", "请先选择一个模板")
            return
            
        # 创建预览窗口
        preview_window = tk.Toplevel(self.root)
        preview_window.title(f"模板预览 - {self.template_var.get()}")
        preview_window.geometry("600x400")
        
        # 预览内容
        preview_text = f"""
模板名称: {self.template_var.get()}
模板类型: {self.current_template.get('type', '未知')}
描述: {self.current_template.get('description', '无描述')}
布局: {self.current_template.get('layout', '默认')}

默认文本:
{self.current_template.get('default_text', '无默认文本')}
        """
        
        text_widget = scrolledtext.ScrolledText(preview_window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert("1.0", preview_text)
        text_widget.config(state=tk.DISABLED)
        
    def load_templates(self):
        """加载内置模板"""
        self.templates = {}
        
        # 加载法学模板
        legal_template_path = os.path.join('templates', 'legal_templates.json')
        if os.path.exists(legal_template_path):
            try:
                with open(legal_template_path, 'r', encoding='utf-8') as f:
                    legal_templates = json.load(f)
                    self.templates.update(legal_templates)
            except Exception as e:
                print(f"加载法学模板文件失败: {e}")
        
        # 加载学术论文模板
        academic_template_path = os.path.join('templates', 'academic_templates.json')
        if os.path.exists(academic_template_path):
            try:
                with open(academic_template_path, 'r', encoding='utf-8') as f:
                    academic_templates = json.load(f)
                    self.templates.update(academic_templates)
            except Exception as e:
                print(f"加载学术论文模板文件失败: {e}")
        
        # 如果没有加载到任何模板，使用默认模板
        if not self.templates:
            self.templates = {
                "法律条文关系图": {
                    "type": "hierarchy",
                    "description": "展示法律条文之间的层级关系",
                    "layout": "vertical",
                    "default_text": "宪法\n基本法\n行政法规\n部门规章\n地方性法规"
                },
                "学术论文研究框架图": {
                    "type": "framework",
                    "description": "展示学术论文的研究框架和结构",
                    "layout": "grid",
                    "default_text": "研究背景\n文献综述\n理论框架\n研究方法\n数据分析\n结论建议"
                }
            }
        
        self.template_combo['values'] = list(self.templates.keys())
        if self.templates:
            self.template_combo.set(list(self.templates.keys())[0])
            
    def on_template_selected(self, event=None):
        """模板选择事件处理"""
        selected = self.template_var.get()
        if selected in self.templates:
            self.current_template = self.templates[selected]
            self.template_desc.set(self.current_template.get('description', '无描述'))
            self.status_var.set(f"已选择模板: {selected}")
            
            # 加载默认文本
            if 'default_text' in self.current_template:
                self.text_input.delete("1.0", tk.END)
                self.text_input.insert("1.0", self.current_template['default_text'])
                
    def generate_diagram(self):
        """生成图表"""
        if not self.current_template:
            messagebox.showwarning("警告", "请先选择一个模板")
            return
            
        text_content = self.text_input.get("1.0", tk.END).strip()
        if not text_content:
            messagebox.showwarning("警告", "请输入文本内容")
            return
            
        try:
            self.clear_canvas()
            self.progress_var.set("正在生成图表...")
            self.root.update()
            
            # 如果启用AI分析
            if self.ai_var.get() and self.ai_enabled:
                self.status_var.set("AI正在分析文本...")
                self.root.update()

                # AI分析文本结构
                ai_analysis = self.ai_service.analyze_text_structure(text_content)

                # 使用AI建议的图表类型
                if ai_analysis.get('suggested_type'):
                    template_type = ai_analysis['suggested_type']
                else:
                    template_type = self.current_template.get('type', 'hierarchy')

                # 使用AI增强的文本内容
                enhanced_text = ai_analysis.get('enhanced_text', text_content)
                if enhanced_text != text_content:
                    self.text_input.delete("1.0", tk.END)
                    self.text_input.insert("1.0", enhanced_text)
                    text_content = enhanced_text

                # 解析AI分析的结果
                parsed_data = self.parse_ai_analysis(ai_analysis)
            else:
                # 传统解析方法
                parsed_data = self.parse_text_content(text_content)
                template_type = self.current_template["type"]

            # 根据模板类型绘制图表
            if template_type == "image_template":
                self.draw_image_template_diagram(parsed_data)
            elif template_type == "hierarchy":
                self.draw_hierarchy_diagram(parsed_data)
            elif template_type == "flowchart":
                self.draw_flowchart_diagram(parsed_data)
            elif template_type == "network":
                self.draw_network_diagram(parsed_data)
            elif template_type == "decision_tree":
                self.draw_decision_tree_diagram(parsed_data)
            elif template_type == "framework":
                self.draw_framework_diagram(parsed_data)
            else:
                self.draw_hierarchy_diagram(parsed_data)

            # 更新画布
            self.canvas.draw()
            self.status_var.set("图表生成完成")
            self.progress_var.set("")
            
            # 自动快速保存
            self.quick_save()
            
        except Exception as e:
            messagebox.showerror("错误", f"生成图表失败: {str(e)}")
            self.status_var.set("生成失败")
            self.progress_var.set("")
            
    def parse_text_content(self, text):
        """解析文本内容"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # 简单的解析逻辑，可以根据需要扩展
        parsed_data = {
            'title': lines[0] if lines else "法学研究图表",
            'nodes': [],
            'connections': []
        }
        
        for i, line in enumerate(lines[1:], 1):
            if '->' in line or '→' in line:
                # 连接关系
                parts = line.replace('→', '->').split('->')
                if len(parts) == 2:
                    parsed_data['connections'].append({
                        'from': parts[0].strip(),
                        'to': parts[1].strip()
                    })
            else:
                # 节点
                parsed_data['nodes'].append({
                    'id': f"node_{i}",
                    'text': line,
                    'level': i
                })
                
        return parsed_data
    
    def parse_ai_analysis(self, ai_analysis):
        """解析AI分析结果"""
        parsed_data = {
            'title': "AI智能分析图表",
            'nodes': [],
            'connections': []
        }
        
        # 处理AI分析的概念
        concepts = ai_analysis.get('concepts', [])
        for i, concept in enumerate(concepts):
            if isinstance(concept, dict):
                node = {
                    'id': concept.get('id', f'node_{i}'),
                    'text': concept.get('text', str(concept)),
                    'level': concept.get('level', 1)
                }
            else:
                node = {
                    'id': f'node_{i}',
                    'text': str(concept),
                    'level': 1
                }
            parsed_data['nodes'].append(node)
        
        # 处理连接关系
        connections = ai_analysis.get('connections', [])
        for conn in connections:
            if isinstance(conn, dict):
                parsed_data['connections'].append({
                    'from': conn.get('from', ''),
                    'to': conn.get('to', ''),
                    'type': conn.get('type', 'simple'),
                    'label': conn.get('label', '')
                })
        
        return parsed_data
    
    def enhance_content(self):
        """AI内容增强"""
        if not self.ai_enabled:
            messagebox.showwarning("警告", "AI服务不可用")
            return
            
        text_content = self.text_input.get("1.0", tk.END).strip()
        if not text_content:
            messagebox.showwarning("警告", "请输入文本内容")
            return
        
        try:
            self.status_var.set("AI正在增强内容...")
            self.root.update()
            
            # 获取当前模板类型
            template_type = self.current_template.get('type', 'hierarchy') if self.current_template else 'hierarchy'
            
            # AI增强内容
            enhanced_text = self.ai_service.enhance_diagram_content(text_content, template_type)
            
            # 更新文本输入
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert("1.0", enhanced_text)
            
            self.status_var.set("AI内容增强完成")
            messagebox.showinfo("成功", "AI已成功增强内容，请重新生成图表")
            
        except Exception as e:
            messagebox.showerror("错误", f"AI内容增强失败: {str(e)}")
            self.status_var.set("AI内容增强失败")
        
    def draw_hierarchy_diagram(self, data):
        """绘制层级关系图"""
        self.ax.clear()
        
        nodes = data['nodes']
        connections = data['connections']
        
        # 计算节点位置
        levels = {}
        for node in nodes:
            level = node.get('level', 1)
            if level not in levels:
                levels[level] = []
            levels[level].append(node)
            
        # 绘制节点
        node_positions = {}
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        
        for level, level_nodes in levels.items():
            y = 10 - level * 2
            for i, node in enumerate(level_nodes):
                x = (i - len(level_nodes) / 2) * 3
                node_positions[node['id']] = (x, y)
                
                # 绘制节点框
                box = FancyBboxPatch((x-1.2, y-0.5), 2.4, 1, 
                                   boxstyle="round,pad=0.1", 
                                   facecolor=colors[level % len(colors)],
                                   edgecolor='black', linewidth=2)
                self.ax.add_patch(box)
                
                # 添加文本
                self.ax.text(x, y, node['text'], ha='center', va='center', 
                           fontsize=10, fontweight='bold')
                
        # 绘制连接线
        for conn in connections:
            from_node = conn.get('from', '')
            to_node = conn.get('to', '')
            conn_type = conn.get('type', 'simple')
            label = conn.get('label', '')
            
            # 查找节点位置
            from_pos = None
            to_pos = None
            
            for node in nodes:
                if node['text'] == from_node:
                    from_pos = node_positions.get(node['id'])
                elif node['text'] == to_node:
                    to_pos = node_positions.get(node['id'])
            
            if from_pos and to_pos:
                x1, y1 = from_pos
                x2, y2 = to_pos
                
                # 使用高级箭头绘制
                DrawingUtils.draw_advanced_arrow(
                    self.ax, x1, y1, x2, y2, 
                    arrow_type=conn_type, 
                    color='black', 
                    linewidth=2, 
                    label=label
                )
        
        # 如果没有明确的连接关系，使用层次连接
        if not connections and len(nodes) > 1:
            for i in range(len(nodes) - 1):
                pos1 = node_positions.get(nodes[i]['id'])
                pos2 = node_positions.get(nodes[i+1]['id'])
                if pos1 and pos2:
                    DrawingUtils.draw_hierarchical_connection(
                        self.ax, pos1, pos2, i+1, 'black', 2
                    )
                    
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(0, 12)
        self.ax.set_title(data['title'], fontsize=16, fontweight='bold', pad=20)
        self.ax.axis('off')
        
    def draw_flowchart_diagram(self, data):
        """绘制流程图"""
        self.ax.clear()
        
        nodes = data['nodes']
        
        # 绘制流程图
        for i, node in enumerate(nodes):
            x = 0
            y = 10 - i * 2
            
            # 绘制流程框
            if i == 0:  # 开始
                box = FancyBboxPatch((x-1.5, y-0.5), 3, 1, 
                                   boxstyle="round,pad=0.1", 
                                   facecolor='#90EE90', edgecolor='black', linewidth=2)
            elif i == len(nodes) - 1:  # 结束
                box = FancyBboxPatch((x-1.5, y-0.5), 3, 1, 
                                   boxstyle="round,pad=0.1", 
                                   facecolor='#FFB6C1', edgecolor='black', linewidth=2)
            else:  # 过程
                box = FancyBboxPatch((x-1.5, y-0.5), 3, 1, 
                                   boxstyle="round,pad=0.1", 
                                   facecolor='#87CEEB', edgecolor='black', linewidth=2)
                
            self.ax.add_patch(box)
            self.ax.text(x, y, node['text'], ha='center', va='center', 
                       fontsize=10, fontweight='bold')
            
            # 绘制箭头
            if i < len(nodes) - 1:
                DrawingUtils.draw_advanced_arrow(
                    self.ax, x, y+0.5, x, y-0.5, 
                    arrow_type='simple', 
                    color='black', 
                    linewidth=2
                )
                
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(0, 12)
        self.ax.set_title(data['title'], fontsize=16, fontweight='bold', pad=20)
        self.ax.axis('off')
        
    def draw_network_diagram(self, data):
        """绘制网络图"""
        self.ax.clear()
        
        nodes = data['nodes']
        
        # 计算节点位置（圆形布局）
        n = len(nodes)
        for i, node in enumerate(nodes):
            angle = 2 * np.pi * i / n
            x = 5 * np.cos(angle)
            y = 5 * np.sin(angle)
            
            # 绘制节点
            circle = patches.Circle((x, y), 1, facecolor='#FFD700', 
                                  edgecolor='black', linewidth=2)
            self.ax.add_patch(circle)
            
            # 添加文本
            self.ax.text(x, y, node['text'], ha='center', va='center', 
                       fontsize=9, fontweight='bold')
            
            # 绘制连接线
            if i < n - 1:
                next_angle = 2 * np.pi * (i + 1) / n
                next_x = 5 * np.cos(next_angle)
                next_y = 5 * np.sin(next_angle)
                
                DrawingUtils.draw_advanced_arrow(
                    self.ax, x, y, next_x, next_y, 
                    arrow_type='simple', 
                    color='black', 
                    linewidth=1
                )
                
        self.ax.set_xlim(-8, 8)
        self.ax.set_ylim(-8, 8)
        self.ax.set_title(data['title'], fontsize=16, fontweight='bold', pad=20)
        self.ax.axis('off')
        
    def draw_decision_tree_diagram(self, data):
        """绘制决策树"""
        self.ax.clear()
        
        nodes = data['nodes']
        
        # 绘制决策树
        for i, node in enumerate(nodes):
            x = 0
            y = 10 - i * 1.5
            
            # 绘制菱形（决策节点）
            if i % 2 == 0:
                diamond = patches.Polygon([(x-1, y), (x, y+0.5), (x+1, y), (x, y-0.5)], 
                                        facecolor='#FFA07A', edgecolor='black', linewidth=2)
                self.ax.add_patch(diamond)
            else:
                # 绘制矩形（结果节点）
                box = FancyBboxPatch((x-1, y-0.5), 2, 1, 
                                   boxstyle="round,pad=0.1", 
                                   facecolor='#98FB98', edgecolor='black', linewidth=2)
                self.ax.add_patch(box)
                
            self.ax.text(x, y, node['text'], ha='center', va='center', 
                       fontsize=9, fontweight='bold')
            
            # 绘制连接线
            if i < len(nodes) - 1:
                self.ax.annotate('', xy=(x, y-0.5), xytext=(x, y+0.5),
                               arrowprops=dict(arrowstyle='->', lw=2, color='black'))
                
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(0, 12)
        self.ax.set_title(data['title'], fontsize=16, fontweight='bold', pad=20)
        self.ax.axis('off')
        
    def draw_framework_diagram(self, data):
        """绘制框架图"""
        self.ax.clear()
        
        nodes = data['nodes']
        
        # 网格布局
        cols = 3
        rows = (len(nodes) + cols - 1) // cols
        
        for i, node in enumerate(nodes):
            row = i // cols
            col = i % cols
            
            x = (col - 1) * 4
            y = 8 - row * 2
            
            # 绘制框架框
            box = FancyBboxPatch((x-1.5, y-0.5), 3, 1, 
                               boxstyle="round,pad=0.1", 
                               facecolor='#E6E6FA', edgecolor='black', linewidth=2)
            self.ax.add_patch(box)
            
            # 添加文本
            self.ax.text(x, y, node['text'], ha='center', va='center', 
                       fontsize=9, fontweight='bold')
            
        self.ax.set_xlim(-6, 6)
        self.ax.set_ylim(0, 10)
        self.ax.set_title(data['title'], fontsize=16, fontweight='bold', pad=20)
        self.ax.axis('off')
        
    def draw_image_template_diagram(self, data):
        """绘制图片模板图表"""
        if not self.current_template or self.current_template.get('type') != 'image_template':
            return
            
        try:
            # 获取图片数据
            image_base64 = self.current_template.get('image_base64')
            if not image_base64:
                messagebox.showerror("错误", "图片模板数据不完整")
                return
                
            # 解码base64图片数据
            image_data = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_data))
            
            # 调整图片大小以适应画布
            fig_width, fig_height = self.figure.get_size_inches()
            dpi = self.figure.dpi
            canvas_width = fig_width * dpi
            canvas_height = fig_height * dpi
            
            # 计算图片显示尺寸
            img_width, img_height = image.size
            aspect_ratio = img_width / img_height
            canvas_aspect = canvas_width / canvas_height
            
            if aspect_ratio > canvas_aspect:
                # 图片更宽，以宽度为准
                display_width = canvas_width * 0.8
                display_height = display_width / aspect_ratio
            else:
                # 图片更高，以高度为准
                display_height = canvas_height * 0.8
                display_width = display_height * aspect_ratio
                
            # 调整图片大小
            image = image.resize((int(display_width), int(display_height)), Image.Resampling.LANCZOS)
            
            # 显示图片
            self.ax.imshow(image, extent=[-6, 6, -4, 4])
            
            # 添加标题
            title = data.get('title', '图片模板图表')
            self.ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            
            # 如果有文本内容，在图片下方显示
            if data.get('nodes'):
                text_content = '\n'.join([node['text'] for node in data['nodes']])
                self.ax.text(0, -5, text_content, ha='center', va='top', 
                           fontsize=10, bbox=dict(boxstyle="round,pad=0.5", 
                                                facecolor='lightblue', alpha=0.7))
            
            self.ax.set_xlim(-6, 6)
            self.ax.set_ylim(-6, 6)
            self.ax.axis('off')
            
        except Exception as e:
            messagebox.showerror("错误", f"绘制图片模板失败: {str(e)}")
        
    def save_diagram(self):
        """保存图表"""
        if not self.figure:
            messagebox.showwarning("警告", "没有可保存的图表")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG文件", "*.png"), ("PDF文件", "*.pdf"), ("SVG文件", "*.svg")]
        )
        
        if file_path:
            try:
                self.figure.savefig(file_path, dpi=300, bbox_inches='tight')
                messagebox.showinfo("成功", f"图表已保存到: {file_path}")
                self.status_var.set("图表保存成功")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")
                
    def import_template(self):
        """导入模板 - 支持JSON和图片格式"""
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("所有支持格式", "*.json;*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff"),
                ("JSON模板文件", "*.json"),
                ("图片模板文件", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            try:
                file_ext = os.path.splitext(file_path)[1].lower()
                
                if file_ext == '.json':
                    # 导入JSON模板
                    with open(file_path, 'r', encoding='utf-8') as f:
                        template_data = json.load(f)
                    
                    template_name = template_data.get('name', '导入的JSON模板')
                    self.templates[template_name] = template_data
                    
                elif file_ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']:
                    # 导入图片模板
                    template_name = os.path.splitext(os.path.basename(file_path))[0]
                    
                    # 读取图片并转换为base64
                    with open(file_path, 'rb') as f:
                        image_data = f.read()
                        image_base64 = base64.b64encode(image_data).decode('utf-8')
                    
                    # 创建图片模板数据结构
                    template_data = {
                        'name': template_name,
                        'type': 'image_template',
                        'description': f'从图片导入的模板: {template_name}',
                        'layout': 'image',
                        'image_path': file_path,
                        'image_base64': image_base64,
                        'image_format': file_ext[1:],  # 去掉点号
                        'default_text': f'基于图片模板 {template_name} 的图表'
                    }
                    
                    self.templates[template_name] = template_data
                    
                else:
                    messagebox.showerror("错误", f"不支持的文件格式: {file_ext}")
                    return
                
                # 更新下拉列表
                self.template_combo['values'] = list(self.templates.keys())
                self.template_combo.set(template_name)
                
                messagebox.showinfo("成功", f"模板 '{template_name}' 导入成功")
                self.status_var.set("模板导入成功")
                
            except Exception as e:
                messagebox.showerror("错误", f"导入模板失败: {str(e)}")
                
    def export_template(self):
        """导出模板"""
        if not self.current_template:
            messagebox.showwarning("警告", "没有可导出的模板")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json")]
        )
        
        if file_path:
            try:
                template_data = {
                    'name': self.template_var.get(),
                    **self.current_template
                }
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(template_data, f, ensure_ascii=False, indent=2)
                    
                messagebox.showinfo("成功", f"模板已导出到: {file_path}")
                self.status_var.set("模板导出成功")
                
            except Exception as e:
                messagebox.showerror("错误", f"导出模板失败: {str(e)}")
                
    def clear_canvas(self):
        """清空画布"""
        if self.ax:
            self.ax.clear()
            self.ax.set_xlim(0, 10)
            self.ax.set_ylim(0, 10)
            self.ax.axis('off')
            self.canvas.draw()
            self.status_var.set("画布已清空")

def main():
    root = tk.Tk()
    app = LegalResearchDrawingTool(root)
    root.mainloop()

if __name__ == "__main__":
    main() 