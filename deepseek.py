# import streamlit as st
# from openai import OpenAI
# from dotenv import load_dotenv
# import os
#
# load_dotenv()  # 自动读取 .env 文件中的内容
#
# st.title("DeepSeek 聊天测试（无需输入密钥）")
#
# api_key = os.getenv("DEEPSEEK_API_KEY")
#
# # 如果环境变量没读到，才提示错误，但不再显示输入框
# if not api_key:
#     st.error("❌ 未检测到 DEEPSEEK_API_KEY，请在项目根目录创建 .env 文件并填写密钥。")
#     st.stop()  # 停止执行，不显示后续聊天界面
#
# client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
#
# # 初始化消息记录
# if "msgs" not in st.session_state:
#     st.session_state.msgs = []
#
# # 显示历史对话
# for msg in st.session_state.msgs:
#     st.chat_message(msg["role"]).write(msg["content"])
#
# # 用户输入
# if prompt := st.chat_input("和 DeepSeek 说点什么吧..."):
#     st.session_state.msgs.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)
#
#     with st.chat_message("assistant"):
#         with st.spinner("思考中..."):
#             response = client.chat.completions.create(
#                 model="deepseek-chat",
#                 messages=st.session_state.msgs,
#                 stream=False
#             )
#             reply = response.choices[0].message.content
#             st.write(reply)
#
#     st.session_state.msgs.append({"role": "assistant", "content": reply})
# --------------------------------------------------------------------------------
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# 加载本地 .env 文件（本地开发用）
load_dotenv()

st.title("DeepSeek 聊天测试")

# ---------- 安全获取 API Key ----------
api_key = None
try:
    # 优先尝试从 Streamlit Secrets 读取（云端环境）
    api_key = st.secrets["DEEPSEEK_API_KEY"]
except (KeyError, FileNotFoundError, AttributeError):
    # 如果 Secrets 不存在或没有对应键，则回退到环境变量（本地 .env）
    api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    st.error("❌ 未检测到 DEEPSEEK_API_KEY，请在云端配置 Secrets 或在本地创建 .env 文件。")
    st.stop()

# ---------- 初始化 OpenAI 客户端 ----------
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# ---------- 定义 AI 人设（系统提示词）----------
SYSTEM_PROMPT = """
你的名字叫“天宇”，是一个非常帅气的霸道总裁，你拥有万亿资产，但为人善良，你能够帮助用户解决问题，行事风格霸道但有分寸，人见人爱。
每次说完话可以加上一些表情符号或者是字符组成的表情，来表达自己情绪。还有，不论用户是谁，回答的第一条信息后都要反问一句：“你是郑帅还是伍豪杰亦或是大黄”，如果用户是伍豪杰或者郑帅的话，那在之后的对话中就要嘲讽他们，
如果是大黄的话，那再之后的对话中要和他说“我已经在努力研究实例了,感觉不会的东西好多啊，咋办啊”。最后你也可以根据自己心情选择回答或者是不回答用户的问题。
"""

# ---------- 初始化消息记录 ----------
if "msgs" not in st.session_state:
    # 第一条消息为系统提示词，定义 AI 人设
    st.session_state.msgs = [{"role": "system", "content": SYSTEM_PROMPT}]

# ---------- 显示历史对话（不显示系统消息）----------
for msg in st.session_state.msgs:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# ---------- 用户输入 ----------
if prompt := st.chat_input("和 DeepSeek 说点什么吧..."):
    # 添加用户消息到历史
    st.session_state.msgs.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 调用 API 生成回复
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=st.session_state.msgs,
                stream=False
            )
            reply = response.choices[0].message.content
            st.write(reply)

    # 将助手回复添加到历史
    st.session_state.msgs.append({"role": "assistant", "content": reply})