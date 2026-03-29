import asyncio
import sys
import os
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


server_params = StdioServerParameters(
    command=sys.executable,
    args=[os.path.join(os.path.dirname(os.path.abspath(__file__)), "server.py")],
    env=os.environ.copy()
)


async def call_mcp_tool(tool_name: str, arguments: dict):
    """
    自包含的原子调用，解决 Cancel Scope 跨 Task 报错问题。
    """
    try:
        # 1. start the child process
        async with stdio_client(server_params) as (read, write):
            # 2. create Session
            async with ClientSession(read, write) as session:
                # 3. initialize and set strict timeout
                # Note: Do not wrap too much wait_for externally, let initialize handle it internally
                await asyncio.wait_for(session.initialize(), timeout=5.0)

                # 4. call tool
                result = await session.call_tool(tool_name, arguments)

                # 5. parse and return
                if result and result.content:
                    raw_text = result.content[0].text
                    try:
                        return json.loads(raw_text)
                    except:
                        return raw_text
                return None
    except asyncio.TimeoutError:
        print(f"MCP Timeout: {tool_name} failed to respond.")
        return {"error": "timeout"}
    except Exception as e:
        # capture the subprocess startup failure or protocol error
        print(f"MCP Critical Error: {e}")
        return {"error": str(e)}