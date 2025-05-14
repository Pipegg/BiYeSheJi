from core.query import DB
import csv
import os
import logging
from typing import List, Tuple, Any
from pathlib import Path

# 配置日志
logger = logging.getLogger(__name__)

# 定义数据文件路径
BASE_DIR = Path(__file__).resolve().parent
csv_path = os.path.join(BASE_DIR, "student_course_data.csv")

def get_learning_records() -> List[Tuple[Any, ...]]:
    """
    获取学习记录数据
    """
    try:
        records = (DB.name("xuexijindu").alias("j")
            .joinLeft("kechengxuexi k", "k.id=j.kechengxuexiid")
            .joinLeft("xuesheng x", "j.xueshengyonghu=x.xuehao")
            .field("x.id xueshengid,k.kechengxinxiid,k.xuexijindu")
            .order("j.id asc")
            .select())
        
        if not records:
            logger.warning("未找到学习记录数据")
            return []
            
        return [(str(r.xueshengid), str(r.kechengxinxiid), float(r.xuexijindu)) 
                for r in records if r.xueshengid and r.kechengxinxiid is not None]
                
    except Exception as e:
        logger.error(f"获取学习记录失败: {e}")
        return []

def validate_data(data: List[Tuple[Any, ...]]) -> bool:
    """
    验证数据的有效性
    """
    if not data:
        logger.error("数据为空")
        return False
        
    try:
        for record in data:
            if len(record) != 3:
                logger.error(f"数据格式错误: {record}")
                return False
            if not all(x is not None for x in record):
                logger.error(f"数据包含空值: {record}")
                return False
    except Exception as e:
        logger.error(f"数据验证失败: {e}")
        return False
        
    return True

def ensure_directory_exists(file_path: str) -> bool:
    """
    确保目录存在
    """
    try:
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        return True
    except Exception as e:
        logger.error(f"创建目录失败: {e}")
        return False

def write_to_csv(file_path: str, columns: List[str], data: List[Tuple[Any, ...]]) -> bool:
    """
    写入数据到CSV文件
    """
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(columns)  # 写入列名
            writer.writerows(data)  # 写入数据
        return True
    except Exception as e:
        logger.error(f"写入CSV文件失败: {e}")
        return False

def updateKecheng() -> bool:
    """
    更新课程学习数据到CSV文件
    返回：是否更新成功
    """
    try:
        # 获取数据
        data = get_learning_records()
        
        # 验证数据
        if not validate_data(data):
            return False
            
        # 确保目录存在
        if not ensure_directory_exists(csv_path):
            return False
            
        # 定义列名
        columns = ["学生ID", "课程ID", "学习进度"]
        
        # 写入数据
        if write_to_csv(csv_path, columns, data):
            logger.info(f"成功写入预训练集: {csv_path}")
            return True
        else:
            return False
            
    except Exception as e:
        logger.error(f"更新课程数据失败: {e}")
        return False
