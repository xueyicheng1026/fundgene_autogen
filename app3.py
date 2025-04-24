import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat, SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_core import CancellationToken
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools

model_client = OpenAIChatCompletionClient(
    model="deepseek-chat", 
    base_url="https://api.deepseek.com",
    api_key="sk-7889909525714fb1b1544a8fd4dcacf2", 
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": "unknown",
    },
)

async def main():
    # 设置MCP fetch服务器参数
    # 这个服务器用于获取网页内容
    fetch_mcp_server = StdioServerParams(command="uvx", args=["mcp-server-fetch"], read_timeout_seconds=10)

    # 设置MCP文件系统服务器参数
    # 这个服务器用于写入本地文件
    write_mcp_server = StdioServerParams(command="npx", args=["-y", "@modelcontextprotocol/server-filesystem", "/Users/xueyicheng/Documents/SRTP/autogen/autogen_mcp"], read_timeout_seconds=10)

    # 从MCP服务器获取fetch工具
    tools_fetch = await mcp_server_tools(fetch_mcp_server)

    # 从MCP服务器获取filesystem工具
    tools_write = await mcp_server_tools(write_mcp_server)

    #创建