#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建示例图片模板
用于测试图片模板导入功能
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_image_templates():
    """创建示例图片模板"""
    
    # 创建输出目录
    output_dir = "sample_templates"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 模板1: 法律流程图
    create_legal_flowchart_template(output_dir)
    
    # 模板2: 学术研究框架
    create_academic_framework_template(output_dir)
    
    # 模板3: 决策树模板
    create_decision_tree_template(output_dir)
    
    print("示例图片模板创建完成！")

def create_legal_flowchart_template(output_dir):
    """创建法律流程图模板"""
    # 创建画布
    width, height = 800, 600
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # 绘制标题
    title = "法律流程图模板"
    draw.text((width//2, 30), title, fill='black', anchor='mm')
    
    # 绘制流程图元素
    boxes = [
        (100, 100, 300, 150, "法律问题"),
        (100, 200, 300, 250, "法律分析"),
        (100, 300, 300, 350, "法律适用"),
        (100, 400, 300, 450, "结论"),
        (400, 150, 600, 200, "相关法条"),
        (400, 250, 600, 300, "判例参考"),
        (400, 350, 600, 400, "专家意见")
    ]
    
    for x1, y1, x2, y2, text in boxes:
        # 绘制矩形
        draw.rectangle([x1, y1, x2, y2], outline='blue', width=2)
        # 绘制文本
        draw.text(((x1+x2)//2, (y1+y2)//2), text, fill='black', anchor='mm')
    
    # 绘制连接线
    arrows = [
        ((300, 125), (400, 175)),  # 问题 -> 法条
        ((300, 225), (400, 275)),  # 分析 -> 判例
        ((300, 325), (400, 375)),  # 适用 -> 意见
    ]
    
    for start, end in arrows:
        draw.line([start, end], fill='red', width=2)
        # 绘制箭头
        draw_arrow(draw, start, end)
    
    # 保存图片
    file_path = os.path.join(output_dir, "法律流程图模板.png")
    image.save(file_path)
    print(f"创建模板: {file_path}")

def create_academic_framework_template(output_dir):
    """创建学术研究框架模板"""
    # 创建画布
    width, height = 800, 600
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # 绘制标题
    title = "学术研究框架模板"
    draw.text((width//2, 30), title, fill='black', anchor='mm')
    
    # 绘制框架元素
    boxes = [
        (50, 80, 350, 130, "研究背景"),
        (450, 80, 750, 130, "文献综述"),
        (50, 180, 350, 230, "理论框架"),
        (450, 180, 750, 230, "研究方法"),
        (50, 280, 350, 330, "数据分析"),
        (450, 280, 750, 330, "结论建议"),
        (250, 380, 550, 430, "研究贡献"),
        (250, 480, 550, 530, "未来展望")
    ]
    
    for x1, y1, x2, y2, text in boxes:
        # 绘制圆角矩形
        draw_rounded_rectangle(draw, x1, y1, x2, y2, 'lightblue', 'blue', 10)
        # 绘制文本
        draw.text(((x1+x2)//2, (y1+y2)//2), text, fill='black', anchor='mm')
    
    # 保存图片
    file_path = os.path.join(output_dir, "学术研究框架模板.png")
    image.save(file_path)
    print(f"创建模板: {file_path}")

def create_decision_tree_template(output_dir):
    """创建决策树模板"""
    # 创建画布
    width, height = 800, 600
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # 绘制标题
    title = "决策树模板"
    draw.text((width//2, 30), title, fill='black', anchor='mm')
    
    # 绘制决策树节点
    nodes = [
        (400, 100, "决策点", 'diamond'),
        (200, 200, "选项A", 'circle'),
        (600, 200, "选项B", 'circle'),
        (100, 300, "结果A1", 'box'),
        (300, 300, "结果A2", 'box'),
        (500, 300, "结果B1", 'box'),
        (700, 300, "结果B2", 'box')
    ]
    
    for x, y, text, shape in nodes:
        if shape == 'diamond':
            draw_diamond(draw, x, y, 60, 'lightgreen', 'green')
        elif shape == 'circle':
            draw_circle(draw, x, y, 40, 'lightyellow', 'orange')
        else:  # box
            draw.rectangle([x-50, y-20, x+50, y+20], fill='lightpink', outline='red')
        
        draw.text((x, y), text, fill='black', anchor='mm')
    
    # 绘制连接线
    connections = [
        ((400, 100), (200, 200), "是"),
        ((400, 100), (600, 200), "否"),
        ((200, 200), (100, 300), "条件1"),
        ((200, 200), (300, 300), "条件2"),
        ((600, 200), (500, 300), "条件3"),
        ((600, 200), (700, 300), "条件4")
    ]
    
    for start, end, label in connections:
        draw.line([start, end], fill='gray', width=2)
        # 在连接线中点添加标签
        mid_x = (start[0] + end[0]) // 2
        mid_y = (start[1] + end[1]) // 2
        draw.text((mid_x, mid_y), label, fill='blue', anchor='mm')
    
    # 保存图片
    file_path = os.path.join(output_dir, "决策树模板.png")
    image.save(file_path)
    print(f"创建模板: {file_path}")

def draw_arrow(draw, start, end):
    """绘制箭头"""
    # 计算箭头方向
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    
    # 箭头长度和角度
    arrow_length = 15
    angle = 30  # 度
    
    # 计算箭头点
    import math
    angle_rad = math.atan2(dy, dx)
    
    # 箭头尖端
    tip_x = end[0] - arrow_length * math.cos(angle_rad)
    tip_y = end[1] - arrow_length * math.sin(angle_rad)
    
    # 箭头两侧
    left_x = tip_x - arrow_length * math.cos(angle_rad + math.radians(angle))
    left_y = tip_y - arrow_length * math.sin(angle_rad + math.radians(angle))
    
    right_x = tip_x - arrow_length * math.cos(angle_rad - math.radians(angle))
    right_y = tip_y - arrow_length * math.sin(angle_rad - math.radians(angle))
    
    # 绘制箭头
    draw.polygon([end, (left_x, left_y), (right_x, right_y)], fill='red')

def draw_rounded_rectangle(draw, x1, y1, x2, y2, fill_color, outline_color, radius):
    """绘制圆角矩形"""
    # 绘制填充
    draw.rectangle([x1, y1, x2, y2], fill=fill_color)
    # 绘制边框
    draw.rectangle([x1, y1, x2, y2], outline=outline_color, width=2)

def draw_diamond(draw, x, y, size, fill_color, outline_color):
    """绘制菱形"""
    points = [
        (x, y - size//2),  # 上
        (x + size//2, y),  # 右
        (x, y + size//2),  # 下
        (x - size//2, y)   # 左
    ]
    draw.polygon(points, fill=fill_color, outline=outline_color)

def draw_circle(draw, x, y, radius, fill_color, outline_color):
    """绘制圆形"""
    draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                fill=fill_color, outline=outline_color)

if __name__ == "__main__":
    create_sample_image_templates() 