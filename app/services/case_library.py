import os
import json
import logging
from typing import List, Dict, Any, Optional
from langchain.vectorstores import Chroma
from langchain.embeddings.base import Embeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader, JSONLoader

from app.core.config import settings

logger = logging.getLogger("mcp-server")

class CaseLibrary:
    def __init__(self, embeddings: Embeddings):
        """初始化案例库"""
        self.embeddings = embeddings
        self.case_library_path = settings.CASE_LIBRARY_PATH
        self.vector_store_path = os.path.join(settings.VECTOR_DB_PATH, "case_library")
        
        # 确保目录存在
        os.makedirs(self.vector_store_path, exist_ok=True)
        os.makedirs(self.case_library_path, exist_ok=True)
        
        # 加载案例向量数据库
        self._load_vector_store()
        
        # 文本分割器
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=200
        )
    
    def _load_vector_store(self):
        """加载向量数据库，如果不存在则创建"""
        try:
            # 尝试加载现有的向量数据库
            self.vector_store = Chroma(
                persist_directory=self.vector_store_path,
                embedding_function=self.embeddings
            )
            
            # 检查向量数据库是否为空
            if self.vector_store._collection.count() == 0:
                logger.info("案例库向量数据库为空，准备初始化")
                self._initialize_case_library()
            else:
                logger.info(f"成功加载案例库向量数据库，包含 {self.vector_store._collection.count()} 条记录")
        
        except Exception as e:
            logger.error(f"加载案例库向量数据库时出错: {str(e)}")
            logger.info("创建新的案例库向量数据库")
            self._initialize_case_library()
    
    def _initialize_case_library(self):
        """初始化案例库，将案例文件加载到向量数据库中"""
        # 检查案例库目录是否存在
        if not os.path.exists(self.case_library_path):
            logger.warning(f"案例库目录 {self.case_library_path} 不存在，创建空目录")
            os.makedirs(self.case_library_path, exist_ok=True)
            return
        
        try:
            # 准备加载JSON文件的函数
            def json_loader(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return Document(
                    page_content=json.dumps(data, ensure_ascii=False),
                    metadata={
                        "source": file_path,
                        "case_id": data.get("case_id", ""),
                        "title": data.get("title", ""),
                        "type": data.get("type", ""),
                        "date": data.get("date", "")
                    }
                )
            
            documents = []
            # 遍历目录中的所有JSON文件
            for root, _, files in os.walk(self.case_library_path):
                for file in files:
                    if file.endswith('.json'):
                        file_path = os.path.join(root, file)
                        try:
                            doc = json_loader(file_path)
                            documents.append(doc)
                        except Exception as e:
                            logger.error(f"加载案例文件 {file_path} 时出错: {str(e)}")
            
            if not documents:
                logger.warning("案例库目录中没有找到有效的案例文件")
                # 创建一个空的向量数据库
                self.vector_store = Chroma(
                    persist_directory=self.vector_store_path,
                    embedding_function=self.embeddings
                )
                return
            
            logger.info(f"从案例库中加载了 {len(documents)} 个案例文档")
            
            # 创建向量数据库
            self.vector_store = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.vector_store_path
            )
            
            # 持久化向量数据库
            self.vector_store.persist()
            logger.info("案例库向量数据库初始化完成并已持久化")
            
        except Exception as e:
            logger.error(f"初始化案例库时出错: {str(e)}")
            # 创建一个空的向量数据库
            self.vector_store = Chroma(
                persist_directory=self.vector_store_path,
                embedding_function=self.embeddings
            )
    
    def add_case(self, case_data: Dict[str, Any], case_id: Optional[str] = None) -> bool:
        """添加新案例到案例库"""
        try:
            # 确保有案例ID
            if not case_id:
                case_id = f"case_{len(os.listdir(self.case_library_path)) + 1}"
            
            # 确保案例数据有必要的字段
            if "title" not in case_data:
                case_data["title"] = f"案例 {case_id}"
            
            case_data["case_id"] = case_id
            
            # 将案例保存为JSON文件
            file_path = os.path.join(self.case_library_path, f"{case_id}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(case_data, f, ensure_ascii=False, indent=2)
            
            # 添加到向量数据库
            document = Document(
                page_content=json.dumps(case_data, ensure_ascii=False),
                metadata={
                    "source": file_path,
                    "case_id": case_id,
                    "title": case_data.get("title", ""),
                    "type": case_data.get("type", ""),
                    "date": case_data.get("date", "")
                }
            )
            
            self.vector_store.add_documents([document])
            self.vector_store.persist()
            
            logger.info(f"成功添加案例 {case_id} 到案例库")
            return True
        
        except Exception as e:
            logger.error(f"添加案例到案例库时出错: {str(e)}")
            return False
    
    def get_case(self, case_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取特定案例"""
        file_path = os.path.join(self.case_library_path, f"{case_id}.json")
        
        if not os.path.exists(file_path):
            logger.warning(f"案例 {case_id} 不存在")
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                case_data = json.load(f)
            return case_data
        
        except Exception as e:
            logger.error(f"获取案例 {case_id} 时出错: {str(e)}")
            return None
    
    def search_similar_cases(self, query: str, k: int = 3) -> List[Document]:
        """搜索与查询相似的案例"""
        try:
            results = self.vector_store.similarity_search(query, k=k)
            return results
        except Exception as e:
            logger.error(f"搜索案例库时出错: {str(e)}")
            return []
    
    def list_all_cases(self) -> List[Dict[str, Any]]:
        """列出所有案例的基本信息"""
        try:
            cases = []
            for file in os.listdir(self.case_library_path):
                if file.endswith('.json'):
                    file_path = os.path.join(self.case_library_path, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        case_data = json.load(f)
                    
                    # 提取基本信息
                    case_info = {
                        "case_id": case_data.get("case_id", ""),
                        "title": case_data.get("title", ""),
                        "type": case_data.get("type", ""),
                        "date": case_data.get("date", "")
                    }
                    cases.append(case_info)
            
            return sorted(cases, key=lambda x: x.get("date", ""), reverse=True)
        
        except Exception as e:
            logger.error(f"列出案例库时出错: {str(e)}")
            return [] 