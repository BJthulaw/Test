#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本
验证程序的基本功能
"""

import sys
import os
import json

# 添加utils目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

def test_imports():
    """测试导入功能"""
    print("=== 测试导入功能 ===")
    
    try:
        import tkinter as tk
        print("✓ tkinter导入成功")
    except Exception as e:
        print(f"✗ tkinter导入失败: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✓ matplotlib导入成功")
    except Exception as e:
        print(f"✗ matplotlib导入失败: {e}")
        return False
    
    try:
        from drawing_utils import DrawingUtils
        print("✓ DrawingUtils导入成功")
    except Exception as e:
        print(f"✗ DrawingUtils导入失败: {e}")
        return False
    
    return True

def test_templates():
    """测试模板加载功能"""
    print("\n=== 测试模板加载功能 ===")
    
    # 测试法学模板
    legal_template_path = os.path.join('templates', 'legal_templates.json')
    if os.path.exists(legal_template_path):
        try:
            with open(legal_template_path, 'r', encoding='utf-8') as f:
                legal_templates = json.load(f)
            print(f"✓ 法学模板加载成功，共{len(legal_templates)}个模板")
        except Exception as e:
            print(f"✗ 法学模板加载失败: {e}")
    else:
        print("✗ 法学模板文件不存在")
    
    # 测试学术论文模板
    academic_template_path = os.path.join('templates', 'academic_templates.json')
    if os.path.exists(academic_template_path):
        try:
            with open(academic_template_path, 'r', encoding='utf-8') as f:
                academic_templates = json.load(f)
            print(f"✓ 学术论文模板加载成功，共{len(academic_templates)}个模板")
        except Exception as e:
            print(f"✗ 学术论文模板加载失败: {e}")
    else:
        print("✗ 学术论文模板文件不存在")
    
    return True

def test_drawing_utils():
    """测试绘图工具功能"""
    print("\n=== 测试绘图工具功能 ===")
    
    try:
        from drawing_utils import DrawingUtils
        
        # 测试颜色调色板
        colors = DrawingUtils.get_color_palette('default')
        print(f"✓ 颜色调色板获取成功，共{len(colors)}种颜色")
        
        # 测试文本格式化
        text = "这是一个很长的文本需要被格式化处理"
        formatted = DrawingUtils.format_text(text, max_length=10)
        print(f"✓ 文本格式化成功: {formatted}")
        
        # 测试位置计算
        nodes = [{'id': f'node_{i}', 'text': f'节点{i}', 'level': i} for i in range(1, 4)]
        positions = DrawingUtils.calculate_hierarchy_positions(nodes)
        print(f"✓ 位置计算成功，共{len(positions)}个位置")
        
    except Exception as e:
        print(f"✗ 绘图工具测试失败: {e}")
        return False
    
    return True

def main():
    """主测试函数"""
    print("法学研究科研绘图工具 - 功能测试")
    print("=" * 50)
    
    # 测试导入
    if not test_imports():
        print("\n❌ 导入测试失败，程序无法正常运行")
        return
    
    # 测试模板
    if not test_templates():
        print("\n❌ 模板测试失败")
        return
    
    # 测试绘图工具
    if not test_drawing_utils():
        print("\n❌ 绘图工具测试失败")
        return
    
    print("\n✅ 所有测试通过！程序可以正常运行。")
    print("\n启动程序请运行: python main.py")
    print("或双击: run.bat")

if __name__ == "__main__":
    main() 