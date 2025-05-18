#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
案例数据库 - 管理月子中心成功案例
"""

import logging
import json
import os
from typing import Any, Dict, List, Optional

from care_elite.database.user_profile import get_user_profile

logger = logging.getLogger(__name__)

# 模拟案例数据库，实际项目中应使用数据库存储
SUCCESS_CASES = [
    {
        "case_id": "case001",
        "title": "顺产妈妈的完美恢复之旅",
        "customer_info": {
            "age": 28,
            "delivery_type": "顺产",
            "child_count": 1,
            "initial_concerns": ["体重恢复", "母乳喂养"]
        },
        "stay_info": {
            "package": "高级产后护理套餐",
            "duration": "28天",
            "start_date": "2023-01-15",
            "end_date": "2023-02-12"
        },
        "results": {
            "weight_recovery": {
                "before": "65kg",
                "after": "56kg",
                "target": "54kg",
                "achievement": "恢复至目标体重的91%"
            },
            "breastfeeding": {
                "before": "困难，乳汁分泌不足",
                "after": "顺利，纯母乳喂养",
                "achievement": "成功建立充足奶源"
            },
            "sleep_quality": {
                "before": "每晚睡眠不足4小时",
                "after": "每晚连续睡眠6-7小时",
                "achievement": "睡眠质量显著提升"
            }
        },
        "testimonial": "在月子中心的28天是我产后恢复的黄金时期，专业的团队让我能够专注于恢复和照顾宝宝，不必担心其他琐事。我的体重恢复超出预期，母乳喂养也顺利建立，非常感谢中心的每一位工作人员！",
        "images": [
            {
                "url": "https://example.com/cases/001/before.jpg",
                "description": "入住前"
            },
            {
                "url": "https://example.com/cases/001/after.jpg",
                "description": "结束时"
            }
        ]
    },
    {
        "case_id": "case002",
        "title": "剖腹产妈妈的舒适恢复计划",
        "customer_info": {
            "age": 32,
            "delivery_type": "剖腹产",
            "child_count": 2,
            "initial_concerns": ["伤口愈合", "肠胃恢复", "睡眠质量"]
        },
        "stay_info": {
            "package": "尊享产后护理套餐",
            "duration": "35天",
            "start_date": "2023-03-10",
            "end_date": "2023-04-14"
        },
        "results": {
            "wound_healing": {
                "before": "手术后疼痛明显，活动受限",
                "after": "伤口完全愈合，无不适感",
                "achievement": "提前一周完成愈合过程"
            },
            "digestive_system": {
                "before": "肠胃功能弱，消化不良",
                "after": "肠胃功能恢复正常，饮食多样化",
                "achievement": "排便规律，无腹胀不适"
            },
            "sleep_quality": {
                "before": "浅眠多梦，易醒",
                "after": "深度睡眠增加，精力充沛",
                "achievement": "平均睡眠质量提升60%"
            }
        },
        "testimonial": "作为二胎剖腹产妈妈，我非常担心恢复问题。选择入住月子中心是我做的最明智的决定！专业的伤口护理和中医调理让我恢复得比想象中快得多。现在我推荐给所有准备生二胎的朋友。",
        "images": [
            {
                "url": "https://example.com/cases/002/before.jpg",
                "description": "入住前"
            },
            {
                "url": "https://example.com/cases/002/after.jpg",
                "description": "结束时"
            }
        ]
    }
]

def search_similar_cases(user_profile_id: str, case_type: str = "similar") -> List[Dict[str, Any]]:
    """
    搜索与用户情况相近的成功案例
    
    参数:
        user_profile_id: 用户画像ID
        case_type: 案例类型，可选值: "similar"(相似案例), "best"(最佳案例)
        
    返回:
        匹配的案例列表
    """
    # 获取用户画像
    user_profile = get_user_profile(user_profile_id)
    
    if not user_profile:
        logger.warning(f"无法获取用户画像: {user_profile_id}")
        # 返回默认的热门案例
        if case_type == "best":
            return SUCCESS_CASES[:1]  # 返回最佳案例
        return SUCCESS_CASES  # 返回所有案例
    
    # 根据用户画像匹配案例
    results = []
    
    # 提取用户关键信息
    delivery_type = user_profile.get("basic_info", {}).get("delivery_type", "")
    concerns = user_profile.get("basic_info", {}).get("concerns", [])
    child_count = user_profile.get("basic_info", {}).get("child_count", 0)
    
    for case in SUCCESS_CASES:
        match_score = 0
        case_info = case.get("customer_info", {})
        
        # 分娩方式匹配
        if delivery_type and case_info.get("delivery_type") == delivery_type:
            match_score += 3
        
        # 关注点匹配
        for concern in concerns:
            if concern in case_info.get("initial_concerns", []):
                match_score += 2
        
        # 胎次匹配
        if child_count and case_info.get("child_count") == child_count:
            match_score += 1
        
        # 如果匹配分数大于0，添加到结果中
        if match_score > 0:
            result = case.copy()
            result["match_score"] = match_score
            results.append(result)
    
    # 排序结果
    results.sort(key=lambda x: x["match_score"], reverse=True)
    
    # 根据case_type返回结果
    if case_type == "best":
        # 返回最佳匹配案例
        return results[:1] if results else SUCCESS_CASES[:1]
    
    # 返回相似案例
    return results if results else SUCCESS_CASES
    
def get_case_by_id(case_id: str) -> Optional[Dict[str, Any]]:
    """
    根据ID获取特定案例
    
    参数:
        case_id: 案例ID
        
    返回:
        案例信息，如果不存在则返回None
    """
    for case in SUCCESS_CASES:
        if case["case_id"] == case_id:
            logger.info(f"获取案例: {case_id}")
            return case
    
    logger.warning(f"案例不存在: {case_id}")
    return None 