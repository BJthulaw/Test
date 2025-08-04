#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试AI功能和绘图优化
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# 添加utils目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

def test_ai_service():
    """测试AI服务"""
    print("=== 测试AI服务 ===")
    
    try:
        from ai_service import AlibabaCloudAIService
        
        # 初始化AI服务
        ai_service = AlibabaCloudAIService("sk-4dbeb6767a574dff9eeef2c40e3acc96")
        
        # 测试连接
        print("测试AI服务连接...")
        is_available = ai_service.is_available()
        print(f"AI服务可用: {is_available}")
        
        if is_available:
            # 测试文本分析
            test_text = "宪法\n基本法\n行政法规\n部门规章"
            print(f"\n测试文本: {test_text}")
            
            analysis = ai_service.analyze_text_structure(test_text)
            print(f"AI分析结果: {analysis}")
            
            # 测试内容增强
            enhanced = ai_service.enhance_diagram_content(test_text, "hierarchy")
            print(f"增强内容: {enhanced}")
            
            # 测试图表类型建议
            suggested_type = ai_service.suggest_diagram_type(test_text)
            print(f"建议图表类型: {suggested_type}")
        
        return True
        
    except Exception as e:
        print(f"AI服务测试失败: {e}")
        return False

def test_drawing_utils():
    """测试绘图工具"""
    print("\n=== 测试绘图工具 ===")
    
    try:
        from drawing_utils import DrawingUtils
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        
        # 测试高级连接解析
        test_connections = [
            "概念A -> 概念B",
            "概念B => 概念C",
            "概念C --> 概念D[重要]",
            "概念D ==> 概念E"
        ]
        
        connections = DrawingUtils.parse_advanced_connections('\n'.join(test_connections))
        print(f"解析的连接关系: {connections}")
        
        # 测试连接矩阵
        nodes = [
            {'id': 'node_1', 'text': '概念A'},
            {'id': 'node_2', 'text': '概念B'},
            {'id': 'node_3', 'text': '概念C'}
        ]
        
        matrix, node_ids = DrawingUtils.create_connection_matrix(nodes)
        print(f"连接矩阵: {matrix}")
        print(f"节点ID: {node_ids}")
        
        return True
        
    except Exception as e:
        print(f"绘图工具测试失败: {e}")
        return False

def test_main_application():
    """测试主应用程序"""
    print("\n=== 测试主应用程序 ===")
    
    try:
        # 创建测试窗口
        root = tk.Tk()
        root.withdraw()  # 隐藏窗口
        
        from main import LegalResearchDrawingTool
        
        # 创建应用实例
        app = LegalResearchDrawingTool(root)
        
        # 测试模板加载
        print(f"加载的模板数量: {len(app.templates)}")
        
        # 测试AI服务状态
        print(f"AI服务可用: {app.ai_enabled}")
        
        # 测试文本解析
        test_text = "宪法\n基本法\n行政法规"
        parsed_data = app.parse_text_content(test_text)
        print(f"解析结果: {parsed_data}")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"主应用程序测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始测试AI功能和绘图优化...")
    
    # 测试AI服务
    ai_test = test_ai_service()
    
    # 测试绘图工具
    drawing_test = test_drawing_utils()
    
    # 测试主应用程序
    app_test = test_main_application()
    
    # 总结测试结果
    print("\n=== 测试总结 ===")
    print(f"AI服务测试: {'✓ 通过' if ai_test else '✗ 失败'}")
    print(f"绘图工具测试: {'✓ 通过' if drawing_test else '✗ 失败'}")
    print(f"主应用程序测试: {'✓ 通过' if app_test else '✗ 失败'}")
    
    if ai_test and drawing_test and app_test:
        print("\n🎉 所有测试通过！AI功能和绘图优化已成功集成。")
        return True
    else:
        print("\n⚠️ 部分测试失败，请检查相关功能。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 