from functools import lru_cache
from fastapi import Depends

from app.core.config import settings
from app.services.ai_service import AIService
from app.services.knowledge_base import KnowledgeBase
from app.services.case_library import CaseLibrary
from langchain.embeddings.openai import OpenAIEmbeddings

# 创建单例服务实例

@lru_cache()
def get_embeddings():
    """获取嵌入模型单例"""
    return OpenAIEmbeddings(
        openai_api_key=settings.OPENAI_API_KEY
    )

@lru_cache()
def get_knowledge_base(embeddings=Depends(get_embeddings)):
    """获取知识库服务单例"""
    return KnowledgeBase(embeddings)

@lru_cache()
def get_case_library(embeddings=Depends(get_embeddings)):
    """获取案例库服务单例"""
    return CaseLibrary(embeddings)

@lru_cache()
def get_ai_service():
    """获取AI服务单例"""
    return AIService()