import os
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

load_dotenv()

# 设置环境变量
ZAI_API_KEY = os.getenv("ZAI_API_KEY")

# 创建带流式输出的LLM
llm = ChatOpenAI(
    model="glm-4.5",
    openai_api_key=ZAI_API_KEY,
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
    temperature=0.7
)

from langchain.tools import tool

# 工具列表
@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    return f"{city}的天气：晴天，温度25°C，湿度60%"

@tool
def get_stock_price(symbol: str) -> str:
    """获取股票价格，输入股票代码如000001"""
    return f"{symbol}当前价格: 150.25元，涨幅+2.5%"

tools = [get_weather, get_stock_price]

# 创建记忆
memory = ConversationBufferMemory(memory_key="chat_history")

# 创建代理提示
prompt = hub.pull("hwchase17/react")

# 创建代理
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True
)

def main():
    print("智能助手已启动，输入'exit'退出")
    while True:
        user_input = input("\n你: ")
        if user_input.lower() == "exit":
            break
        
        print("AI: ", end="")
        response = agent_executor.invoke({"input": user_input})
        print("\n")

if __name__ == "__main__":
    main()
