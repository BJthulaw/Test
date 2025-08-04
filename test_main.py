#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试主程序
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import os

# 添加utils目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

try:
    from drawing_utils import DrawingUtils
    print("DrawingUtils导入成功")
except Exception as e:
    print(f"DrawingUtils导入失败: {e}")

def test_gui():
    """测试GUI"""
    root = tk.Tk()
    root.title("测试窗口")
    root.geometry("800x600")
    
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 创建matplotlib图形
    figure, ax = plt.subplots(figsize=(8, 6))
    canvas = FigureCanvasTkAgg(figure, root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # 测试绘图
    ax.clear()
    ax.text(0.5, 0.5, '测试绘图功能', ha='center', va='center', fontsize=16)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    canvas.draw()
    
    print("GUI测试成功")
    root.mainloop()

if __name__ == "__main__":
    test_gui() 