from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
import json
import logging

from app.models.customer import CustomerProfile
from app.services.ai_service import AIService
from app.services.knowledge_base import KnowledgeBase
from app.services.case_library import CaseLibrary
from app.core.dependencies import get_ai_service, get_knowledge_base, get_case_library

logger = logging.getLogger("mcp-server")

api_router = APIRouter()

@api_router.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "ok", "service": "mcp-server"}

# 知识库管理路由
@api_router.get("/knowledge")
async def list_knowledge_documents(
    knowledge_base: KnowledgeBase = Depends(get_knowledge_base)
):
    """列出知识库中的文档"""
    # 在实际实现中，你可能需要从数据库中获取文档列表
    return {"message": "知识库文档列表功能待开发"}

@api_router.post("/knowledge/upload")
async def upload_knowledge_document(
    file: UploadFile = File(...),
    document_type: str = Form(...),
    knowledge_base: KnowledgeBase = Depends(get_knowledge_base)
):
    """上传文档到知识库"""
    try:
        content = await file.read()
        # 处理文档上传逻辑
        # 将来实现
        
        return {"message": "文档上传成功", "filename": file.filename}
    except Exception as e:
        logger.error(f"上传文档时出错: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文档上传失败: {str(e)}"
        )

# 案例库管理路由
@api_router.get("/cases")
async def list_cases(
    case_library: CaseLibrary = Depends(get_case_library)
):
    """列出所有案例"""
    cases = case_library.list_all_cases()
    return cases

@api_router.get("/cases/{case_id}")
async def get_case(
    case_id: str,
    case_library: CaseLibrary = Depends(get_case_library)
):
    """获取特定案例"""
    case = case_library.get_case(case_id)
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"案例 {case_id} 不存在"
        )
    return case

@api_router.post("/cases")
async def create_case(
    case_data: Dict[str, Any],
    case_library: CaseLibrary = Depends(get_case_library)
):
    """创建新案例"""
    success = case_library.add_case(case_data)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建案例失败"
        )
    return {"message": "案例创建成功"}

@api_router.post("/cases/search")
async def search_similar_cases(
    query: Dict[str, Any],
    case_library: CaseLibrary = Depends(get_case_library)
):
    """搜索相似案例"""
    # 将查询字典转换为文本查询
    query_text = " ".join([f"{k}: {v}" for k, v in query.items()])
    cases = case_library.search_similar_cases(query_text)
    
    # 格式化结果
    formatted_cases = []
    for case in cases:
        case_data = case.page_content
        metadata = case.metadata
        
        # 确保案例数据是字典格式
        if isinstance(case_data, str):
            try:
                case_data = json.loads(case_data)
            except:
                case_data = {"description": case_data}
        
        # 合并元数据和案例数据
        result = {**metadata, **case_data}
        formatted_cases.append(result)
    
    return formatted_cases

# AI服务路由
@api_router.post("/ai/analyze")
async def analyze_text(
    text: Dict[str, str],
    ai_service: AIService = Depends(get_ai_service)
):
    """分析客户文本"""
    try:
        analysis = await ai_service.analyze_customer_feedback(text.get("content", ""))
        return analysis
    except Exception as e:
        logger.error(f"分析文本时出错: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"分析失败: {str(e)}"
        )

@api_router.post("/ai/generate-response")
async def generate_response(
    request: Dict[str, Any],
    ai_service: AIService = Depends(get_ai_service)
):
    """生成AI回应"""
    try:
        query = request.get("query", "")
        customer_profile = request.get("customer_profile", {})
        context = request.get("context", [])
        
        response = await ai_service.generate_professional_response(
            query, customer_profile, context
        )
        
        return {"response": response}
    except Exception as e:
        logger.error(f"生成回应时出错: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"生成回应失败: {str(e)}"
        )

# 客户管理路由
@api_router.post("/customers")
async def create_customer(customer: CustomerProfile):
    """创建客户资料"""
    # 将来实现客户资料的持久化
    return customer

@api_router.get("/customers/{customer_id}")
async def get_customer(customer_id: str):
    """获取客户资料"""
    # 将来实现
    return {"message": "获取客户资料功能待开发"} 