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
