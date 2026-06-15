import json
import os.path
from datetime import datetime
from file_path import get_abs_path

"""
    将会话存入到内存的文件中 
    读取、删除等操作
    可尝试通过redis保存
"""

def format_time():
    return datetime.now().strftime("%Y%m%d %H:%M:%S")

# 保存会话
def save_session(data):
    # print(f"save_session 接收到的数据类型: {type(data)}")
    # print(f"save_session 接收到的数据内容: {data}")
    if not isinstance(data, dict):
        raise TypeError(f"期望传入 dict 类型，但收到 {type(data).__name__} 类型")

    current_session = data.get("current_session")
    if current_session is None:
        raise ValueError("data 中缺少 'current_session' 键")

    session_data = {
        "nick_name": data.get("nick_name"),
        "character": data.get("character"),
        "current_session": current_session,
        "message": data.get("message", [])
    }

    os.makedirs("sessions", exist_ok=True)

    with open(get_abs_path(f"sessions/{current_session}.json"), "w", encoding="utf-8") as f:
        # json.dump(session_data, f, ensure_ascii=False, indent=4)
        json.dump(session_data, f, ensure_ascii=False, indent=4)


# 加载会话列表
def load_sessions():
    data_list = []
    if os.path.exists("sessions"):
        file_list = os.listdir("sessions")
        for file in file_list:
            if file.endswith(".json"):
                data_list.append(file[:-5])
    data_list.sort(reverse=True)
    return data_list


# 加载会话详情
def load_session(session_name):
    try:
        session_data = []
        session_path = get_abs_path(f"sessions/{session_name}.json")
        if os.path.exists(session_path):
            with open(session_path, "r", encoding="utf-8") as f:
                session_data = json.load(f)
        return session_data
    except Exception as e:
        print("加载异常！", str(e))
        return []


# 删除会话
def del_session(session_name):
    try:
        session_path = get_abs_path(f"sessions/{session_name}.json")
        if os.path.exists(session_path):
            os.remove(session_path)
        return True
    except Exception as e:
        print("删除会话失败！", str(e))
        return False


if __name__ == '__main__':
    pass