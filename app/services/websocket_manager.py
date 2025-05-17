import json
import logging
from typing import Dict, Any
from fastapi import WebSocket
from app.services.ai_service import AIService

logger = logging.getLogger("mcp-server")

class ConnectionManager:
    def __init__(self):
        # 活跃的WebSocket连接
        self.active_connections: Dict[str, WebSocket] = {}
        # 用户会话状态
        self.sessions: Dict[str, Any] = {}
        # AI服务
        self.ai_service = AIService()
        
    async def connect(self, websocket: WebSocket, client_id: str):
        """建立新的WebSocket连接"""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        self.sessions[client_id] = {
            "context": [],
            "customer_profile": {},
            "interaction_stage": "initial"
        }
        logger.info(f"客户端 {client_id} 已连接")
        
    def disconnect(self, client_id: str):
        """断开WebSocket连接"""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        if client_id in self.sessions:
            del self.sessions[client_id]
            
    async def send_message(self, client_id: str, message: str):
        """向指定客户端发送消息"""
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)
    
    async def broadcast(self, message: str):
        """向所有连接的客户端广播消息"""
        for connection in self.active_connections.values():
            await connection.send_text(message)
            
    async def process_message(self, client_id: str, message: str) -> str:
        """处理从客户端接收到的消息"""
        try:
            data = json.loads(message)
            message_type = data.get("type", "")
            
            if message_type == "speech":
                # 处理语音输入
                text = data.get("text", "")
                speaker = data.get("speaker", "customer")  # 发言者：customer/sales
                
                # 更新会话上下文
                self.sessions[client_id]["context"].append({
                    "role": speaker,
                    "content": text
                })
                
                # 根据当前阶段进行处理
                stage = self.sessions[client_id]["interaction_stage"]
                if stage == "initial":
                    # 初始接待阶段，主要收集基本信息
                    return await self.handle_initial_stage(client_id, text, speaker)
                elif stage == "tour":
                    # 参观阶段，收集客户反馈
                    return await self.handle_tour_stage(client_id, text, speaker)
                elif stage == "consultation":
                    # 咨询阶段，提供专业建议
                    return await self.handle_consultation_stage(client_id, text, speaker)
                elif stage == "case_presentation":
                    # 案例展示阶段，匹配相似案例
                    return await self.handle_case_presentation(client_id, text, speaker)
                else:
                    return json.dumps({
                        "type": "error",
                        "message": "未知的交互阶段"
                    })
            
            elif message_type == "command":
                # 处理销售发出的指令
                command = data.get("command", "")
                return await self.handle_command(client_id, command)
            
            elif message_type == "stage_change":
                # 改变当前交互阶段
                new_stage = data.get("stage", "")
                if new_stage in ["initial", "tour", "consultation", "case_presentation"]:
                    self.sessions[client_id]["interaction_stage"] = new_stage
                    return json.dumps({
                        "type": "stage_change",
                        "stage": new_stage,
                        "message": f"已切换到{new_stage}阶段"
                    })
                else:
                    return json.dumps({
                        "type": "error",
                        "message": "无效的交互阶段"
                    })
            
            else:
                return json.dumps({
                    "type": "error",
                    "message": "未知的消息类型"
                })
                
        except Exception as e:
            logger.error(f"处理消息时出错: {str(e)}")
            return json.dumps({
                "type": "error",
                "message": f"处理消息时出错: {str(e)}"
            })
    
    async def handle_initial_stage(self, client_id: str, text: str, speaker: str) -> str:
        """处理初始接待阶段"""
        # 在初始阶段，我们主要收集客户基本信息
        if speaker == "customer":
            # 使用AI分析客户的回答，提取关键信息
            extracted_info = await self.ai_service.extract_customer_info(text)
            
            # 更新客户资料
            self.sessions[client_id]["customer_profile"].update(extracted_info)
            
            return json.dumps({
                "type": "info_collection",
                "extracted": extracted_info
            })
        else:
            # 销售人员的发言，只记录不特殊处理
            return json.dumps({
                "type": "acknowledgement",
                "message": "已记录销售话术"
            })
    
    async def handle_tour_stage(self, client_id: str, text: str, speaker: str) -> str:
        """处理参观阶段"""
        # 在参观阶段，我们记录客户对设施和服务的反馈
        if speaker == "customer":
            # 分析客户反馈，识别兴趣点和关注点
            feedback_analysis = await self.ai_service.analyze_customer_feedback(text)
            
            # 更新客户资料中的兴趣点
            customer_profile = self.sessions[client_id]["customer_profile"]
            if "interests" not in customer_profile:
                customer_profile["interests"] = []
            customer_profile["interests"].extend(feedback_analysis.get("interests", []))
            
            return json.dumps({
                "type": "feedback_analysis",
                "analysis": feedback_analysis
            })
        else:
            return json.dumps({
                "type": "acknowledgement",
                "message": "已记录介绍内容"
            })
    
    async def handle_consultation_stage(self, client_id: str, text: str, speaker: str) -> str:
        """处理咨询阶段"""
        # 在咨询阶段，AI需要回答客户的专业问题或提供个性化建议
        if speaker == "customer":
            # 获取客户资料
            customer_profile = self.sessions[client_id]["customer_profile"]
            # 获取会话上下文
            context = self.sessions[client_id]["context"]
            
            # 生成专业回答
            response = await self.ai_service.generate_professional_response(
                text, customer_profile, context
            )
            
            return json.dumps({
                "type": "ai_response",
                "response": response
            })
        else:
            return json.dumps({
                "type": "acknowledgement",
                "message": "已记录销售提问"
            })
    
    async def handle_case_presentation(self, client_id: str, text: str, speaker: str) -> str:
        """处理案例展示阶段"""
        # 在案例展示阶段，AI需要匹配相似案例并提供参考
        customer_profile = self.sessions[client_id]["customer_profile"]
        
        # 查找相似案例
        similar_cases = await self.ai_service.find_similar_cases(customer_profile)
        
        return json.dumps({
            "type": "similar_cases",
            "cases": similar_cases
        })
    
    async def handle_command(self, client_id: str, command: str) -> str:
        """处理销售发出的指令"""
        if "小美" in command:
            # 提取实际指令内容
            prompt = command.split("小美")[1].strip()
            if not prompt.endswith("?") and not prompt.endswith("？"):
                prompt += "?"
                
            # 获取客户资料
            customer_profile = self.sessions[client_id]["customer_profile"]
            customer_name = customer_profile.get("name", "客户")
            
            # 生成AI回应
            response = await self.ai_service.generate_sales_assistant_response(
                prompt, customer_profile, self.sessions[client_id]["context"]
            )
            
            return json.dumps({
                "type": "ai_command_response",
                "response": response
            })
        else:
            return json.dumps({
                "type": "error",
                "message": "无效的指令格式"
            }) 