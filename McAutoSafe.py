from datetime import datetime
import os, sys, shutil, time, configparser

##################################hanshu#####################################
def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

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

def load_config():
    config = configparser.ConfigParser()
    if os.path.exists('config.ini'):
        config.read('config.ini')
    else:
        # 创建默认配置
        config['Settings'] = {
            'source_path': 'D:\\thing\\PCL2\\Server-for-fabric\\world',
            'backup_base_path': 'C:\\Users\\Zyzsdy\\Desktop\\MCdownload',
            'server_count': '1',
            'server_tag': 'server1'
        }
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    return config

def save_config(config):
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def reset_server():
    config = load_config()
    source_path = config['Settings']['source_path']
    
    # 删除世界文件夹内容
    if os.path.exists(source_path):
        for item in os.listdir(source_path):
            item_path = os.path.join(source_path, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
        print(f"已清空世界文件夹: {source_path}")
    else:
        print(f"警告: 源路径不存在: {source_path}")
    
    # 更新服务器标签
    server_count = int(config['Settings']['server_count'])
    server_tag = f"server{server_count + 1}"
    config['Settings']['server_count'] = str(server_count + 1)
    config['Settings']['server_tag'] = server_tag
    
    save_config(config)
    print(f"服务器标签已更新为: {server_tag}")

######################################################################################################################
def auto_backup(route=None):
    config = load_config()
    
    # 使用提供的路径或配置中的路径
    if route:
        print(f"使用命令行指定的路径: {route}")
    else:
        route = config['Settings']['source_path']
        print(f"使用配置中的路径: {route}")

    # 检查源路径是否存在
    if not os.path.exists(route):
        print(f"错误：源文件夹 '{route}' 不存在")
        return False

    # 使用配置中的备份路径和服务器标签
    backup_base_path = config['Settings']['backup_base_path']
    server_tag = config['Settings']['server_tag']
    timestamp = timestamp_to_datetime(time.time())[:10]
    
    save_path = f"{backup_base_path}\\{timestamp}_{server_tag}\\{time.time()}"
    create_directory(f"{save_path}\\Java")
    copy_folder(route, save_path)
    print(f"备份已完成,保存路径: {save_path}")
    return True

def setup_backup():
    config = load_config()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("                      McAutoSafe v1.0.2              ")
        print("          作者:Zyzsdy  主页:https://github.com/TedZyzsdy         ")
        print("1.设置备份路径")
        print("2.设置备份保存路径")
        print("3.设置服务器标签")
        print("4.开始备份")
        print("5.重置服务器")
        print("6.退出")
        
        choice = input("请输入你的选择: ")
        
        if choice == "1":
            print(f"当前备份路径: {config['Settings']['source_path']}")
            route = input("请输入要备份的文件夹路径: ")
            if not os.path.exists(route):
                print(f"错误：源文件夹 '{route}' 不存在")
            else:
                config['Settings']['source_path'] = route
                save_config(config)
                print(f"备份路径已设置为: {route}")
            input("按Enter继续")
            
        elif choice == "2":
            print(f"当前备份保存路径: {config['Settings']['backup_base_path']}")
            backup_path = input("请输入备份保存的基础路径: ")
            config['Settings']['backup_base_path'] = backup_path
            save_config(config)
            print(f"备份保存路径已设置为: {backup_path}")
            input("按Enter继续")
            
        elif choice == "3":
            print(f"当前服务器标签: {config['Settings']['server_tag']}")
            print(f"服务器计数: {config['Settings']['server_count']}")
            server_tag = input("请输入新的服务器标签: ")
            config['Settings']['server_tag'] = server_tag
            save_config(config)
            print(f"服务器标签已设置为: {server_tag}")
            input("按Enter继续")
            
        elif choice == "4":
            if auto_backup():
                input("备份完成,按Enter继续")
            else:
                input("备份失败,按Enter继续")
                
        elif choice == "5":
            confirm = input("确认要重置服务器吗？这将删除世界文件夹中的所有内容并更新服务器标签。(y/N): ")
            if confirm.lower() == 'y':
                reset_server()
                input("按Enter继续")
            else:
                print("取消重置操作")
                input("按Enter继续")
                
        elif choice == "6":
            return

def print_usage():
    print("用法:")
    print("  McAutoSafe.py [路径]      # 使用指定路径进行备份")
    print("  McAutoSafe.py -setup     # 进入设置模式")
    print("  McAutoSafe.py -reset     # 重置服务器")
    print("  McAutoSafe.py -help      # 显示帮助信息")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "-setup":
            print("启动备份设置...")
            setup_backup()
        elif sys.argv[1] == "-reset":
            print("重置服务器...")
            reset_server()
        elif sys.argv[1] == "-help" or sys.argv[1] == "-h":
            print_usage()
        elif sys.argv[1] == "-auto":
            print("启动自动备份...")
            auto_backup()
        else:
            # 假设参数是路径
            print("启动自动备份...")
            auto_backup(sys.argv[1])
    else:
        # 没有参数时显示使用说明
        print_usage()
        print("\n没有提供参数,进入设置模式...")
        setup_backup()