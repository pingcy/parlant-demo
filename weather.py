import parlant.sdk as p
import asyncio
from tools import get_weather

async def main():
    async with p.Server() as server:
        agent = await server.create_agent(name="WeatherBot", description="中文智能天气助手")
        
        # 添加约束规则
        await agent.create_guideline(
            condition="用户询问指定地点的天气",
            action="查询指定地点的天气信息",
            tools=[get_weather]
        )
        # 定义对话流程（对话状态）
        journey = await agent.create_journey(title="天气查询", description="帮助客户查询到指定地点的天气",conditions=["客户询问天气"])
        await journey.initial_state.transition_to(chat_state="询问城市名称")

if __name__ == "__main__":
    asyncio.run(main())

