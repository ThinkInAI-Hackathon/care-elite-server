import os
import logging
from typing import List, Optional
from langchain.vectorstores import Chroma
from langchain.embeddings.base import Embeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader, TextLoader

from app.core.config import settings

logger = logging.getLogger("mcp-server")

class KnowledgeBase:
    def __init__(self, embeddings: Embeddings):
        """初始化知识库"""
        self.embeddings = embeddings
        self.vector_store_path = settings.VECTOR_DB_PATH
        self.knowledge_base_path = settings.KNOWLEDGE_BASE_PATH
        
        # 确保向量数据库目录存在
        os.makedirs(self.vector_store_path, exist_ok=True)
        
        # 加载向量数据库
        self._load_vector_store()
        
        # 初始化文本分割器
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
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
                logger.info("向量数据库为空，准备初始化")
                self._initialize_knowledge_base()
            else:
                logger.info(f"成功加载向量数据库，包含 {self.vector_store._collection.count()} 条记录")
        
        except Exception as e:
            logger.error(f"加载向量数据库时出错: {str(e)}")
            logger.info("创建新的向量数据库")
            self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self):
        """初始化知识库，将知识库文件加载到向量数据库中"""
        # 检查知识库目录是否存在
        if not os.path.exists(self.knowledge_base_path):
            logger.warning(f"知识库目录 {self.knowledge_base_path} 不存在，创建空目录")
            os.makedirs(self.knowledge_base_path, exist_ok=True)
            return
        
        try:
            # 使用DirectoryLoader加载知识库目录中的所有文本文件
            loader = DirectoryLoader(
                self.knowledge_base_path,
                glob="**/*.{txt,md,pdf}",  # 支持的文件类型
                loader_cls=TextLoader
            )
            
            # 加载文档
            documents = loader.load()
            
            if not documents:
                logger.warning("知识库目录中没有找到文档")
                return
                
            logger.info(f"从知识库中加载了 {len(documents)} 个文档")
            
            # 分割文档
            texts = self.text_splitter.split_documents(documents)
            logger.info(f"文档被分割为 {len(texts)} 个片段")
            
            # 创建向量数据库
            self.vector_store = Chroma.from_documents(
                documents=texts,
                embedding=self.embeddings,
                persist_directory=self.vector_store_path
            )
            
            # 持久化向量数据库
            self.vector_store.persist()
            logger.info("向量数据库初始化完成并已持久化")
            
        except Exception as e:
            logger.error(f"初始化知识库时出错: {str(e)}")
            # 创建一个空的向量数据库
            self.vector_store = Chroma(
                persist_directory=self.vector_store_path,
                embedding_function=self.embeddings
            )
    
    def add_documents(self, documents: List[Document]):
        """向知识库添加文档"""
        try:
            # 分割文档
            texts = self.text_splitter.split_documents(documents)
            
            # 添加到向量数据库
            self.vector_store.add_documents(texts)
            
            # 持久化更改
            self.vector_store.persist()
            
            logger.info(f"成功添加 {len(texts)} 个文档片段到知识库")
            return True
        except Exception as e:
            logger.error(f"添加文档到知识库时出错: {str(e)}")
            return False
    
    def search(self, query: str, k: int = 5) -> List[Document]:
        """搜索与查询相似的文档"""
        try:
            results = self.vector_store.similarity_search(query, k=k)
            return results
        except Exception as e:
            logger.error(f"搜索知识库时出错: {str(e)}")
            return []
    
    @property
    def retriever(self):
        """获取知识库的检索器"""
        return self.vector_store.as_retriever(search_kwargs={"k": 5}) 