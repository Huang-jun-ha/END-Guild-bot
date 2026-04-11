# 此插件为 管理员和白名单管理插件，并且返回权限等级
import os
Adminlist = set()
Whitelist = set()

Adminlist_path = "./plugin_config/admin/adminlist.txt"
Whitelist_path = "./plugin_config/admin/whitelist.txt"

def update_adminlist():
    with open(Adminlist_path ,"w" , encoding = "utf-8") as f:
            for name in Adminlist :
                f.write(name + "\n")

def update_whitelist():
    with open(Whitelist_path ,"w" , encoding = "utf-8") as f:
            for name in Whitelist :
                f.write(name + "\n")

def get_adminlist():
    os.makedirs(os.path.dirname(Adminlist_path), exist_ok=True)
    if os.path.exists(Adminlist_path):
        print("文件存在，即将初始化 管理员名单")
        with open(Adminlist_path , "r" , encoding = "utf-8") as f:
            for line in f:
                new_line = line.strip()
                Adminlist.add(new_line)
    else :
        print("文件不存在，将创建空管理员缓存")
        with open(Adminlist_path , "w" , encoding = "utf-8") as f:
            pass
    return

def get_whitelist():
    os.makedirs(os.path.dirname(Whitelist_path), exist_ok=True)
    if os.path.exists(Whitelist_path):
        print("文件存在，即将初始化 白名单")
        with open(Whitelist_path , "r" , encoding = "utf-8") as f:
            for line in f:
                new_line = line.strip()
                Whitelist.add(new_line)
    else :
        print("文件不存在，将创建空白名单缓存")
        with open(Whitelist_path , "w" , encoding = "utf-8") as f:
            pass
    return

def query_player_level(Player):
    if Player in Adminlist:
        return 2
    
    elif Player in Whitelist:
        return 1
    
    else :
        return 0

def add_player_admin(player):
    if player in Adminlist:
        return 0
    
    else :
        Adminlist.add(player)
        update_adminlist()
        return 1

def add_player_whitelist(player):
    if player in Whitelist:
        return 0
    
    else :
        Whitelist.add(player)
        update_whitelist()
        return 1
    
def del_player_admin(player):
    if player not in Adminlist :
        return 0
    
    else :
        Adminlist.remove(player)
        update_adminlist()

def del_player_whitelist(player):
    if player not in Whitelist :
        return 0
    
    else :
        Whitelist.remove(player)
        update_whitelist()

def init():
    get_adminlist()
    get_whitelist()
    for f in Adminlist :
        print(f)