from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class CustomerProfile(BaseModel):
    """客户资料模型"""
    id: Optional[str] = None
    name: Optional[str] = None
    age: Optional[int] = None
    
    # 孕产状态
    pregnancy_status: Optional[str] = None  # 孕期/产后状态
    birth_type: Optional[str] = None  # 顺产/剖腹产
    birth_count: Optional[int] = Field(None, description="几胎")
    due_date: Optional[datetime] = None  # 预产期
    
    # 来源渠道
    source_channel: Optional[str] = None  # 如何了解到月子中心
    
    # 兴趣和关注点
    interests: Optional[List[str]] = []  # 客户感兴趣的服务
    concerns: Optional[List[str]] = []  # 客户顾虑
    priority_needs: Optional[List[str]] = []  # 优先需求
    
    # 其他信息
    notes: Optional[str] = None  # 额外备注
    sentiment: Optional[str] = None  # 整体情感倾向
    
    # 互动记录
    interaction_history: Optional[List[dict]] = []  # 互动历史
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    
    class Config:
        schema_extra = {
            "example": {
                "name": "张娜",
                "age": 32,
                "pregnancy_status": "产后",
                "birth_type": "剖腹产",
                "birth_count": 2,
                "source_channel": "朋友介绍",
                "interests": ["母婴护理", "产后修复"],
                "concerns": ["母乳喂养", "恢复速度"],
                "priority_needs": ["母乳喂养指导"],
                "notes": "客户希望能够尽快恢复工作",
                "sentiment": "正面"
            }
        } 