#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI功能演示脚本
展示法学研究绘图工具的AI智能功能
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# 添加utils目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

def demo_ai_analysis():
    """演示AI文本分析功能"""
    print("=== AI文本分析演示 ===")
    
    try:
        from ai_service import AlibabaCloudAIService
        
        # 初始化AI服务
        ai_service = AlibabaCloudAIService("sk-4dbeb6767a574dff9eeef2c40e3acc96")
        
        # 测试文本
        test_texts = [
            "宪法\n基本法\n行政法规\n部门规章",
            "案件受理\n事实认定\n法律适用\n判决结果\n执行程序",
            "研究背景\n文献综述\n理论框架\n研究方法\n数据分析\n结论建议"
        ]
        
        for i, text in enumerate(test_texts, 1):
            print(f"\n--- 示例 {i} ---")
            print(f"输入文本:\n{text}")
            
            # AI分析
            analysis = ai_service.analyze_text_structure(text)
            print(f"AI建议图表类型: {analysis.get('suggested_type', '未知')}")
            print(f"AI增强内容:\n{analysis.get('enhanced_text', '无')}")
            
            # 内容增强
            enhanced = ai_service.enhance_diagram_content(text, "hierarchy")
            print(f"内容增强结果:\n{enhanced}")
            
    except Exception as e:
        print(f"AI演示失败: {e}")

def demo_advanced_connections():
    """演示高级连接语法"""
    print("\n=== 高级连接语法演示 ===")
    
    try:
        from drawing_utils import DrawingUtils
        
        # 测试连接解析
        test_connections = [
            "宪法 -> 基本法[制定依据]",
            "基本法 => 行政法规[实施细则]",
            "行政法规 --> 部门规章[具体实施]",
            "研究背景 ==> 文献综述[理论基础]",
            "文献综述 => 理论框架[核心概念]"
        ]
        
        connections = DrawingUtils.parse_advanced_connections('\n'.join(test_connections))
        
        print("解析的连接关系:")
        for conn in connections:
            print(f"  {conn['from']} --{conn['type']}--> {conn['to']} [{conn['label']}]")
            
    except Exception as e:
        print(f"连接语法演示失败: {e}")

def demo_main_application():
    """演示主应用程序"""
    print("\n=== 主应用程序演示 ===")
    
    try:
        # 创建测试窗口
        root = tk.Tk()
        root.withdraw()  # 隐藏窗口
        
        from main import LegalResearchDrawingTool
        
        # 创建应用实例
        app = LegalResearchDrawingTool(root)
        
        print(f"✓ 应用程序启动成功")
        print(f"✓ 加载模板数量: {len(app.templates)}")
        print(f"✓ AI服务状态: {'可用' if app.ai_enabled else '不可用'}")
        
        # 测试AI功能
        if app.ai_enabled:
            test_text = "宪法\n基本法\n行政法规"
            print(f"\n测试AI分析文本: {test_text}")
            
            # 模拟AI分析
            ai_analysis = app.ai_service.analyze_text_structure(test_text)
            print(f"AI分析完成，建议图表类型: {ai_analysis.get('suggested_type', '未知')}")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"主应用程序演示失败: {e}")
        return False

def show_feature_comparison():
    """显示功能对比"""
    print("\n=== 功能对比 ===")
    
    comparison = {
        "传统模式": [
            "手动解析文本",
            "固定图表类型",
            "简单箭头连接",
            "基础节点样式"
        ],
        "AI增强模式": [
            "智能文本分析",
            "自动图表类型建议",
            "多种箭头类型",
            "多层次节点支持",
            "智能连接识别",
            "内容自动增强"
        ]
    }
    
    for mode, features in comparison.items():
        print(f"\n{mode}:")
        for feature in features:
            print(f"  ✓ {feature}")

def main():
    """主演示函数"""
    print("🎯 法学研究科研绘图工具 v2.0 - AI功能演示")
    print("=" * 50)
    
    # 显示功能对比
    show_feature_comparison()
    
    # 演示AI分析
    demo_ai_analysis()
    
    # 演示高级连接语法
    demo_advanced_connections()
    
    # 演示主应用程序
    demo_main_application()
    
    print("\n" + "=" * 50)
    print("🎉 AI功能演示完成！")
    print("\n使用说明:")
    print("1. 运行 'python main.py' 启动主程序")
    print("2. 勾选'启用AI分析'复选框")
    print("3. 输入文本内容")
    print("4. 点击'AI智能生成'按钮")
    print("5. 体验AI智能功能！")

if __name__ == "__main__":
    main() 