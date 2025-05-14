import json
from typing import Dict, Any, List
import re

def parse_json_response(response: str) -> Dict[str, Any]:
    """
    解析模型返回的JSON响应
    Args:
        response: 模型返回的文本
    Returns:
        解析后的JSON对象
    """
    try:
        # 尝试直接解析JSON
        return json.loads(response)
    except json.JSONDecodeError:
        # 如果直接解析失败，尝试提取JSON部分
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        # 如果仍然失败，返回空字典
        return {}

def format_prompt(template: str, **kwargs) -> str:
    """
    格式化提示模板
    Args:
        template: 提示模板
        kwargs: 模板参数
    Returns:
        格式化后的提示
    """
    return template.format(**kwargs)

def validate_response(response: Dict[str, Any], required_fields: List[str]) -> bool:
    """
    验证响应是否包含所需字段
    Args:
        response: 响应对象
        required_fields: 所需字段列表
    Returns:
        是否验证通过
    """
    return all(field in response for field in required_fields)

def extract_score(text: str) -> float:
    """
    从文本中提取分数
    Args:
        text: 包含分数的文本
    Returns:
        提取的分数
    """
    score_match = re.search(r'(\d+(?:\.\d+)?)\s*分', text)
    if score_match:
        return float(score_match.group(1))
    return 0.0

def clean_text(text: str) -> str:
    """
    清理文本
    Args:
        text: 原始文本
    Returns:
        清理后的文本
    """
    # 移除多余的空白字符
    text = re.sub(r'\s+', ' ', text)
    # 移除特殊字符
    text = re.sub(r'[^\w\s\u4e00-\u9fff.,!?，。！？]', '', text)
    return text.strip() 