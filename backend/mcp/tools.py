from fastmcp import FastMCP
import httpx

# 创建 MCP 实例
mcp = FastMCP("FinanceData")

@mcp.tool()
async def get_macro_rates(country: str = "Canada") -> str:
    """获取指定国家的最新基准利率和宏观经济简报。"""
    # 在实际生产中，这里会调用类似 Alpha Vantage 或 NewsAPI 的 MCP SDK
    # 模拟一个实时查询结果
    if country.lower() == "canada":
        return "Bank of Canada current policy rate is 5.00%. Inflation is cooling to 2.8%."
    else:
        return f"Current base rate for {country} is approximately 5.25% based on latest Fed data."

if __name__ == "__main__":
    mcp.run()