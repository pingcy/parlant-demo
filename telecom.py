import parlant.sdk as p
from tools import (
    get_customer_info, query_balance, query_current_plan, 
    query_available_plans, get_plan_details, change_plan
)

async def add_telecom_glossary(agent: p.Agent) -> None:
    """添加电信业务术语"""
    await agent.create_term(
        name="营业厅工作时间",
        description="周一至周日 9:00-18:00，节假日正常营业"
    )
    await agent.create_term(
        name="话费",
        description="客户账户中的预付费余额或后付费账单金额"
    )
    await agent.create_term(
        name="套餐",
        description="包含通话、流量、短信的资费方案组合"
    )
    await agent.create_term(
        name="流量",
        description="手机上网使用的数据流量，单位为GB"
    )
    await agent.create_term(
        name="漫游",
        description="在非归属地使用手机服务"
    )
    await agent.create_term(
        name="5G网络",
        description="第五代移动通信技术，提供更快的网络速度"
    )

async def create_plan_change_journey(agent: p.Agent) -> p.Journey:
    """创建套餐变更旅程"""
    journey = await agent.create_journey(
        title="话费套餐变更",
        description="帮客户找到合适的话费套餐并完成变更",
        conditions=["仅当客户明确表示需要变更话费套餐"],
    )

    #标准化回复
    response_plans = await journey.create_canned_response(
        template="以下是您可以选择的话费套餐：{{std.variables.available_plans}}, 请问您想要变更到哪个套餐？",
        tags=[p.Tag.preamble()],
    )

    t1 = await journey.initial_state.transition_to(chat_state="列出可以变更的套餐，然后询问客户需要变更到哪个套餐",canned_responses=[response_plans])
    t2 = await t1.target.transition_to(chat_state="询问客户是否确认本次变更",condition="客户选择变更到某一个新的业务套餐")

    t31 = await t2.target.transition_to(tool_state=change_plan,condition="客户确认需要变更到该套餐",tool_instruction="new_plan_id参数值从可用的套餐中提取")
    await t2.target.transition_to(state=t1.target,condition="客户表示还需要再考虑一下")

    t4 = await t31.target.transition_to(chat_state="根据变更的结果告知客户变更成功或者失败",condition="套餐变更结束")
    await t4.target.transition_to(state=p.END_JOURNEY)

    await journey.create_guideline(
        condition="客户明确表示需要深入了解某个套餐的详细信息",
        action="查询某个套餐的详细信息并告知客户,plan_id从客户对话中提取",
        tools=[get_plan_details],
    )

    return journey

async def main() -> None:
    
    try:
        # 创建服务器使用OpenAI服务
        async with p.Server(
            nlp_service=p.NLPServices.openai
        ) as server:

            agent = await server.create_agent(
                name="10086客服小助手",
                description="专业友好的电信运营商客户服务代表，提供话费查询、套餐变更等服务。",
                composition_mode=p.CompositionMode.FLUID
            )

            customer = await server.create_customer(name="秋山墨客",metadata={"phone_number": "13812345678"}) 

            # 标准化回复
            welcome = await agent.create_canned_response(
                template="你好！{{std.customer.name}}, 很高兴为您服务。请问有什么可以帮您？"
            )

            # 变量
            available_plans = await agent.create_variable(
                name="available_plans",
                description="客户可以选择的套餐列表",
                tool=query_available_plans,
                freshness_rules='0 * * * *'
            )

            # 术语
            await agent.create_term(
                name="营业时间",
                description="营业时间是周一至周五，上午9点到下午6点。",
            )
            await agent.create_term(
                name="至尊套餐",
                description="至尊套餐是最高级别的188元套餐",
            )
                    
            # 添加准则
            await agent.create_guideline(
                condition="客户进行日常闲聊",
                action="友好回应，但适当引导到业务服务话题。", 
                canned_responses=[welcome]
            )

            await agent.create_guideline(
                condition="当客户明确表达出对服务不满意或有投诉、转网的意图",
                action="首先表示歉意，并表示将会让客户经理联系客户，了解客户需求并提供帮助。"
            )
            
            #查询话费
            query_journey = await agent.create_guideline(
                condition="仅当客户明确要求查询自己当前的话费余额",
                action="使用query_balance工具查询并告知客户当前余额",
                tools=[query_balance]
            )

            # 创建套餐变更旅程
            change_journey = await create_plan_change_journey(agent)

    except KeyboardInterrupt:
        print("\n客服: 感谢您使用我们的客户服务系统，再见！👋")
    except Exception as e:
        print(f"系统启动失败：{e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
