import json
import logging
from typing import Dict, List, Any
import asyncio
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.callbacks.manager import CallbackManager
from langchain.chains import RetrievalQA

from app.core.config import settings
from app.services.knowledge_base import KnowledgeBase
from app.services.case_library import CaseLibrary
from app.models.customer import CustomerProfile

logger = logging.getLogger("mcp-server")

class AIService:
    def __init__(self):
        """初始化AI服务"""
        # 初始化大语言模型
        self.llm = ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            model_name=settings.OPENAI_MODEL,
            temperature=0.7
        )
        
        # 初始化向量嵌入
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # 初始化知识库
        self.knowledge_base = KnowledgeBase(self.embeddings)
        
        # 初始化案例库
        self.case_library = CaseLibrary(self.embeddings)
        
        # 初始化检索QA链
        self.retrieval_qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.knowledge_base.retriever,
            return_source_documents=True
        )
        
        logger.info("AI服务初始化完成")
    
    async def extract_customer_info(self, text: str) -> Dict[str, Any]:
        """从客户对话中提取关键信息"""
        prompt = ChatPromptTemplate.from_template(
            """
            请从以下对话中提取客户的关键信息，包括但不限于：
            - 姓名（如果提到）
            - 年龄（如果提到）
            - 孕期/产后情况（几胎、顺产/剖腹产等）
            - 了解月子中心的渠道（如朋友介绍、网络等）
            - 关注点/需求（如果提到）
            
            对话内容：{text}
            
            请以JSON格式输出，只返回提取到的信息，不要添加其他解释。如果某项信息未提及，则不要包含该字段。
            """
        )
        
        # 异步调用大语言模型
        response = await self.llm.ainvoke(prompt.format(text=text))
        
        try:
            # 解析JSON响应
            extracted_info = json.loads(response.content)
            return extracted_info
        except json.JSONDecodeError:
            logger.error("无法解析LLM响应为JSON")
            # 尝试使用一个基本结构
            return {"raw_feedback": text}
    
    async def analyze_customer_feedback(self, text: str) -> Dict[str, Any]:
        """分析客户反馈，识别兴趣点和关注点"""
        prompt = ChatPromptTemplate.from_template(
            """
            请分析以下客户反馈，识别客户的兴趣点、关注点以及可能的顾虑：
            
            客户反馈：{text}
            
            请以JSON格式输出，包含以下字段：
            - interests: 客户表达兴趣的服务或设施（列表）
            - concerns: 客户可能的顾虑（列表）
            - sentiment: 整体情感倾向（正面/中性/负面）
            - priority_needs: 客户最优先的需求（列表）
            
            只返回JSON格式的分析结果，不要添加其他解释。
            """
        )
        
        # 异步调用大语言模型
        response = await self.llm.ainvoke(prompt.format(text=text))
        
        try:
            # 解析JSON响应
            analysis = json.loads(response.content)
            return analysis
        except json.JSONDecodeError:
            logger.error("无法解析LLM响应为JSON")
            return {
                "interests": [],
                "concerns": [],
                "sentiment": "unknown",
                "priority_needs": []
            }
    
    async def generate_professional_response(
        self, 
        query: str, 
        customer_profile: Dict[str, Any], 
        context: List[Dict[str, str]]
    ) -> str:
        """生成专业的回答，使用RAG增强精确度"""
        # 准备上下文信息
        context_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in context[-5:]])
        
        # 构建客户资料摘要
        profile_summary = ""
        if customer_profile:
            profile_items = []
            for key, value in customer_profile.items():
                if isinstance(value, list):
                    profile_items.append(f"{key}: {', '.join(value)}")
                else:
                    profile_items.append(f"{key}: {value}")
            profile_summary = "客户资料:\n" + "\n".join(profile_items)
        
        # 使用RAG检索相关知识
        retrieval_result = await asyncio.to_thread(
            self.retrieval_qa,
            {"query": query}
        )
        
        # 获取检索到的信息
        retrieved_info = retrieval_result.get("result", "")
        source_docs = retrieval_result.get("source_documents", [])
        
        # 构建包含检索信息的提示
        prompt = ChatPromptTemplate.from_template(
            """
            你是"小美"，一位月子中心的AI专业顾问，擅长孕产康养知识。
            
            客户资料：
            {profile_summary}
            
            最近的对话内容：
            {context}
            
            相关专业知识：
            {retrieved_info}
            
            客户问题：{query}
            
            请根据以上信息，提供专业、准确、温暖的回答。回答应当：
            1. 保持专业性，引用可靠的孕产知识
            2. 针对客户个人情况给出个性化建议
            3. 语气温和亲切，使用专业但不过于医学化的语言
            4. 避免过度承诺或夸大效果
            
            回答：
            """
        )
        
        # 异步调用大语言模型
        response = await self.llm.ainvoke(
            prompt.format(
                profile_summary=profile_summary,
                context=context_str,
                retrieved_info=retrieved_info,
                query=query
            )
        )
        
        return response.content
    
    async def generate_sales_assistant_response(
        self, 
        prompt: str, 
        customer_profile: Dict[str, Any], 
        context: List[Dict[str, str]]
    ) -> str:
        """生成销售助手的回应"""
        # 准备上下文信息
        context_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in context[-5:]])
        
        # 构建客户资料摘要
        profile_summary = ""
        if customer_profile:
            profile_items = []
            for key, value in customer_profile.items():
                if isinstance(value, list):
                    profile_items.append(f"{key}: {', '.join(value)}")
                else:
                    profile_items.append(f"{key}: {value}")
            profile_summary = "客户资料:\n" + "\n".join(profile_items)
        
        # 使用RAG检索相关知识
        retrieval_result = await asyncio.to_thread(
            self.retrieval_qa,
            {"query": prompt}
        )
        
        # 获取检索到的信息
        retrieved_info = retrieval_result.get("result", "")
        
        # 构建销售助手提示
        assistant_prompt = ChatPromptTemplate.from_template(
            """
            你是"小美"，一位月子中心的AI专业顾问，现在正在协助销售人员与客户交流。
            
            客户资料：
            {profile_summary}
            
            最近的对话内容：
            {context}
            
            相关专业知识：
            {retrieved_info}
            
            销售人员的指令：{prompt}
            
            请根据以上信息，提供一段专业、有说服力的回应，帮助销售人员向客户解释月子中心的服务价值。回应应当：
            1. 直接针对销售人员的指令
            2. 结合客户的具体情况和需求
            3. 突出月子中心服务的专业性和个性化
            4. 语言亲切自然，避免生硬的营销腔调
            5. 引用事实和专业知识增加可信度
            
            回应：
            """
        )
        
        # 异步调用大语言模型
        response = await self.llm.ainvoke(
            assistant_prompt.format(
                profile_summary=profile_summary,
                context=context_str,
                retrieved_info=retrieved_info,
                prompt=prompt
            )
        )
        
        return response.content
    
    async def find_similar_cases(self, customer_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """查找与当前客户相似的历史案例"""
        # 从客户资料构建查询
        query_parts = []
        
        # 添加基本信息
        if "age" in customer_profile:
            query_parts.append(f"年龄: {customer_profile['age']}")
        
        if "pregnancy_status" in customer_profile:
            query_parts.append(f"孕产状态: {customer_profile['pregnancy_status']}")
        
        # 添加关注点和需求
        if "interests" in customer_profile and customer_profile["interests"]:
            interests = ", ".join(customer_profile["interests"])
            query_parts.append(f"关注服务: {interests}")
        
        if "priority_needs" in customer_profile and customer_profile["priority_needs"]:
            needs = ", ".join(customer_profile["priority_needs"])
            query_parts.append(f"优先需求: {needs}")
        
        # 构建查询字符串
        query = " ".join(query_parts)
        if not query:
            query = "标准月子服务"  # 默认查询
        
        # 查询相似案例
        similar_cases = await asyncio.to_thread(
            self.case_library.search_similar_cases,
            query, 3  # 返回前3个最相似的案例
        )
        
        # 格式化结果
        formatted_cases = []
        for case in similar_cases:
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