from datetime import datetime
from enum import Enum
import parlant.sdk as p

@p.tool
async def get_weather(context: p.ToolContext, city: str) -> p.ToolResult:
  """获取指定城市的天气信息"""
  # 模拟天气数据
  weather_data = {
    "北京": {"temp": "15°C", "condition": "晴", "humidity": "45%", "wind": "东北风3级"},
    "上海": {"temp": "18°C", "condition": "多云", "humidity": "60%", "wind": "东风2级"},
    "广州": {"temp": "25°C", "condition": "阴", "humidity": "75%", "wind": "南风2级"},
    "深圳": {"temp": "26°C", "condition": "晴", "humidity": "70%", "wind": "东南风3级"},
    "成都": {"temp": "20°C", "condition": "小雨", "humidity": "80%", "wind": "西风1级"},
  }
  
  if city in weather_data:
    data = weather_data[city]
    result = f"{city}天气：{data['condition']}，温度{data['temp']}，湿度{data['humidity']}，{data['wind']}"
  else:
    result = f"{city}天气：晴，温度22°C，湿度55%，微风（默认数据）"
  
  return p.ToolResult(result)

# 电信运营商相关工具
@p.tool
async def get_customer_info(context: p.ToolContext) -> p.ToolResult:
  """查询基本客户资料"""

  server = p.ToolContextAccessor(context).server
  if customer := await server.find_customer(id=context.customer_id):
      phone_number = customer.metadata.get("phone_number")

  # 模拟客户数据库
  customer_db = {
    "13812345678": {"name": "张三", "id_card": "110101199001010001", "status": "正常", "register_date": "2020-05-15"},
    "13987654321": {"name": "李四", "id_card": "320101199002020002", "status": "正常", "register_date": "2019-03-22"},
    "15612345678": {"name": "王五", "id_card": "440101199003030003", "status": "正常", "register_date": "2021-08-10"},
    "18888888888": {"name": "赵六", "id_card": "510101199004040004", "status": "欠费", "register_date": "2018-12-01"}
  }
  
  if phone_number in customer_db:
    info = customer_db[phone_number]
    result = f"客户姓名：{info['name']}，身份证：{info['id_card'][:6]}****{info['id_card'][-4:]}，状态：{info['status']}，开户日期：{info['register_date']}"
  else:
    result = f"未找到手机号{phone_number}的客户信息，请确认号码是否正确"
  
  return p.ToolResult(result)

@p.tool
async def query_balance(context: p.ToolContext) -> p.ToolResult:
  """查询话费余额"""
  # 模拟余额数据

  print(f'当前上下文信息：{context}')

  server = p.ToolContextAccessor(context).server
  if customer := await server.find_customer(id=context.customer_id):
      phone_number = customer.metadata.get("phone_number")
  
  print(f'查询话费余额，客户手机号：{phone_number}')
  balance_db = {
    "13812345678": {"balance": 85.60, "due_date": "2024-12-15"},
    "13987654321": {"balance": 23.40, "due_date": "2024-12-08"},
    "15612345678": {"balance": 156.80, "due_date": "2024-12-20"},
    "18888888888": {"balance": -12.50, "due_date": "2024-11-30"}
  }
  
  if phone_number in balance_db:
    info = balance_db[phone_number]
    if info["balance"] >= 0:
      result = f"您的话费余额为{info['balance']:.2f}元，下次缴费日期：{info['due_date']}"
    else:
      result = f"您的账户欠费{abs(info['balance']):.2f}元，请及时缴费。最后缴费日期：{info['due_date']}"
  else:
    result = f"未找到手机号{phone_number}的余额信息"
  
  return p.ToolResult(result)

@p.tool
async def query_current_plan(context: p.ToolContext) -> p.ToolResult:
  """查询当前套餐"""

  server = p.ToolContextAccessor(context).server
  if customer := await server.find_customer(id=context.customer_id):
      phone_number = customer.metadata.get("phone_number")
  
  print(f'查询当前套餐，客户手机号：{phone_number}')
  # 模拟套餐数据
  plan_db = {
    "13812345678": {"plan_id": "PLAN001", "plan_name": "畅享套餐58元", "monthly_fee": 58, "voice": "300分钟", "data": "10GB", "sms": "100条"},
    "13987654321": {"plan_id": "PLAN002", "plan_name": "无限流量88元", "monthly_fee": 88, "voice": "500分钟", "data": "无限", "sms": "200条"},
    "15612345678": {"plan_id": "PLAN003", "plan_name": "商务套餐128元", "monthly_fee": 128, "voice": "1000分钟", "data": "30GB", "sms": "500条"},
    "18888888888": {"plan_id": "PLAN001", "plan_name": "畅享套餐58元", "monthly_fee": 58, "voice": "300分钟", "data": "10GB", "sms": "100条"}
  }
  
  if phone_number in plan_db:
    plan = plan_db[phone_number]
    result = f"当前套餐：{plan['plan_name']}，月费：{plan['monthly_fee']}元，包含：通话{plan['voice']}，流量{plan['data']}，短信{plan['sms']}"
  else:
    result = f"未找到手机号{phone_number}的套餐信息"
  
  return p.ToolResult(result)

