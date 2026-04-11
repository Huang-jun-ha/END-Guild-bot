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
            ["pkill", "-f", "MCC-Windows-x64.exe"],
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )
    os.execv(sys.executable, [sys.executable] + sys.argv)

def monitor_process_output():
    global _process, _running
    _process = subprocess.Popen(
        ["./MCC-Windows-x64.exe"],   # 启动指令
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
        if output_line:
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
