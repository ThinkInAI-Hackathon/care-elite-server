#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
用户画像数据库 - 处理用户画像的存储和检索
"""

import logging
import os
import json
from typing import Any, Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# 模拟数据库，实际项目中应当使用MongoDB等数据库
# 存储结构为 user_id -> profile_data
USER_PROFILES = {}

def save_user_profile(profile_data: Dict[str, Any]) -> str:
    """
    保存用户画像到数据库
    
    参数:
        profile_data: 用户画像数据
        
    返回:
        用户画像ID
    """
    profile_id = profile_data.get("profile_id")
    
    if not profile_id:
        # 生成新的profile_id
        profile_id = f"user_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        profile_data["profile_id"] = profile_id
    
    # 保存到模拟数据库
    USER_PROFILES[profile_id] = profile_data
    
    logger.info(f"保存用户画像: {profile_id}")
    return profile_id

def get_user_profile(profile_id: str) -> Optional[Dict[str, Any]]:
    """
    从数据库获取用户画像
    
    参数:
        profile_id: 用户画像ID
        
    返回:
        用户画像数据，如果不存在则返回None
    """
    profile = USER_PROFILES.get(profile_id)
    
    if not profile:
        logger.warning(f"用户画像不存在: {profile_id}")
        return None
    
    logger.info(f"获取用户画像: {profile_id}")
    return profile

def update_user_profile(profile_id: str, update_data: Dict[str, Any]) -> bool:
    """
    更新用户画像信息
    
    参数:
        profile_id: 用户画像ID
        update_data: 要更新的用户画像数据
        
    返回:
        更新是否成功
    """
    profile = get_user_profile(profile_id)
    
    if not profile:
        logger.warning(f"更新失败，用户画像不存在: {profile_id}")
        return False
    
    # 递归更新嵌套字典
    def update_dict(original, update):
        for key, value in update.items():
            if key in original and isinstance(original[key], dict) and isinstance(value, dict):
                update_dict(original[key], value)
            else:
                original[key] = value
    
    update_dict(profile, update_data)
    USER_PROFILES[profile_id] = profile
    
    logger.info(f"更新用户画像: {profile_id}")
    return True

def add_conversation_history(profile_id: str, role: str, content: str) -> bool:
    """
    向用户画像添加对话历史
    
    参数:
        profile_id: 用户画像ID
        role: 角色 (user/sales)
        content: 对话内容
        
    返回:
        添加是否成功
    """
    profile = get_user_profile(profile_id)
    
    if not profile:
        logger.warning(f"添加对话历史失败，用户画像不存在: {profile_id}")
        return False
    
    # 确保conversation_history字段存在
    if "conversation_history" not in profile:
        profile["conversation_history"] = []
    
    # 添加对话记录
    conversation_entry = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    }
    
    profile["conversation_history"].append(conversation_entry)
    USER_PROFILES[profile_id] = profile
    
    logger.info(f"添加对话历史: {profile_id}, 角色: {role}")
    return True 