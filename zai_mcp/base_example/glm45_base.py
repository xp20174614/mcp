from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os


from dotenv import load_dotenv
load_dotenv()

# 设置环境变量
ZAI_API_KEY= os.getenv("ZAI_API_KEY")

# 创建 LLM 实例
llm = ChatOpenAI(
    temperature=0.7,
    model="glm-4.5",
    openai_api_key=ZAI_API_KEY,
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
)

# 创建消息
messages = [
    SystemMessage(content="你是一个有用的 AI 助手"),
    HumanMessage(content="请介绍一下人工智能的发展历程")
]

# 调用模型
response = llm(messages)
print(response.content)
