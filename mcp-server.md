python sdk 开发 mcp-server 天气查询案例：

构建您的服务器
导入包并设置实例
在您的 weather.py 文件顶部添加以下内容：


Copy
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# 初始化 FastMCP 服务器
mcp = FastMCP("weather")

# 常量
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"
FastMCP 类使用 Python 类型提示和文档字符串自动生成工具定义，使创建和维护 MCP 工具变得简单。

辅助函数
接下来，添加用于查询和格式化美国国家气象服务 API 数据的辅助函数：


Copy
async def make_nws_request(url: str) -> dict[str, Any] | None:
    """向 NWS API 发送请求并进行适当的错误处理。"""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """将警报特征格式化为可读字符串。"""
    props = feature["properties"]
    return f"""
事件: {props.get('event', '未知')}
区域: {props.get('areaDesc', '未知')}
严重性: {props.get('severity', '未知')}
描述: {props.get('description', '无描述可用')}
指示: {props.get('instruction', '无具体指示提供')}
"""
实现工具执行
工具执行处理程序负责实际执行每个工具的逻辑。让我们添加它：


Copy
@mcp.tool()
async def get_alerts(state: str) -> str:
    """获取美国某个州的天气警报。

    参数：
        state: 两位美国州代码（例如 CA, NY）
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "无法获取警报或未找到警报。"

    if not data["features"]:
        return "此州没有活跃警报。"

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """获取某个位置的天气预报。

    参数：
        latitude: 位置的纬度
        longitude: 位置的经度
    """
    # 首先获取预报网格端点
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "无法为此位置获取预报数据。"

    # 从点响应中获取预报 URL
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "无法获取详细预报。"

    # 将周期格式化为可读的预报
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # 仅显示接下来的 5 个周期
        forecast = f"""
{period['name']}：
温度: {period['temperature']}°{period['temperatureUnit']}
风速: {period['windSpeed']} {period['windDirection']}
预报: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)
运行服务器
最后，初始化并运行服务器：


Copy
if __name__ == "__main__":
    # 初始化并运行服务器
    mcp.run(transport='stdio')
您的服务器已完成！运行 uv run weather.py 以确认一切正常。