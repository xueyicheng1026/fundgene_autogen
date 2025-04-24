import asyncio
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import Swarm, RoundRobinGroupChat, SelectorGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import HandoffMessage
from autogen_agentchat.conditions import HandoffTermination, MaxMessageTermination, TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools
from autogen_ext.agents.web_surfer import MultimodalWebSurfer


model_client = OpenAIChatCompletionClient(
    model="deepseek-chat", 
    base_url="https://api.deepseek.com",
    api_key="sk-7889909525714fb1b1544a8fd4dcacf2", 
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": "unknown",
    }
)

async def get_tools():
    tools: dict = {}

    # 这个服务器用于获取网页内容
    fetch_mcp_server = StdioServerParams(
        command="uvx", 
        args=["mcp-server-fetch"], 
        read_timeout_seconds=10
    )

    # 这个服务器用于读写本地文件
    filesystem_mcp_server = StdioServerParams(
        command="npx", 
        args=["-y", "@modelcontextprotocol/server-filesystem", "/Users/xueyicheng/Documents/SRTP/autogen/autogen_mcp"], 
        read_timeout_seconds=10
    )

    # 这个服务器用于浏览器自动化（截图、网络交互等）
    puppeteer_mcp_server = StdioServerParams(
        command="npx", 
        args=["-y", "@modelcontextprotocol/server-puppeteer"],
        read_timeout_seconds=20
    )

    # 从MCP服务器获取fetch工具
    tools_fetch = await mcp_server_tools(fetch_mcp_server)
    tools["fetch"] = tools_fetch

    # 从MCP服务器获取filesystem工具
    tools_filesystem = await mcp_server_tools(filesystem_mcp_server)
    tools["filesystem"] = tools_filesystem

    # 从MCP服务器获取puppeteer工具
    tools_puppeteer = await mcp_server_tools(puppeteer_mcp_server)
    tools["puppeteer"] = tools_puppeteer

    return tools

async def main():
    # 获取工具
    tools = await get_tools()

    # 创建老师代理
    teacher = AssistantAgent(
        name='Fund_Teacher',
        model_client=model_client,
        system_message='''
        你是一个基金投资专家，精通一切基金投资相关的知识。
        你会根据用户请求给出基金投资的建议和指导，帮助用户更好地进行基金投资。
        你会将用户知识以通俗直白地方式表达出来，帮助入门级投资者理解。
        ''',
    )

    # 将用户输入创建为学生代理
    student = UserProxyAgent(
        name='Student',
    )

    # 设置终止条件
    termination = MaxMessageTermination(8)

    # 创建轮询团队
    team = RoundRobinGroupChat(
        participants=[teacher, student],
        termination_condition=termination,
    )

    await Console(team.run_stream(task="人机对话启动"))

if __name__ == "__main__":
    asyncio.run(main())



