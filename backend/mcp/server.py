from fastmcp import FastMCP
from tools import fetch_canadian_rates


# 1. instantiate FastMCP, this will automatically handle the underlying protocol and Stdio interaction
mcp = FastMCP("FinAgent-Toolserver")


@mcp.tool()
async def get_client_credit_context(client_id: str) -> dict:
    """fetch client credit score and default history from internal protected system."""
    mock_database = {
        "C001": {"score": 750, "history": "Clean", "limit": 50000},
        "C002": {"score": 580, "history": "1 Default", "limit": 5000}
    }
    # return dict and FastMCP will serialize it to json
    return mock_database.get(client_id, {"score": 600, "history": "Unknown", "limit": 0})


@mcp.tool()
async def check_fraud_blacklist(name: str) -> bool:
    """check if the customer name is in the bank's compliance blacklist."""
    blacklist = ["Bad Actor Inc", "Fraudulent Entity"]
    return name in blacklist


@mcp.tool()
async def get_macro_context(country: str = "Canada") -> str:
    """
    call external search tool to get real-time macroeconomic data and interest rates for the specified country.
    This is used as a reference for the external economic environment during risk assessment.
    """
    if country.lower() == "canada":
        data = await fetch_canadian_rates()
        return str(data)
    return "Market data for this region is currently unavailable."


if __name__ == "__main__":
    # it will act as the child process communicating with LangGraph via stdin/stdout
    mcp.run()