# 月子中心孕产康养AI专家系统 (MCP Server)

基于AI技术的孕产康养智能咨询系统，为月子中心提供专业的客户服务支持。

## 主要功能

1. **数据采集分析**：通过Agent语音交互记录并分析宝妈生理和需求数据
2. **模型分析**：大模型+RAG检索增强，搭建私有知识库生成内调外养个性化定制方案
3. **案例库建设**：建立客户档案库，提供历史案例参考，助力服务优化

## 技术架构

- Python FastAPI 后端服务
- LangChain 知识库及智能代理
- 向量数据库实现RAG
- 大语言模型集成
- WebSocket 实时通信

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/yourusername/care-elite-server.git
cd care-elite-server

# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python app/main.py
```

## Cursor 接入指南

1. 在Cursor中通过WebSocket连接至MCP服务器
2. 发送认证请求获取会话Token
3. 通过语音API将用户对话实时转发至服务器
4. 接收服务器响应并在界面上展示

详细API文档请参考 [docs/api_reference.md](docs/api_reference.md)
