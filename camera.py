# -*- coding: utf-8 -*-
#author:小羊1227
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
