#Copyright (c) 2025 Zyzsdy
from datetime import datetime
import os,sys,shutil,time
##################################hanshu#####################################
def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
def have_files(path):
    # 获取文件夹路径
    current_path = path
    # 获取当前文件夹下所有文件和文件夹
    try:
        files = os.listdir(current_path)
    except FileNotFoundError:
        print("用户名错误,请重新输入")
        input("按Enter退出")
        sys.exit()
    # 筛选出文件夹
    folders = [f for f in files if os.path.isdir(os.path.join(current_path, f))]
    return folders
def read_config(path):
    with open(path,"r",encoding="UTF-8") as file:
        str_file = file.read()
        while True:
            if "true" in str_file:
                str_file = str_file.replace("true","True")
            elif "false" in str_file:
                str_file = str_file.replace("false","False")
            elif "null" in str_file:
                str_file = str_file.replace("null","None")
            else:
                break
        dict = eval(str_file)
        return dict["GUID"]
def copy_folder(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copy_folder(s, d)
        else:
            shutil.copy2(s, d)
def create_directory(directory_path):
    try:
        os.makedirs(directory_path, exist_ok=True)
    except OSError as e:
        print(f"[waring]创建目录时发生错误: {e}")
######################################################################################################################
# 添加命令行参数处理
if len(sys.argv) > 1:
    route = sys.argv[1]  # 使用命令行传入的路径
    print(f"使用命令行指定的路径: {route}")
else:
    route = "C:\\Users\\Administrator\\Desktop\\PCL2\\Server-for-fabric\\world"  # 默认路径
    print(f"使用默认路径: {route}")

# 检查源路径是否存在
if not os.path.exists(route):
    print(f"错误：源文件夹 '{route}' 不存在")
    input("按Enter退出")
    sys.exit(1)

save_path = "C:\\Users\\Administrator\\Desktop\\MCdownload\\%s\\%s"%(timestamp_to_datetime(time.time())[:10],time.time())
create_directory("%s\\Java"%(save_path))
copy_folder(route,save_path)