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
