from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

# 设置环境变量
ZAI_API_KEY= os.getenv("ZAI_API_KEY")

# 创建 LLM
llm = ChatOpenAI(
    model="glm-4.5",
    openai_api_key=ZAI_API_KEY,
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
)

# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的{domain}专家"),
    ("human", "请解释一下{topic}的概念和应用")
])

# 创建链
chain = prompt | llm

# 调用链
response = chain.invoke({
    "domain": "机器学习",
    "topic": "深度学习"
})

print(response.content)
