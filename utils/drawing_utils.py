#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
绘图工具类
提供各种绘图功能的辅助方法
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np
import json
import os

class DrawingUtils:
    """绘图工具类"""
    
    @staticmethod
    def create_text_box(ax, x, y, text, width=2.4, height=1, 
                       facecolor='#87CEEB', edgecolor='black', 
                       linewidth=2, fontsize=10, fontweight='bold'):
        """创建文本框"""
        box = FancyBboxPatch((x-width/2, y-height/2), width, height,
                           boxstyle="round,pad=0.1",
                           facecolor=facecolor,
                           edgecolor=edgecolor,
                           linewidth=linewidth)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center',
               fontsize=fontsize, fontweight=fontweight)
        return box
    
    @staticmethod
    def create_diamond(ax, x, y, text, size=1, facecolor='#FFA07A',
                      edgecolor='black', linewidth=2, fontsize=10, fontweight='bold'):
        """创建菱形（决策节点）"""
        diamond = patches.Polygon([(x-size, y), (x, y+size/2), 
                                  (x+size, y), (x, y-size/2)],
                                facecolor=facecolor,
                                edgecolor=edgecolor,
                                linewidth=linewidth)
        ax.add_patch(diamond)
        ax.text(x, y, text, ha='center', va='center',
               fontsize=fontsize, fontweight=fontweight)
        return diamond
    
    @staticmethod
    def create_circle(ax, x, y, text, radius=1, facecolor='#FFD700',
                     edgecolor='black', linewidth=2, fontsize=10, fontweight='bold'):
        """创建圆形节点"""
        circle = patches.Circle((x, y), radius, facecolor=facecolor,
                          edgecolor=edgecolor, linewidth=linewidth)
        ax.add_patch(circle)
        ax.text(x, y, text, ha='center', va='center',
               fontsize=fontsize, fontweight=fontweight)
        return circle
    
    @staticmethod
    def draw_arrow(ax, x1, y1, x2, y2, color='black', linewidth=2, 
                  arrowstyle='->', connectionstyle='arc3'):
        """绘制箭头"""
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle=arrowstyle, lw=linewidth, 
                                 color=color, connectionstyle=connectionstyle))
    
    @staticmethod
    def draw_line(ax, x1, y1, x2, y2, color='black', linewidth=1, linestyle='-'):
        """绘制直线"""
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=linewidth, linestyle=linestyle)
    
    @staticmethod
    def calculate_hierarchy_positions(nodes, max_width=10, max_height=12):
        """计算层级图节点位置"""
        positions = {}
        levels = {}
        
        # 按层级分组
        for node in nodes:
            level = node.get('level', 1)
            if level not in levels:
                levels[level] = []
            levels[level].append(node)
        
        # 计算位置
        for level, level_nodes in levels.items():
            y = max_height - level * 2
            for i, node in enumerate(level_nodes):
                x = (i - len(level_nodes) / 2) * (max_width / max(len(levels), 1))
                positions[node['id']] = (x, y)
        
        return positions
    
    @staticmethod
    def calculate_flowchart_positions(nodes, direction='vertical'):
        """计算流程图节点位置"""
        positions = {}
        
        if direction == 'vertical':
            for i, node in enumerate(nodes):
                x = 0
                y = 10 - i * 2
                positions[node['id']] = (x, y)
        else:  # horizontal
            for i, node in enumerate(nodes):
                x = i * 3 - (len(nodes) - 1) * 1.5
                y = 0
                positions[node['id']] = (x, y)
        
        return positions
    
    @staticmethod
    def calculate_network_positions(nodes, layout='circular'):
        """计算网络图节点位置"""
        positions = {}
        n = len(nodes)
        
        if layout == 'circular':
            radius = 5
            for i, node in enumerate(nodes):
                angle = 2 * np.pi * i / n
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                positions[node['id']] = (x, y)
        elif layout == 'grid':
            cols = int(np.ceil(np.sqrt(n)))
            for i, node in enumerate(nodes):
                row = i // cols
                col = i % cols
                x = (col - cols/2) * 3
                y = (rows/2 - row) * 2
                positions[node['id']] = (x, y)
        
        return positions
    
    @staticmethod
    def calculate_tree_positions(nodes):
        """计算树形图节点位置"""
        positions = {}
        
        for i, node in enumerate(nodes):
            x = 0
            y = 10 - i * 1.5
            positions[node['id']] = (x, y)
        
        return positions
    
    @staticmethod
    def calculate_framework_positions(nodes, cols=3):
        """计算框架图节点位置"""
        positions = {}
        rows = (len(nodes) + cols - 1) // cols
        
        for i, node in enumerate(nodes):
            row = i // cols
            col = i % cols
            x = (col - (cols-1)/2) * 4
            y = (rows-1)/2 - row * 2
            positions[node['id']] = (x, y)
        
        return positions
    
    @staticmethod
    def parse_connections(text):
        """解析连接关系"""
        connections = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if '->' in line or '→' in line:
                parts = line.replace('→', '->').split('->')
                if len(parts) == 2:
                    connections.append({
                        'from': parts[0].strip(),
                        'to': parts[1].strip()
                    })
        
        return connections
    
    @staticmethod
    def load_template(template_name):
        """加载模板"""
        template_path = os.path.join('templates', 'legal_templates.json')
        
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                templates = json.load(f)
                return templates.get(template_name)
        
        return None
    
    @staticmethod
    def save_template(template_name, template_data):
        """保存模板"""
        template_path = os.path.join('templates', 'legal_templates.json')
        
        # 确保目录存在
        os.makedirs(os.path.dirname(template_path), exist_ok=True)
        
        # 加载现有模板
        templates = {}
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                templates = json.load(f)
        
        # 添加新模板
        templates[template_name] = template_data
        
        # 保存
        with open(template_path, 'w', encoding='utf-8') as f:
            json.dump(templates, f, ensure_ascii=False, indent=2)
    
    @staticmethod
    def get_color_palette(palette_name='default'):
        """获取颜色调色板"""
        palettes = {
            'default': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'],
            'legal': ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#592E83'],
            'professional': ['#34495E', '#3498DB', '#E74C3C', '#2ECC71', '#F39C12'],
            'pastel': ['#FFB3BA', '#BAFFC9', '#BAE1FF', '#FFFFBA', '#FFB3F7']
        }
        
        return palettes.get(palette_name, palettes['default'])
    
    @staticmethod
    def format_text(text, max_length=20):
        """格式化文本，处理长文本"""
        if len(text) <= max_length:
            return text
        
        # 简单的文本换行处理
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + word) <= max_length:
                current_line += word + " "
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        return '\n'.join(lines)
    
    @staticmethod
    def draw_advanced_arrow(ax, x1, y1, x2, y2, arrow_type='simple', 
                           color='black', linewidth=2, label='', 
                           connection_style='arc3,rad=0.1'):
        """绘制高级箭头，支持多种箭头类型"""
        arrow_styles = {
            'simple': '->',
            'thick': '->',
            'double': '<->',
            'curved': '->',
            'dashed': '->',
            'dotted': '->'
        }
        
        linestyles = {
            'simple': '-',
            'thick': '-',
            'double': '-',
            'curved': '-',
            'dashed': '--',
            'dotted': ':'
        }
        
        arrowstyle = arrow_styles.get(arrow_type, '->')
        linestyle = linestyles.get(arrow_type, '-')
        
        # 绘制箭头
        if arrow_type == 'curved':
            connection_style = 'arc3,rad=0.2'
        
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle=arrowstyle, lw=linewidth, 
                                 color=color, connectionstyle=connection_style,
                                 linestyle=linestyle))
        
        # 添加标签
        if label:
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            if arrow_type == 'curved':
                mid_y += 0.3
            ax.text(mid_x, mid_y, label, ha='center', va='center',
                   fontsize=8, bbox=dict(boxstyle='round,pad=0.2', 
                                       facecolor='white', alpha=0.8))
    
    @staticmethod
    def draw_hierarchical_connection(ax, parent_pos, child_pos, level, 
                                   color='black', linewidth=2):
        """绘制层次连接线"""
        x1, y1 = parent_pos
        x2, y2 = child_pos
        
        # 垂直连接线
        ax.plot([x1, x1], [y1, y2], color=color, linewidth=linewidth, linestyle='-')
        # 水平连接线
        ax.plot([x1, x2], [y2, y2], color=color, linewidth=linewidth, linestyle='-')
        # 箭头
        ax.annotate('', xy=(x2, y2), xytext=(x2-0.3, y2),
                   arrowprops=dict(arrowstyle='->', lw=linewidth, color=color))
    
    @staticmethod
    def create_multi_level_node(ax, x, y, text, levels=1, node_type='box',
                               colors=None, fontsize=10):
        """创建多层次节点"""
        if colors is None:
            colors = ['#87CEEB', '#FFA07A', '#FFD700', '#98FB98']
        
        if node_type == 'box':
            width = 2.4
            height = 1.2 * levels
            for i in range(levels):
                y_offset = y + (levels - 1 - i) * 0.6
                box = FancyBboxPatch((x-width/2, y_offset-height/levels/2), 
                                   width, height/levels,
                                   boxstyle="round,pad=0.1",
                                   facecolor=colors[i % len(colors)],
                                   edgecolor='black', linewidth=1)
                ax.add_patch(box)
            
            # 添加文本
            ax.text(x, y, text, ha='center', va='center',
                   fontsize=fontsize, fontweight='bold')
        
        elif node_type == 'circle':
            radius = 1.2
            for i in range(levels):
                y_offset = y + (levels - 1 - i) * 0.8
                circle = patches.Circle((x, y_offset), radius/levels,
                                      facecolor=colors[i % len(colors)],
                                      edgecolor='black', linewidth=1)
                ax.add_patch(circle)
            
            ax.text(x, y, text, ha='center', va='center',
                   fontsize=fontsize, fontweight='bold')
    
    @staticmethod
    def parse_advanced_connections(text):
        """解析高级连接关系，支持多种连接类型"""
        connections = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 支持多种连接符号
            connection_symbols = ['->', '→', '=>', '⇒', '-->', '--->', '==>']
            connection_type = 'simple'
            
            for symbol in connection_symbols:
                if symbol in line:
                    parts = line.split(symbol)
                    if len(parts) == 2:
                        # 检测连接类型
                        if symbol in ['=>', '⇒']:
                            connection_type = 'thick'
                        elif symbol in ['-->', '--->']:
                            connection_type = 'dashed'
                        elif symbol in ['==>']:
                            connection_type = 'double'
                        
                        # 提取标签
                        label = ''
                        from_text = parts[0].strip()
                        to_text = parts[1].strip()
                        
                        # 检查是否有标签
                        if '[' in to_text and ']' in to_text:
                            label_start = to_text.find('[')
                            label_end = to_text.find(']')
                            label = to_text[label_start+1:label_end]
                            to_text = to_text[:label_start].strip()
                        
                        connections.append({
                            'from': from_text,
                            'to': to_text,
                            'type': connection_type,
                            'label': label
                        })
                    break
        
        return connections
    
    @staticmethod
    def create_connection_matrix(nodes):
        """创建连接矩阵"""
        n = len(nodes)
        matrix = [[0] * n for _ in range(n)]
        node_ids = [node['id'] for node in nodes]
        
        return matrix, node_ids
    
    @staticmethod
    def apply_connections_to_matrix(matrix, node_ids, connections):
        """将连接关系应用到矩阵"""
        for conn in connections:
            try:
                from_idx = node_ids.index(conn['from'])
                to_idx = node_ids.index(conn['to'])
                matrix[from_idx][to_idx] = 1
            except ValueError:
                continue
        
        return matrix 