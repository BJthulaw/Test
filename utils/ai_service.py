#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI服务模块
集成阿里云API进行文本理解和转换
"""

import requests
import json
import time
import hashlib
import base64
import hmac
from urllib.parse import urlencode
import logging

class AlibabaCloudAIService:
    """阿里云AI服务类"""
    
    def __init__(self, api_key, region='cn-hangzhou'):
        self.api_key = api_key
        self.region = region
        self.base_url = f"https://dashscope.aliyuncs.com/api/v1"
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # 设置日志
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def analyze_text_structure(self, text):
        """分析文本结构，提取层次关系和逻辑连接"""
        try:
            prompt = f"""
请分析以下文本的结构和逻辑关系，提取出：
1. 主要概念和节点
2. 概念之间的层次关系
3. 逻辑连接和流程
4. 建议的图表类型

文本内容：
{text}

请以JSON格式返回分析结果，包含以下字段：
{{
    "concepts": [节点列表],
    "hierarchy": [层次关系],
    "connections": [连接关系],
    "suggested_type": "建议的图表类型",
    "enhanced_text": "优化后的文本内容"
}}
"""
            
            response = self._call_llm_api(prompt)
            if response:
                return json.loads(response)
            else:
                return self._fallback_analysis(text)
                
        except Exception as e:
            self.logger.error(f"AI分析失败: {e}")
            return self._fallback_analysis(text)
    
    def enhance_diagram_content(self, original_text, diagram_type):
        """增强图表内容，添加更多细节和逻辑关系"""
        try:
            prompt = f"""
请基于以下原始文本和图表类型，生成更详细和结构化的内容：

原始文本：{original_text}
图表类型：{diagram_type}

要求：
1. 保持原有核心概念
2. 添加逻辑连接词和关系
3. 补充缺失的中间步骤
4. 优化文本表达
5. 添加箭头和连接符号

请返回优化后的文本内容。
"""
            
            response = self._call_llm_api(prompt)
            if response:
                return response.strip()
            else:
                return original_text
                
        except Exception as e:
            self.logger.error(f"内容增强失败: {e}")
            return original_text
    
    def suggest_diagram_type(self, text):
        """根据文本内容建议合适的图表类型"""
        try:
            prompt = f"""
请分析以下文本内容，建议最合适的图表类型：

文本内容：{text}

可选图表类型：
- hierarchy: 层级关系图
- flowchart: 流程图
- network: 网络关系图
- decision_tree: 决策树
- framework: 框架图

请返回图表类型名称。
"""
            
            response = self._call_llm_api(prompt)
            if response:
                return response.strip().lower()
            else:
                return "hierarchy"
                
        except Exception as e:
            self.logger.error(f"图表类型建议失败: {e}")
            return "hierarchy"
    
    def _call_llm_api(self, prompt):
        """调用阿里云LLM API"""
        try:
            url = f"{self.base_url}/services/aigc/text-generation/generation"
            
            data = {
                "model": "qwen-turbo",
                "input": {
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                },
                "parameters": {
                    "temperature": 0.7,
                    "max_tokens": 2000
                }
            }
            
            response = requests.post(url, headers=self.headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if 'output' in result and 'text' in result['output']:
                    return result['output']['text']
                else:
                    self.logger.error(f"API响应格式错误: {result}")
                    return None
            else:
                self.logger.error(f"API调用失败: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            self.logger.error(f"API调用异常: {e}")
            return None
    
    def _fallback_analysis(self, text):
        """备用分析方法，当AI服务不可用时使用"""
        lines = text.strip().split('\n')
        concepts = []
        
        for i, line in enumerate(lines):
            if line.strip():
                concepts.append({
                    'id': f'node_{i}',
                    'text': line.strip(),
                    'level': 1
                })
        
        return {
            "concepts": concepts,
            "hierarchy": [],
            "connections": [],
            "suggested_type": "hierarchy",
            "enhanced_text": text
        }
    
    def is_available(self):
        """检查AI服务是否可用"""
        try:
            test_prompt = "测试连接"
            response = self._call_llm_api(test_prompt)
            return response is not None
        except:
            return False 