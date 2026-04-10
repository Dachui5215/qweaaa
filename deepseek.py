import streamlit as st

#大标题
# st.title("入门演示——大标题")
# st.header("一级标题")
# st.subheader("二级标题")

#文字段落
# ---------- 子页面1：用户信息 (含聊天功能) ----------


from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()  # 自动读取 .env 文件中的内容

st.title("DeepSeek 聊天测试（无需输入密钥）")

api_key = os.getenv("DEEPSEEK_API_KEY")

# 如果环境变量没读到，才提示错误，但不再显示输入框
if not api_key:
    st.error("❌ 未检测到 DEEPSEEK_API_KEY，请在项目根目录创建 .env 文件并填写密钥。")
    st.stop()  # 停止执行，不显示后续聊天界面

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# 初始化消息记录
if "msgs" not in st.session_state:
    st.session_state.msgs = []

# 显示历史对话
for msg in st.session_state.msgs:
    st.chat_message(msg["role"]).write(msg["content"])

# 用户输入
if prompt := st.chat_input("和 DeepSeek 说点什么吧..."):
    st.session_state.msgs.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=st.session_state.msgs,
                stream=False
            )
            reply = response.choices[0].message.content
            st.write(reply)

    st.session_state.msgs.append({"role": "assistant", "content": reply})