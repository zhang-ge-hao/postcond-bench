import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console

from src.agent.proto_v2.models import client

# 1) 定义工具：强烈建议写 docstring + type hints
async def add(a: int, b: int) -> int:
    """Add two integers and return the sum."""
    return a + b

async def main():
    model_client = client("Qwen/Qwen3-32B", thinking=True)

    agent = AssistantAgent(
        name="assistant",
        model_client=model_client,
        tools=[add],                   # ✅ 注册工具
        max_tool_iterations=5,         # 允许多轮 tool calls
        reflect_on_tool_use=True,      # tool 调用完给个最终总结
    )

    await Console(agent.run_stream(task="Compute 23+19 using the tool, then reply with just the number."))

    await model_client.close()

if __name__ == "__main__":
    asyncio.run(main())
