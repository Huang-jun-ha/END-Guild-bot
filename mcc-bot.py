import os
import sys
import subprocess
import threading
import time
import re
from queue import Queue, Empty
import plugin
qz="~"
_process = None
_running = True
input_queue = Queue()

def match_player_info(output):
    output.strip()
    player_info_pattern = re.compile(r'▌\s*(?:\[([^\]]+)\])?\s*([a-zA-Z0-9_]+)\s*>>\s*(.+)')
    player_info_match = re.match(player_info_pattern , output)
    if not player_info_match :
        return None
    Title = player_info_match.group(1)
    Player_name = player_info_match.group(2)
    Player_msg = player_info_match.group(3)
    msg_list = Player_msg.split()
    return Title , Player_name , msg_list

def send_command(command):
    global _process
    if _process is None:
        raise RuntimeError("进程未启动，请先调用 monitor_process_output()")
    
    try:
        _process.stdin.write(command + "\n")
        time.sleep(1)
        _process.stdin.flush()
        return True
    except Exception as e:
        print(f"发送命令失败: {e}")
        return False

def input_reader():
    while _running:
        try:
            line = input()
            input_queue.put(line)
        except EOFError:
            break
        except Exception as e:
            print(f"读取输入失败: {e}")

def user_input_loop():
    global _running
    while _running:
        try:
            user_input = input_queue.get(timeout=1)
            if user_input.lower() == 'exit':
                _running = False
                if _process:
                    _process.terminate()
                break
            send_command(user_input)
        except Empty:
            continue
        except Exception as e:
            print(f"输入处理错误: {e}")

def restart_program():
    subprocess.run(
            ["pkill", "-f", "Linux-mcc"],
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )
    os.execv(sys.executable, [sys.executable] + sys.argv)

def monitor_process_output():
    global _process, _running
    _process = subprocess.Popen(
        ["./Linux-mcc"],   # 启动指令
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        bufsize=1,
        universal_newlines=True,
        shell=False,
        encoding="utf-8",
        errors="ignore"
    )

    threading.Thread(target=input_reader, daemon=True).start()
    threading.Thread(target=user_input_loop, daemon=True).start()
    print("欢迎使用末影bot喵")
    while _running:
        output_line = _process.stdout.readline()
        if output_line == "" and _process.poll() is not None:
            continue
        print(output_line, end="")

        if output_line: #监听输出，判断指令部分
            Player_info = match_player_info(output_line)
            if Player_info :
                Title , Player_name , Player_msg = Player_info
                msg_size = len(Player_msg)

                if msg_size < 1 :
                    continue

                First_msg = Player_msg[0]
                if First_msg[0] != qz:
                    continue
                First_msg = First_msg[1:]
                op_level = plugin.admin.query_player_level(Player_name)
                if op_level >= 1 and First_msg == "查等级" and msg_size > 1:
                    i = 1
                    while i < msg_size :
                        if Player_msg[i][0] == '@':
                            Player_msg[i] = Player_msg[i][1:]
                        print(f"正在查询玩家 {Player_msg[i]}")
                        send_command(f"玩家 {Player_msg[i]} 等级为：{plugin.admin.query_player_level(Player_msg[i])}")
                        print(f"查询玩家 {Player_msg[i]} 完毕")
                        time.sleep(1)
                        i = i + 1
                    continue
                if op_level >= 2 and First_msg == "加管" and msg_size > 1:
                    i=1
                    while i < msg_size :
                        if Player_msg[i][0] == '@':
                            Player_msg[i] = Player_msg[i][1:]
                        print(f"正在添加玩家为管理员 {Player_msg[i]}")
                        Flag = plugin.admin.add_player_admin({Player_msg[i]})
                        if Flag:
                            send_command(f"已成功添加管理员 {Player_msg[i]}")
                        else :
                            send_command(f"玩家 {Player_msg[i]} 已经是管理员")
                        print(f"玩家 {Player_msg[i]} 加管流程结束")
                        time.sleep(1)
                        i = i + 1
                    continue
                    
                if op_level >= 2 and First_msg == "加白" and msg_size > 1:
                    i=1
                    while i < msg_size :
                        if Player_msg[i][0] == '@':
                            Player_msg[i] = Player_msg[i][1:]
                        print(f"正在添加玩家到白名单 {Player_msg[i]}")
                        Flag = plugin.admin.add_player_whitelist({Player_msg[i]})
                        if Flag:
                            send_command(f"已成功添加白 {Player_msg[i]}")
                        else :
                            send_command(f"玩家 {Player_msg[i]} 已经在白名单内")
                        print(f"玩家 {Player_msg[i]} 加白流程结束")
                        time.sleep(1)
                        i = i + 1
                    continue
                
                if op_level >= 2 and First_msg == "去管" and msg_size > 1:
                    i=1
                    while i < msg_size :
                        if Player_msg[i][0] == '@':
                            Player_msg[i] = Player_msg[i][1:]
                        print(f"正在删除玩家为管理员 {Player_msg[i]}")
                        Flag = plugin.admin.del_player_admin({Player_msg[i]})
                        if Flag:
                            send_command(f"已成功删除管理员 {Player_msg[i]}")
                        else :
                            send_command(f"玩家 {Player_msg[i]} 不是管理员")
                        print(f"玩家 {Player_msg[i]} 去管流程结束")
                        time.sleep(1)
                        i = i + 1
                    continue
                    
                if op_level >= 2 and First_msg == "去白" and msg_size > 1:
                    i=1
                    while i < msg_size :
                        if Player_msg[i][0] == '@':
                            Player_msg[i] = Player_msg[i][1:]
                        print(f"正在删除玩家在白名单 {Player_msg[i]}")
                        Flag = plugin.admin.del_player_whitelist({Player_msg[i]})
                        if Flag:
                            send_command(f"已成功去白 {Player_msg[i]}")
                        else :
                            send_command(f"玩家 {Player_msg[i]} 不在白名单内")
                        print(f"玩家 {Player_msg[i]} 去白流程结束")
                        time.sleep(1)
                        i = i + 1
                    continue
            continue 
    
    _running = False
    return_code = _process.poll()
    if return_code != 0:
        print(f"进程异常退出，返回码: {return_code}")
        error_output = _process.stderr.read()
        if error_output:
            print(f"错误信息: {error_output}")

if __name__ == "__main__":
    plugin.admin.init()
    monitor_process_output()
