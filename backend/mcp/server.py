from fastmcp import FastMCP
from tools import fetch_canadian_rates


# 1. 实例化 FastMCP，这会自动处理底层协议和 Stdio 交互
mcp = FastMCP("FinAgent-Toolserver")


@mcp.tool()
async def get_client_credit_context(client_id: str) -> dict:
    """从内部受保护的系统获取客户信用评分和违约历史。"""
    mock_database = {
        "C001": {"score": 750, "history": "Clean", "limit": 50000},
        "C002": {"score": 580, "history": "1 Default", "limit": 5000}
    }
    # 返回字典，FastMCP 会自动序列化为 JSON
    return mock_database.get(client_id, {"score": 600, "history": "Unknown", "limit": 0})


@mcp.tool()
async def check_fraud_blacklist(name: str) -> bool:
    """检查客户姓名是否在银行合规黑名单中。"""
    blacklist = ["Bad Actor Inc", "Fraudulent Entity"]
    return name in blacklist


@mcp.tool()
async def get_macro_context(country: str = "Canada") -> str:
    """
    调用外部搜索工具获取指定国家的实时宏观经济数据和利率。
    用于风险评估时参考外部经济环境。
    """
    if country.lower() == "canada":
        data = await fetch_canadian_rates()
        return str(data)
    return "Market data for this region is currently unavailable."


if __name__ == "__main__":
    # FastMCP 默认会根据运行环境选择 stdio 或其他模式
    # 在这个项目中，它将作为子进程通过标准输入输出与 LangGraph 通信
    mcp.run()