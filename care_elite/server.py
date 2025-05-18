# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# """
# 月子中心专家Agent的MCP服务器实现
# """

# from typing import Any, Dict, List
# from mcp.server.fastmcp import FastMCP

# # 导入工具实现
# from care_elite.tools.information_collector import collect_information
# from care_elite.tools.service_recommender import recommend_service
# from care_elite.tools.case_presenter import present_case


# def create_mcp_server() -> FastMCP:
#     """创建并配置MCP服务器实例"""
#     # 初始化 FastMCP 服务器
#     mcp = FastMCP("care-elite")

#     # 注册工具
#     @mcp.tool()
#     async def collect_user_information(audio_data: str, role: str) -> Dict[str, Any]:
#         """收集并分析用户语音信息，生成用户画像。
        
#         参数:
#             audio_data: 音频数据(Base64编码)
#             role: 发言角色，可选值: "user"(用户) 或 "sales"(销售)
        
#         返回:
#             提取的用户信息和更新后的用户画像
#         """
#         return await collect_information(audio_data, role)

#     @mcp.tool()
#     async def recommend_user_service(user_profile_id: str, query: str = None) -> Dict[str, Any]:
#         """基于用户画像，推荐合适的服务话术。
        
#         参数:
#             user_profile_id: 用户画像ID
#             query: 可选的查询语句，用于精确匹配服务推荐
            
#         返回:
#             推荐的服务信息和话术内容
#         """
#         return await recommend_service(user_profile_id, query)
    
#     @mcp.tool()
#     async def present_success_case(user_profile_id: str, case_type: str = "similar") -> Dict[str, Any]:
#         """展示与用户情况相近的成功合作案例
        
#         参数:
#             user_profile_id: 用户画像ID
#             case_type: 案例类型，可选值: "similar"(相似案例), "best"(最佳案例)
            
#         返回:
#             匹配的案例信息
#         """
#         return await present_case(user_profile_id, case_type)
    
#     return mcp 