# backend/mcp/tools.py
from langchain_community.tools.tavily_search import TavilySearchResults


def get_market_search_tool():
    """return a configured Tavily search tool instance"""
    # ensure TAVILY_API_KEY in .env
    return TavilySearchResults(max_results=2)


async def fetch_canadian_rates():
    """
    used for fetching Canadian macroeconomic rates.
    """
    search = get_market_search_tool()
    query = "current Bank of Canada overnight rate March 2026"
    try:
        results = await search.ainvoke(query)
        return results
    except Exception as e:
        return f"Error fetching market data: {str(e)}"