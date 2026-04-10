# 此插件为 管理员和白名单管理插件，并且返回权限等级
import os
Send_commands = None
Adminlist = set()
Whitelist = set()

Adminlist_path = "/config/admin/adminlist.json"
Whitelist_path = "/config/admin/whitelist.json"

def update_adminlist():
    with open(Adminlist_path ,"w" , encoding = "utf-8") as f:
            for name in Adminlist :
                f.write(name + "\n")

def update_whitelist():
    with open(Whitelist_path ,"w" , encoding = "utf-8") as f:
            for name in Whitelist :
                f.write(name + "\n")

def get_adminlist():
    if os.path.exists(Adminlist_path):
        print("文件存在，即将初始化 管理员名单")
        with open(Adminlist_path , "r" , encoding = "utf-8") as f:
            for line in f:
                line.strip()
                Adminlist.add(line)
    else :
        print("文件不存在，将创建空管理员缓存")
        with open(Adminlist , "x" , encoding = "utf-8") as f:
            pass
    return

def get_whitelist():
    if os.path.exists(Whitelist_path):
        print("文件存在，即将初始化 管理员名单")
        with open(Whitelist_path , "r" , encoding = "utf-8") as f:
            for line in f:
                line.strip()
                Whitelist.add(line)
    else :
        print("文件不存在，将创建空管理员缓存")
        with open(Whitelist_path , "x" , encoding = "utf-8") as f:
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

def init(func):
    global Send_commands
    Send_commands = func
    get_adminlist()
    get_whitelist()