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
