#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
通用工具函数 - 提供项目中共用的辅助函数
"""

import logging
import os
import json
import base64
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> None:
    """
    设置日志配置
    
    参数:
        log_level: 日志级别，默认为INFO
        log_file: 日志文件路径，默认为None（控制台输出）
    """
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    if log_file:
        logging.basicConfig(
            level=numeric_level,
            format=log_format,
            datefmt=date_format,
            filename=log_file,
            filemode='a'
        )
    else:
        logging.basicConfig(
            level=numeric_level,
            format=log_format,
            datefmt=date_format
        )
    
    logger.info(f"日志系统初始化完成，级别: {log_level}")

def save_audio_to_file(audio_data: str, directory: str = "recordings") -> str:
    """
    将Base64编码的音频数据保存到文件
    
    参数:
        audio_data: Base64编码的音频数据
        directory: 保存目录，默认为recordings
        
    返回:
        保存的文件路径
    """
    try:
        # 确保目录存在
        os.makedirs(directory, exist_ok=True)
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"audio_{timestamp}.wav"
        filepath = os.path.join(directory, filename)
        
        # 解码并保存音频数据
        decoded_audio = base64.b64decode(audio_data)
        with open(filepath, "wb") as f:
            f.write(decoded_audio)
        
        logger.info(f"音频保存成功: {filepath}")
        return filepath
    
    except Exception as e:
        logger.error(f"保存音频失败: {str(e)}")
        return ""

def load_audio_from_file(filepath: str) -> Optional[str]:
    """
    从文件加载音频数据并转换为Base64编码
    
    参数:
        filepath: 音频文件路径
        
    返回:
        Base64编码的音频数据，如果失败则返回None
    """
    try:
        with open(filepath, "rb") as f:
            audio_data = f.read()
            base64_audio = base64.b64encode(audio_data).decode('utf-8')
        
        logger.info(f"音频加载成功: {filepath}")
        return base64_audio
    
    except Exception as e:
        logger.error(f"加载音频失败: {str(e)}")
        return None

def save_json_to_file(data: Dict[str, Any], filepath: str) -> bool:
    """
    将JSON数据保存到文件
    
    参数:
        data: 要保存的数据
        filepath: 文件路径
        
    返回:
        是否保存成功
    """
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"JSON数据保存成功: {filepath}")
        return True
    
    except Exception as e:
        logger.error(f"保存JSON数据失败: {str(e)}")
        return False

def load_json_from_file(filepath: str) -> Optional[Dict[str, Any]]:
    """
    从文件加载JSON数据
    
    参数:
        filepath: 文件路径
        
    返回:
        加载的JSON数据，如果失败则返回None
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        logger.info(f"JSON数据加载成功: {filepath}")
        return data
    
    except Exception as e:
        logger.error(f"加载JSON数据失败: {str(e)}")
        return None 