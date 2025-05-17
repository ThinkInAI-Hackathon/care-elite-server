import os
from typing import List
from pydantic import BaseSettings, AnyHttpUrl
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "月子中心孕产康养AI专家系统"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api/v1"
    
    # 服务器设置
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "True").lower() == "true"
    
    # CORS设置
    CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://localhost:8080",
    ]
    
    # 数据库设置
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017/mcp")
    
    # 向量数据库设置
    VECTOR_DB_PATH: str = os.getenv("VECTOR_DB_PATH", "./data/vector_db")
    
    # LLM设置
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo")
    
    # 语音识别设置
    SPEECH_API_KEY: str = os.getenv("SPEECH_API_KEY", "")
    
    # 会话设置
    SESSION_TIMEOUT: int = int(os.getenv("SESSION_TIMEOUT", "3600"))  # 会话超时时间（秒）
    
    # 知识库设置
    KNOWLEDGE_BASE_PATH: str = os.getenv("KNOWLEDGE_BASE_PATH", "./data/knowledge_base")
    
    # 案例库设置
    CASE_LIBRARY_PATH: str = os.getenv("CASE_LIBRARY_PATH", "./data/case_library")

    class Config:
        case_sensitive = True

# 创建全局设置实例
settings = Settings() 