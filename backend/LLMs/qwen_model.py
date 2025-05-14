import os
from typing import List, Dict, Any, Optional
import requests
import json
from dotenv import load_dotenv

class QwenModel:
    def __init__(self, model_name: str = "qwen-turbo"):
        """
        初始化Qwen模型
        Args:
            model_name: 模型名称，默认为qwen-turbo（性价比最高的模型）
        """
        self.model_name = model_name
        self.api_key = os.getenv('QWEN_API_KEY')
        if not self.api_key:
            raise ValueError("QWEN_API_KEY environment variable is not set")
        
        self.api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_response(
        self,
        prompt: str,
        max_length: int = 2048,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 50,
        repetition_penalty: float = 1.1
    ) -> str:
        """
        生成回复
        Args:
            prompt: 输入提示
            max_length: 最大生成长度
            temperature: 温度参数
            top_p: 核采样参数
            top_k: top-k采样参数
            repetition_penalty: 重复惩罚参数
        Returns:
            生成的回复文本
        """
        try:
            payload = {
                "model": self.model_name,
                "input": {
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                },
                "parameters": {
                    "max_tokens": max_length,
                    "temperature": temperature,
                    "top_p": top_p,
                    "top_k": top_k,
                    "repetition_penalty": repetition_penalty
                }
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["output"]["text"]
            else:
                print(f"Error: API request failed with status code {response.status_code}")
                print(f"Response: {response.text}")
                return ""
                
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return ""

    def batch_generate(
        self,
        prompts: List[str],
        max_length: int = 2048,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 50,
        repetition_penalty: float = 1.1
    ) -> List[str]:
        """
        批量生成回复
        Args:
            prompts: 输入提示列表
            max_length: 最大生成长度
            temperature: 温度参数
            top_p: 核采样参数
            top_k: top-k采样参数
            repetition_penalty: 重复惩罚参数
        Returns:
            生成的回复文本列表
        """
        responses = []
        for prompt in prompts:
            response = self.generate_response(
                prompt,
                max_length,
                temperature,
                top_p,
                top_k,
                repetition_penalty
            )
            responses.append(response)
        return responses 