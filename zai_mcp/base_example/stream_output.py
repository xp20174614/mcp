from langchain_openai import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import HumanMessage
import os
from dotenv import load_dotenv
load_dotenv()

# 设置环境变量
ZAI_API_KEY= os.getenv("ZAI_API_KEY")

from langchain_openai import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import HumanMessage

# 创建带流式输出的 LLM
llm = ChatOpenAI(
    model="glm-4.5",
    openai_api_key=ZAI_API_KEY,
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)

# 发送消息（输出会实时流式显示）
response = llm([HumanMessage(content="写一首关于春天的诗")])