@p.tool
async def query_available_plans(context: p.ToolContext) -> p.ToolResult:

  print(f'查询可用套餐')
  print(f'当前上下文信息：{context}')
  
  """查询可用套餐"""
  # 模拟可变更的套餐列表（根据客户等级或其他条件）
  available_plans = [
    "PLAN001 - 畅享套餐58元：通话300分钟，流量10GB，短信100条",
    "PLAN002 - 无限流量88元：通话500分钟，流量无限，短信200条", 
    "PLAN003 - 商务套餐128元：通话1000分钟，流量30GB，短信500条",
    "PLAN004 - 青春套餐38元：通话200分钟，流量8GB，短信50条",
    "PLAN005 - 尊享套餐188元：通话无限，流量无限，短信无限"
  ]
  
  return p.ToolResult(data=available_plans)

class PlanID(str, Enum):
  PLAN001 = "PLAN001"
  PLAN002 = "PLAN002"
  PLAN003 = "PLAN003"
  PLAN004 = "PLAN004"
  PLAN005 = "PLAN005"

@p.tool
async def get_plan_details(context: p.ToolContext, plan_id: PlanID) -> p.ToolResult:

  print(f'查询套餐详情，套餐ID：{plan_id}')
  """查询套餐详情"""
  # 模拟详细套餐信息
  plan_details = {
    "PLAN001": {
      "name": "畅享套餐58元",
      "monthly_fee": 58,
      "voice": "300分钟",
      "data": "10GB", 
      "sms": "100条",
      "features": ["免费接听", "流量不清零", "全国通用"],
      "extra_fees": "超出部分：通话0.15元/分钟，流量3元/GB，短信0.1元/条"
    },
    "PLAN002": {
      "name": "无限流量88元",
      "monthly_fee": 88,
      "voice": "500分钟",
      "data": "无限（超40GB后限速）",
      "sms": "200条", 
      "features": ["免费接听", "流量无限", "全国通用", "5G网络"],
      "extra_fees": "超出部分：通话0.15元/分钟，短信0.1元/条"
    },
    "PLAN003": {
      "name": "商务套餐128元",
      "monthly_fee": 128,
      "voice": "1000分钟",
      "data": "30GB",
      "sms": "500条",
      "features": ["免费接听", "商务优先", "全国通用", "5G网络", "免费热点"],
      "extra_fees": "超出部分：通话0.1元/分钟，流量2元/GB，短信0.05元/条"
    },
    "PLAN004": {
      "name": "青春套餐38元", 
      "monthly_fee": 38,
      "voice": "200分钟",
      "data": "8GB",
      "sms": "50条",
      "features": ["免费接听", "学生优惠", "全国通用"],
      "extra_fees": "超出部分：通话0.2元/分钟，流量5元/GB，短信0.1元/条"
    },
    "PLAN005": {
      "name": "尊享套餐188元",
      "monthly_fee": 188,
      "voice": "无限",
      "data": "无限",
      "sms": "无限", 
      "features": ["免费接听", "VIP客服", "全国通用", "5G网络", "免费热点", "国际漫游优惠"],
      "extra_fees": "无超出费用"
    }
  }
  
  if plan_id in plan_details:
    plan = plan_details[plan_id]
    result = f"""
{plan['name']} 详细信息：
• 月费：{plan['monthly_fee']}元
• 通话：{plan['voice']}
• 流量：{plan['data']}
• 短信：{plan['sms']}
• 特色服务：{', '.join(plan['features'])}
• 超出资费：{plan['extra_fees']}
    """.strip()
  else:
    result = f"未找到套餐ID {plan_id} 的详细信息"
  
  return p.ToolResult(result)

@p.tool
async def change_plan(context: p.ToolContext, new_plan_id: PlanID) -> p.ToolResult:
  """变更套餐"""

  server = p.ToolContextAccessor(context).server
  if customer := await server.find_customer(id=context.customer_id):
      phone_number = customer.metadata.get("phone_number")

  print(f'变更套餐，客户手机号：{phone_number}，新套餐ID：{new_plan_id}')
  # 模拟套餐变更
  plan_names = {
    "PLAN001": "畅享套餐58元",
    "PLAN002": "无限流量88元", 
    "PLAN003": "商务套餐128元",
    "PLAN004": "青春套餐38元",
    "PLAN005": "尊享套餐188元"
  }
  
  if new_plan_id in plan_names:
    plan_name = plan_names[new_plan_id]
    result = f"已成功为手机号{phone_number}变更套餐至{plan_name}，新套餐将于下个月1日生效。"
  else:
    result = f"套餐ID {new_plan_id} 不存在，套餐变更失败。"
  
  return p.ToolResult(result)