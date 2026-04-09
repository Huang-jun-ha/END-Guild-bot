import subprocess
import sys
import os
from threading import Thread
import plugin

Flag = True

def read_stream(stream, prefix):
    try:
        for line in iter(stream.readline, b''):
            try:
                line = line.decode('utf-8').rstrip('\n\r')
            except UnicodeDecodeError:
                line = line.decode('gbk').rstrip('\n\r')
            print(f"[{prefix}] {line}\n")
    finally:
        stream.close()

def send_input(proc):
    global Flag
    while True and Flag:
        try:
            user_input = input()
            send_command(proc, user_input)
        except EOFError:
            break
        except Exception as e:
            print(f"[发送错误] {e}")
            break

def send_command(proc, user_input):
    global Flag
    if user_input == "Mcc-bot-exit":
        print("[*] 正在停止程序...")
        proc.terminate()
        Flag = False
        return
    if user_input == "Test hello":
        plugin.test1.send_hello()
        return
    proc.stdin.write((user_input + '\n').encode('utf-8'))
    proc.stdin.flush()

def monitor_command(command):
    global Flag
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        shell=True,
        bufsize=0,
        close_fds=sys.platform != "win32"
    )

    # 核心修复：用lambda把proc和send_command绑定，插件只需要传指令
    plugin.test1.set_func(lambda cmd: send_command(proc, cmd))

    Thread(target=read_stream, args=(proc.stdout, "OUT"), daemon=True).start()
    Thread(target=read_stream, args=(proc.stderr, "ERR"), daemon=True).start()

    send_input(proc)
    proc.wait()

    print(f"\n=== 程序已退出 ===")
    print("将重新启动，停止请输入：Mcc-bot-exit")

if __name__ == "__main__":
    MONITOR_CMD = "MCC-Windows-x64.exe"
    Path_Mcc = "MCC-Windows-x64.exe"

    if not os.path.exists(Path_Mcc):
        print("该文件不存在，停止运行")
        exit()

    print("="*50)
    print("程序启动成功！可直接输入指令发送给程序")
    print("输入 Mcc-bot-exit 并回车 可停止程序")
    print("="*50)

    while Flag:
        print("\n已重新启动程序")
        monitor_command(MONITOR_CMD)