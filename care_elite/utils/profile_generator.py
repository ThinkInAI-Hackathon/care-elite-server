#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
用户画像生成器 - 从对话文本中提取用户信息，生成用户画像
"""

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

def extract_user_info(text: str) -> Dict[str, Any]:
    """
    从文本中提取用户信息
    
    参数:
        text: 待分析的文本内容
        
    返回:
        提取的用户信息
    """
    # TODO: 实际实现应使用NLP或LLM提取用户信息
    # 以下为mock实现
    
    # 模拟提取的用户信息
    extracted_info = {
        "delivery_type": None,
        "child_count": None,
        "concerns": [],
        "budget_preference": None
    }
    
    # 简单的关键词匹配提取
    if "顺产" in text:
        extracted_info["delivery_type"] = "顺产"
    elif "剖腹产" in text or "刨腹产" in text:
        extracted_info["delivery_type"] = "剖腹产"
    
    if "一胎" in text or "第一胎" in text or "第一个孩子" in text:
        extracted_info["child_count"] = 1
    elif "二胎" in text or "第二胎" in text or "第二个孩子" in text:
        extracted_info["child_count"] = 2
    
    # 提取关注点
    concerns = []
    if any(keyword in text for keyword in ["体重", "瘦身", "减肥", "恢复身材"]):
        concerns.append("体重恢复")
    if any(keyword in text for keyword in ["母乳", "奶水", "喂养", "催乳"]):
        concerns.append("母乳喂养")
    if any(keyword in text for keyword in ["睡眠", "失眠", "休息不好"]):
        concerns.append("睡眠质量")
    if any(keyword in text for keyword in ["伤口", "恢复", "疼痛"]):
        concerns.append("伤口愈合")
    
    extracted_info["concerns"] = concerns
    
    # 提取预算偏好
    if any(keyword in text for keyword in ["经济", "便宜", "实惠", "性价比"]):
        extracted_info["budget_preference"] = "经济型"
    elif any(keyword in text for keyword in ["高端", "豪华", "尊享", "贵"]):
        extracted_info["budget_preference"] = "高端"
    
    return extracted_info

def generate_user_profile(conversation_history: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    从对话历史生成用户画像
    
    参数:
        conversation_history: 对话历史记录
        
    返回:
        生成的用户画像
    """
    logger.info(f"从{len(conversation_history)}条对话记录生成用户画像")
    
    # 整合所有文本
    all_text = ""
    for entry in conversation_history:
        if entry["role"] == "user":
            all_text += entry["content"] + " "
    
    # 提取用户信息
    user_info = extract_user_info(all_text)
    
    # 构建用户画像
    user_profile = {
        "basic_info": {
            "pregnancy_status": "产后",  # 默认值，实际应从对话中提取
            "delivery_type": user_info["delivery_type"] or "未知",
            "child_count": user_info["child_count"] or 0,
            "concerns": user_info["concerns"]
        },
        "preferences": {
            "budget_level": user_info["budget_preference"] or "未知",
            "stay_duration": "28天",  # 默认值
            "dietary_restrictions": []  # 默认值
        },
        "conversation_history": conversation_history
    }
    
    return user_profile

def update_user_profile(existing_profile: Dict[str, Any], new_text: str, role: str) -> Dict[str, Any]:
    """
    根据新的对话更新用户画像
    
    参数:
        existing_profile: 现有的用户画像
        new_text: 新的对话文本
        role: 发言角色
        
    返回:
        更新后的用户画像
    """
    # 添加新的对话记录
    if "conversation_history" not in existing_profile:
        existing_profile["conversation_history"] = []
    
    existing_profile["conversation_history"].append({
        "role": role,
        "content": new_text
    })
    
    # 如果是用户发言，提取信息并更新画像
    if role == "user":
        user_info = extract_user_info(new_text)
        
        # 更新分娩方式
        if user_info["delivery_type"]:
            existing_profile["basic_info"]["delivery_type"] = user_info["delivery_type"]
        
        # 更新胎次
        if user_info["child_count"]:
            existing_profile["basic_info"]["child_count"] = user_info["child_count"]
        
        # 更新关注点，添加新的关注点
        for concern in user_info["concerns"]:
            if concern not in existing_profile["basic_info"]["concerns"]:
                existing_profile["basic_info"]["concerns"].append(concern)
        
        # 更新预算偏好
        if user_info["budget_preference"]:
            existing_profile["preferences"]["budget_level"] = user_info["budget_preference"]
    
    return existing_profile 