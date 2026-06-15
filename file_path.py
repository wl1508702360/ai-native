import os

def get_project_path() -> str:
    # 获取当前文件的绝对路径
    current_file = os.path.abspath(__file__)
    current_path = os.path.dirname(current_file)
    return current_path

def get_abs_path(relative_path: str) -> str:
   """
   绝对路径+相对路径
   :param relative_path:
   :return:
   """
   abs_path = get_project_path()
   return os.path.join(abs_path, relative_path)


if __name__ == '__main__':
    # get_project_path()
    print(get_abs_path("resources/logo.png"))

