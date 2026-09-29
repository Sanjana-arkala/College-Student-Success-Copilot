"""MCP server entrypoint (stdio). Run: python -m app.mcp_server.server"""
from app.mcp_server import (attendance_tools, course_tools, marks_tools,  # noqa: F401
                            policy_tools, student_tools)
from app.mcp_server.instance import mcp

if __name__ == "__main__":
    mcp.run(transport="stdio")
