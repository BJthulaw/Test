#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试导入
"""

import sys
import os

# 添加utils目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

try:
    from drawing_utils import DrawingUtils
    print("DrawingUtils导入成功")
except Exception as e:
    print(f"DrawingUtils导入失败: {e}")

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog, scrolledtext
    print("tkinter模块导入成功")
except Exception as e:
    print(f"tkinter模块导入失败: {e}")

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    print("matplotlib模块导入成功")
except Exception as e:
    print(f"matplotlib模块导入失败: {e}")

try:
    import numpy as np
    print("numpy模块导入成功")
except Exception as e:
    print(f"numpy模块导入失败: {e}")

print("所有模块测试完成") 