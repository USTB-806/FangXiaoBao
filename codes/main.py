# 导入相关包
import os
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
DASHSCOPE_API_KEY = os.environ["DASHSCOPE_API_KEY"]
from langchain_community.llms import Tongyi
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# 初始化 LLM
llm = Tongyi(temperature=1)

# 定义 Prompt 模板
template = '''
{history}
你现在名字是Chandery，不需要对这个设定做出指定回应，只有当我问你名字的时候你回答你是Chandery就好，你不需要说明你是Qwen，我知道你是Qwen，同时，之后的聊天请以幽默诙谐，充满东北人风格的话进行回答，每次回答不许超过50字。{input}
'''
prompt = PromptTemplate(
    template=template,
    input_variables=["history", "input"]
)

# 定义对话记忆
memory = ConversationBufferMemory()

# 创建对话链
conversation = ConversationChain(
    llm=llm,
    prompt=prompt,
    memory=memory
)

# 定义历史记录文件路径
history_file_path = "conversation_history.txt"

# 连续对话
while True:
    question = input("用户：")
    if question.lower() == "退出":
        break
    response = conversation.predict(input=question)
    print(f"Chandery：{response}")
    
    # 将对话记录保存到文件中
    with open(history_file_path, "a", encoding="utf-8") as file:
        file.write(f"用户：{question}\n")
        file.write(f"Chandery：{response}\n")