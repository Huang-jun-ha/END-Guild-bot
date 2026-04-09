main_send_command = None

def set_func(func):
    global main_send_command
    main_send_command = func

def send_hello():
    global main_send_command
    main_send_command("Hello!This is a test for the bot of plugins.")