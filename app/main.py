import os
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api.router import api_router
from app.core.config import settings
from app.services.websocket_manager import ConnectionManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("mcp-server")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="月子中心孕产康养AI专家系统API",
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含API路由
app.include_router(api_router, prefix=settings.API_PREFIX)

# WebSocket连接管理器
manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            # 处理接收到的数据
            response = await manager.process_message(client_id, data)
            await manager.send_message(client_id, response)
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        logger.info(f"客户端 {client_id} 已断开连接")

@app.on_event("startup")
async def startup_event():
    logger.info("MCP服务器启动中...")
    # 初始化服务

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("MCP服务器关闭中...")
    # 清理资源

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG_MODE
    ) 