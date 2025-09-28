import os
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

# 设置环境变量
ZAI_API_KEY= os.getenv("ZAI_API_KEY")

@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    # 这里应该调用真实的天气 API
    # 示例返回
    return f"{city} 的天气：晴天，温度 25°C，湿度 60%"

@tool
def get_stock_price(symbol):
    """获取股票价格"""
    # 模拟股票 API 调用
    return {
        "symbol": symbol,
        "price": 150.25,
        "change": "+2.5%"
    }

# 创建 LLM
llm = ChatOpenAI(
    model="glm-4-plus",
    openai_api_key=ZAI_API_KEY,
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/",
    streaming=True,
)

# 工具列表
tools = [get_weather, get_stock_price]

# 创建代理
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=3)

# 使用代理
result = agent_executor.invoke({"input": "北京今天天气怎么样？然后帮我查询股票价格，股票代码是 000001"})
print(result['output'])
