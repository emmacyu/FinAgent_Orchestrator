# backend/mcp/tools.py
from langchain_community.tools.tavily_search import TavilySearchResults


def get_market_search_tool():
    """返回一个配置好的 Tavily 搜索工具实例"""
    # 确保你的 .env 或 Docker 环境中有 TAVILY_API_KEY
    return TavilySearchResults(max_results=2)


async def fetch_canadian_rates():
    """
    专门用于获取加拿大宏观利率的函数
    """
    search = get_market_search_tool()
    query = "current Bank of Canada overnight rate March 2026"
    try:
        results = await search.ainvoke(query)
        return results
    except Exception as e:
        return f"Error fetching market data: {str(e)}"