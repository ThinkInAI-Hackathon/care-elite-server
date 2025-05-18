#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
销售心得数据库 - 管理销售心得和话术数据
"""

import logging
import json
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# 模拟销售心得数据库，实际项目中应使用向量数据库存储
SALES_EXPERIENCES = [
    {
        "id": "exp001",
        "title": "顺产后体重恢复",
        "tags": ["顺产", "体重恢复", "产后恢复"],
        "persona": {
            "delivery_type": "顺产",
            "concerns": ["体重恢复"],
            "child_count": 1
        },
        "experience": "针对顺产后关注体重恢复的客户，应着重强调我们的科学饮食计划和专业营养师一对一指导。他们通常希望快速恢复产前身材，可以展示往期客户的恢复案例和数据。",
        "scripts": [
            {
                "scenario": "初次咨询",
                "content": "了解到您是顺产，现在特别关注产后体重恢复，这是很多新妈妈的共同诉求。我们中心的膳食由营养师团队定制，针对顺产妈妈的恢复周期科学调配，平均28天内能恢复到孕前体重的85%以上。"
            },
            {
                "scenario": "价格顾虑",
                "content": "我理解您对价格的考虑。不过您想过吗，如果没有专业指导，自行恢复往往会走很多弯路，反而耽误黄金恢复期。我们的服务虽然有一定费用，但提供的是全方位、科学的恢复方案，长期来看是非常划算的投资。"
            }
        ]
    },
    {
        "id": "exp002",
        "title": "母乳喂养困难",
        "tags": ["母乳喂养", "催乳", "新生儿护理"],
        "persona": {
            "concerns": ["母乳喂养"],
            "budget_level": "中高端"
        },
        "experience": "对于母乳喂养有困难的客户，他们的焦虑点主要是担心宝宝营养不足。应强调我们有专业催乳师和哺乳指导，成功率高，并且提供24小时专业护理支持。",
        "scripts": [
            {
                "scenario": "哺乳困难",
                "content": "许多妈妈刚开始都会遇到母乳喂养的困难，这非常正常。我们中心的专业催乳师会每天为您进行一对一指导，包括按摩手法教学、正确哺乳姿势指导，90%的妈妈在我们的帮助下成功建立了充足的奶源。"
            },
            {
                "scenario": "担心宝宝吃不饱",
                "content": "我们理解您的担忧。在中心期间，护理团队会全天候观察宝宝的进食和排泄情况，确保宝宝获得充足营养。同时，我们会教您判断宝宝是否吃饱的方法，让您逐渐建立信心。"
            }
        ]
    }
]

def search_sales_experience(query: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    搜索匹配的销售心得
    
    参数:
        query: 查询条件，可包含tags、persona等字段
        
    返回:
        匹配的销售心得列表
    """
    results = []
    
    # 简单匹配逻辑，实际项目中应使用向量搜索
    for exp in SALES_EXPERIENCES:
        match_score = 0
        
        # 检查标签匹配
        if "tags" in query and "tags" in exp:
            for tag in query["tags"]:
                if tag in exp["tags"]:
                    match_score += 1
        
        # 检查客户画像匹配
        if "persona" in query and "persona" in exp:
            persona_query = query["persona"]
            persona_exp = exp["persona"]
            
            # 分娩方式匹配
            if "delivery_type" in persona_query and "delivery_type" in persona_exp:
                if persona_query["delivery_type"] == persona_exp["delivery_type"]:
                    match_score += 2
            
            # 关注点匹配
            if "concerns" in persona_query and "concerns" in persona_exp:
                for concern in persona_query["concerns"]:
                    if concern in persona_exp["concerns"]:
                        match_score += 2
            
            # 预算级别匹配
            if "budget_level" in persona_query and "budget_level" in persona_exp:
                if persona_query["budget_level"] == persona_exp["budget_level"]:
                    match_score += 1
        
        # 如果匹配分数大于0，添加到结果中
        if match_score > 0:
            result = exp.copy()
            result["match_score"] = match_score
            results.append(result)
    
    # 按匹配分数排序
    results.sort(key=lambda x: x["match_score"], reverse=True)
    
    logger.info(f"搜索销售心得: 找到 {len(results)} 条匹配结果")
    return results

def get_sales_script(script_id: str) -> Optional[Dict[str, Any]]:
    """
    获取特定销售话术
    
    参数:
        script_id: 话术ID，格式为"{experience_id}_{scenario}"
        
    返回:
        话术信息，如果不存在则返回None
    """
    try:
        exp_id, scenario = script_id.split("_", 1)
        
        for exp in SALES_EXPERIENCES:
            if exp["id"] == exp_id:
                for script in exp["scripts"]:
                    if script["scenario"] == scenario:
                        logger.info(f"获取销售话术: {script_id}")
                        return script
        
        logger.warning(f"销售话术不存在: {script_id}")
        return None
    except Exception as e:
        logger.error(f"获取销售话术失败: {str(e)}")
        return None 