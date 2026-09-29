"""Thin MCP client: agents call tools through the MCP server over stdio."""
import json
import sys
from contextlib import asynccontextmanager

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@asynccontextmanager
async def mcp_session():
    params = StdioServerParameters(command=sys.executable, args=["-m", "app.mcp_server.server"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session


async def call_tool(session: ClientSession, name: str, args: dict, trace: list | None = None):
    result = await session.call_tool(name, args)
    text = result.content[0].text if result.content else "{}"
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        data = {"raw": text}
    if trace is not None:
        trace.append(f"MCP: {name}({', '.join(f'{k}={v}' for k, v in args.items())})")
    return data
