from fastapi import FastAPI
from pydantic import BaseModel
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class QueryRequest(BaseModel):
    input: str

# 初始化LLM
llm = ChatOpenAI(
    model="glm-4.5",
    openai_api_key=os.getenv("ZAI_API_KEY"),
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/",
    temperature=0.7
)

# 工具定义
@tool
def get_weather(city: str) -> str:
    """获取城市天气信息"""
    return f"Weather in {city}: Sunny, 25C"

@tool
def get_stock_price(symbol: str) -> str:
    """获取股票价格"""
    return f'{{"symbol":"{symbol}","price":150.25,"change":"+2.5%"}}'

# 创建代理
tools = [get_weather, get_stock_price]
memory = ConversationBufferMemory(memory_key="chat_history")
agent = create_react_agent(llm, tools, hub.pull("hwchase17/react"))
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True
)

@app.post("/query")
async def process_query(request: QueryRequest):
    """MCP服务API端点"""
    result = agent_executor.invoke({"input": request.input})
    return {"output": result['output']}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)