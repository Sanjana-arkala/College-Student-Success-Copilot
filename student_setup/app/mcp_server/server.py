"""MCP server entrypoint (stdio). Run: python -m app.mcp_server.server"""
from app.mcp_server import (student_tools)
from app.mcp_server.instance import mcp
from app.mcp_server import attendance_tools, course_tools, marks_tools, policy_tools

if __name__ == "__main__":
    mcp.run(transport="stdio")

