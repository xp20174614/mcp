import os
import sys
sys.path.append("C:\\secret")

from dotenv import load_dotenv
load_dotenv()

# 使用智谱AI的官方SDK
from zhipuai import ZhipuAI

def test_glm45():
    """测试GLM-4.5模型"""
    
    # 初始化智谱AI客户端
    client = ZhipuAI(api_key=os.getenv("ZAI_API_KEY"))
    
    # 创建对话消息
    messages = [
        {"role": "system", "content": "你是一个有用的AI助手"},
        {"role": "user", "content": "请介绍一下人工智能的发展历程"}
    ]
    
    try:
        # 调用GLM-4.5模型
        response = client.chat.completions.create(
            model="glm-4",  # GLM-4是最新版本
            messages=messages,
            temperature=0.7
        )
        
        print("=== GLM-4.5 响应 ===")
        print(response.choices[0].message.content)
        
    except Exception as e:
        print(f"API调用失败: {e}")
        print("请检查：")
        print("1. ZAI_API_KEY环境变量是否设置正确")
        print("2. 网络连接是否正常")
        print("3. API密钥是否有有效权限")

if __name__ == "__main__":
    test_glm45()
