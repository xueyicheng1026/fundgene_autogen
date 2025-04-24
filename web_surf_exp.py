import asyncio
from autogen_agentchat.ui import Console
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
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

async def main() -> None:
    # Define an agent
    web_surfer_agent = MultimodalWebSurfer(
        name="MultimodalWebSurfer",
        headless=False,
        animate_actions=True,
        model_client=model_client,
    )

    # Define a team
    agent_team = RoundRobinGroupChat([web_surfer_agent], max_turns=3)

    # Run the team and stream messages to the console
    stream = agent_team.run_stream(task="抓取amazon上3090显卡的价格")
    await Console(stream)
    # Close the browser controlled by the agent
    await web_surfer_agent.close()

asyncio.run(main())
