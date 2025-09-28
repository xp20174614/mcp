from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv
load_dotenv()

# 设置环境变量
ZAI_API_KEY= os.getenv("ZAI_API_KEY")

# 创建 LLM
llm = ChatOpenAI(
    temperature=0.6,
    model="glm-4.5",
    openai_api_key=ZAI_API_KEY,
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
)

# 创建提示模板
prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            "You are a nice chatbot having a conversation with a human."
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
)

# 创建记忆
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 创建对话链
conversation = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=memory
)

# 进行对话
response1 = conversation.invoke({"question": "tell me a joke"})
print("AI:", response1['text'])

response2 = conversation.invoke({"question": "tell me another one"})
print("AI:", response2['text'])
