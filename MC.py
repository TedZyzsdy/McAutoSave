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
#################################INIT#########################################
username_files = "C:\\MCLDownload\\Game"
usernames_file = have_files(username_files)
usernames = []
for user_name in usernames_file:
    if user_name == ".minecraft":
        continue
    usernames.append(user_name)
    if len(usernames) == 1:
        username = usernames[0]
    else:
        username = input("请输入MC用户名 >>>")
MC_map_config_path1 = "C:\\MCLDownload\\Game\\%s\\NetGame"%username
MC_map_config_path2 = "C:\\MCLDownload\\Game\\%s\\MCGame"%username
MC_map_files_path = "C:\\MCLDownload\\Game\\.minecraft\\saves"
save_path = "C:\\Users\\Administrator\\Desktop\\MCdownload\\%s"%(timestamp_to_datetime(time.time())[:10])
dioushi = 0
all = 0
###############################read .config file##############################
files_config_file1 = have_files(MC_map_config_path1)
for file in files_config_file1:
    all += 1
    print("正在保存 %s ... "%file,end='')
    #print("正在读取 %s\\%s\\%s.config"%(MC_map_config_path1,file,file))
    GUID = read_config("%s\\%s\\%s.config"%(MC_map_config_path1,file,file))
    #print("GUID为 %s"%GUID)
    #print("正在创建文件夹","%s\\Java\\%s"%(save_path,file))
    create_directory("%s\\Java\\%s"%(save_path,file))
    #print("正在复制文件","%s\\%s"%(MC_map_files_path,GUID),"到","%s\\Java\\%s"%(save_path,file))
    try:
        copy_folder("%s\\%s"%(MC_map_files_path,GUID),"%s\\Java\\%s"%(save_path,file))
        #print("正在创建补充文件夹","%s\\Java\\%s\\netease_config"%(save_path,file))
        create_directory("%s\\Java\\%s\\netease_config"%(save_path,file))
        #print("正在补充文件","%s\\%s"%(MC_map_config_path1,file))
        copy_folder("%s\\%s"%(MC_map_config_path1,file),"%s\\Java\\%s\\netease_config"%(save_path,file))
        print("完成")
    except:
        try:
            os.rmdir("%s\\Java\\%s"%(save_path,file))
            print("文件丢失")
            dioushi += 1
        except:
            pass
    finally:
        pass
        #time.sleep(0.05) #防止cpu占用过高导致卡顿

files_config_file2 = have_files(MC_map_config_path2)
for file in files_config_file2:
    all += 1
    print("正在保存 %s ... "%file,end='')
    #print("正在读取 %s\\%s\\%s.config"%(MC_map_config_path2,file,file))
    GUID = read_config("%s\\%s\\%s.config"%(MC_map_config_path2,file,file))
    #print("GUID为 %s"%GUID)
    #print("正在创建文件夹","%s\\RedRock\\%s"%(save_path,file))
    create_directory("%s\\RedRock\\%s"%(save_path,file))
    #print("正在复制文件","%s\\%s"%(MC_map_files_path,GUID),"到","%s\\RedRock\\%s"%(save_path,file))
    try:
        copy_folder("%s\\%s"%(MC_map_files_path,GUID),"%s\\RedRock\\%s"%(save_path,file))
        create_directory("%s\\RedRock\\%s\\netease_config"%(save_path,file))
        #print("正在补充文件","%s\\%s"%(MC_map_config_path2,file))
        copy_folder("%s\\%s"%(MC_map_config_path2,file),"%s\\RedRock\\%s\\netease_config"%(save_path,file))
        print("完成")
    except:
        try:
            os.rmdir("%s\\RedRock\\%s"%(save_path,file))
            print("文件丢失")
            dioushi += 1
        except:
            pass
    finally:
        pass
        #time.sleep(0.05) #防止cpu占用过高导致卡顿
print("\n用户 %s 文件保存数据:"%username)
print("总数: [%s] ,完成个数: [%s] ,丢失个数: [%s]"%(str(all),str(all - dioushi),str(dioushi)))
input()