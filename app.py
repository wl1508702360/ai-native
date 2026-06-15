import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from streamlit import chat_input, chat_message, empty

from open_api import OpenApi
from util_func import format_time,load_sessions,load_session,del_session,save_session

# 配置参数值
model = os.getenv("ALI_MODEL")
base_url = os.getenv("ALI_BASE_URL")
api_key = os.getenv("DASHSCOPE_API_KEY")

# 设置页面基本信息+右侧栏
st.title("AI的智能伴侣")
st.divider()
st.logo("resources/logo.png")
st.set_page_config(
    page_title="AI的智能伴侣",
    page_icon="🤖",

    # 布局页面
    layout="wide",

    # 控制的是侧边栏的状态
    initial_sidebar_state="expanded",
    menu_items={}
)

nick_name = "小美"
character = "性格活泼的东北人啊"

# 初始化信息
if "message" not in st.session_state:
    st.session_state.message = []

if "nick_name" not in st.session_state:
    st.session_state.nick_name = nick_name

if "character" not in st.session_state:
    st.session_state.character = character

if "current_session" not in st.session_state:
    st.session_state.current_session = format_time()

for msg in st.session_state.message:
    chat_message(msg["role"]).write(msg["content"])

# 设置页面的左侧栏
with st.sidebar:
    # 伴侣信息
    st.subheader("伴侣信息")
    nick_name = st.text_input("昵称", placeholder="请输入伴侣昵称", value=st.session_state.nick_name)
    character = st.text_input("性格", placeholder="请输入伴侣性格", value=st.session_state.character)

    if nick_name:
        st.session_state.nick_name = nick_name

    if character:
        st.session_state.character = character


    # 分割线
    st.divider()
    st.subheader("AI控制面板")
    if st.button("新建会话", width="stretch", icon="🤔"):
        # 保存会话
        data = {
            "nick_name": st.session_state.nick_name,
            "character": st.session_state.character,
            "current_session": st.session_state.current_session,
            "message": st.session_state.message,
        }
        # print("*"*40)
        # print(data)
        # print("*"*40)
        save_session(data)

        # 新建会话后，当会话有内容时我再保存会话
        if st.session_state.message:
            st.session_state.message = []
            st.session_state.current_session = format_time()
            data = {
                "nick_name": st.session_state.nick_name,
                "character": st.session_state.character,
                "current_session": st.session_state.current_session,
                "message": st.session_state.message
            }
            save_session(data)
            st.rerun()


    st.text("历史会话")
    # 加载所有的会话信息
    session_list = load_sessions()
    for session in session_list:
        col1, col2 = st.columns([4,1])
        with col1:
            if st.button(f"{session}", width="stretch", type="primary" if session == st.session_state else "secondary", key=f"load-{session}", icon="✅"):
                session_data = load_session(session)
                # print("*"*40)
                # print(session_data)
                # print("*"*40)
                st.session_state.current_session = session_data["current_session"]
                st.session_state.message = session_data["message"]
                st.session_state.nick_name = session_data["nick_name"]
                st.session_state.character = session_data["character"]
                st.rerun()
        with col2:
            if st.button("", key=f"del-{session}", icon="❌"):
                del_session(session)
                st.session_state.current_session = format_time()
                st.session_state.message = []
                st.session_state.nick_name = nick_name
                st.session_state.character = character
                st.rerun()


# 调用大模型 实现相关逻辑
prompt = chat_input()
sys_prompt = f"""
    你叫{nick_name}，现在是用户的真实伴侣，请完全代入伴侣角色。规则:
    1.每次只回1条消息
    2.禁止任何场景或状态描述性文字
    3.匹配用户的语言
    4.回复简短，像微信聊天一样
    5.有需要的话可以用等emoji表情
    6.用符合伴侣性格的方式对话
    7.回复的内容，要充分体现伴侣的性格特征伴侣性格:
    -{character}。
"""
if prompt:
    chat_message("user").write(prompt)
    # print("*"*30, prompt, "*"*30)

    # 将会话加入到缓存中 使会话可以以追加的形式添加到页面中展示
    st.session_state.message.append({"role": "user", "content": prompt})

    # 调用大模型
    messages = [
        {"role": "system", "content": sys_prompt},
        *st.session_state.message
    ]
    res = OpenApi(model, api_key, base_url).get_result(messages)

    # 处理流式输出
    full_res = ""
    res_message = empty()
    for chunk in res:
        if not chunk.choices or len(chunk.choices) == 0:
            continue

        # print(chunk.model_dump_json(indent=4)) # 打印流式输出的结果
        content = chunk.choices[0].delta.content if chunk.choices[0].delta.content else None
        if content is not None:
            full_res += content
            res_message.chat_message("assistant").write(full_res)

    # st.chat_message("assistant").write_stream(res)
    st.session_state.message.append({"role": "assistant", "content": full_res})
    data = {
        "nick_name": st.session_state.nick_name,
        "character": st.session_state.character,
        "current_session": st.session_state.current_session,
        "message": st.session_state.message
    }
    save_session(data)














