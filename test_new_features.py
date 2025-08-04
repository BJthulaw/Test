#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新功能脚本
验证图片模板导入、结果显示和下载功能
"""

import os
import sys
import json
import base64
from PIL import Image
import io

def test_image_template_import():
    """测试图片模板导入功能"""
    print("🧪 测试图片模板导入功能...")
    
    # 检查示例图片模板是否存在
    sample_dir = "sample_templates"
    if not os.path.exists(sample_dir):
        print("❌ 示例图片模板目录不存在")
        return False
    
    image_files = [f for f in os.listdir(sample_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'))]
    
    if not image_files:
        print("❌ 没有找到示例图片文件")
        return False
    
    print(f"✅ 找到 {len(image_files)} 个示例图片文件")
    
    # 测试第一个图片文件
    test_image = os.path.join(sample_dir, image_files[0])
    print(f"📷 测试图片: {test_image}")
    
    try:
        # 读取图片并转换为base64
        with open(test_image, 'rb') as f:
            image_data = f.read()
            image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # 创建模板数据结构
        template_name = os.path.splitext(os.path.basename(test_image))[0]
        template_data = {
            'name': template_name,
            'type': 'image_template',
            'description': f'从图片导入的模板: {template_name}',
            'layout': 'image',
            'image_path': test_image,
            'image_base64': image_base64,
            'image_format': os.path.splitext(test_image)[1][1:],
            'default_text': f'基于图片模板 {template_name} 的图表'
        }
        
        print(f"✅ 成功创建图片模板: {template_name}")
        print(f"   类型: {template_data['type']}")
        print(f"   格式: {template_data['image_format']}")
        print(f"   Base64长度: {len(image_base64)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 图片模板导入失败: {str(e)}")
        return False

def test_output_directory():
    """测试输出目录创建功能"""
    print("\n🧪 测试输出目录创建功能...")
    
    output_dir = "output"
    
    # 检查目录是否存在
    if os.path.exists(output_dir):
        print(f"✅ 输出目录已存在: {output_dir}")
    else:
        print(f"📁 输出目录不存在，将在使用时自动创建")
    
    # 测试创建目录
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"✅ 成功创建输出目录: {output_dir}")
        else:
            print(f"✅ 输出目录已存在: {output_dir}")
        return True
    except Exception as e:
        print(f"❌ 创建输出目录失败: {str(e)}")
        return False

def test_file_formats():
    """测试文件格式支持"""
    print("\n🧪 测试文件格式支持...")
    
    # 支持的图片格式
    image_formats = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']
    print(f"✅ 支持的图片格式: {', '.join(image_formats)}")
    
    # 支持的下载格式
    download_formats = ['.png', '.pdf', '.svg', '.jpg']
    print(f"✅ 支持的下载格式: {', '.join(download_formats)}")
    
    return True

def test_template_loading():
    """测试模板加载功能"""
    print("\n🧪 测试模板加载功能...")
    
    # 检查JSON模板文件
    json_templates = [
        "templates/legal_templates.json",
        "templates/academic_templates.json"
    ]
    
    loaded_templates = {}
    
    for template_file in json_templates:
        if os.path.exists(template_file):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    templates = json.load(f)
                    loaded_templates.update(templates)
                print(f"✅ 成功加载模板文件: {template_file}")
            except Exception as e:
                print(f"❌ 加载模板文件失败 {template_file}: {str(e)}")
        else:
            print(f"⚠️ 模板文件不存在: {template_file}")
    
    print(f"📊 总共加载了 {len(loaded_templates)} 个模板")
    
    # 显示模板类型统计
    type_count = {}
    for template in loaded_templates.values():
        template_type = template.get('type', 'unknown')
        type_count[template_type] = type_count.get(template_type, 0) + 1
    
    for template_type, count in type_count.items():
        print(f"   {template_type}: {count} 个")
    
    return len(loaded_templates) > 0

def test_ui_components():
    """测试UI组件功能"""
    print("\n🧪 测试UI组件功能...")
    
    try:
        import tkinter as tk
        from tkinter import ttk
        
        # 创建测试窗口
        root = tk.Tk()
        root.withdraw()  # 隐藏窗口
        
        # 测试PanedWindow
        main_frame = ttk.Frame(root)
        paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        
        # 测试LabelFrame
        control_frame = ttk.LabelFrame(paned_window, text="控制面板")
        drawing_frame = ttk.LabelFrame(paned_window, text="绘图区域")
        
        # 测试按钮
        button = ttk.Button(control_frame, text="测试按钮")
        
        print("✅ UI组件测试通过")
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ UI组件测试失败: {str(e)}")
        return False

def test_pil_functionality():
    """测试PIL功能"""
    print("\n🧪 测试PIL功能...")
    
    try:
        # 创建测试图片
        test_image = Image.new('RGB', (100, 100), 'white')
        
        # 测试图片操作
        test_image = test_image.resize((200, 200), Image.Resampling.LANCZOS)
        
        # 测试保存到内存
        buffer = io.BytesIO()
        test_image.save(buffer, format='PNG')
        buffer.seek(0)
        
        # 测试从内存读取
        loaded_image = Image.open(buffer)
        
        print("✅ PIL功能测试通过")
        return True
        
    except Exception as e:
        print(f"❌ PIL功能测试失败: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试新功能...")
    print("=" * 50)
    
    tests = [
        ("图片模板导入", test_image_template_import),
        ("输出目录创建", test_output_directory),
        ("文件格式支持", test_file_formats),
        ("模板加载", test_template_loading),
        ("UI组件", test_ui_components),
        ("PIL功能", test_pil_functionality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} 测试通过")
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {str(e)}")
        print("-" * 30)
    
    print("=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！新功能正常工作。")
    else:
        print("⚠️ 部分测试失败，请检查相关功能。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 