import requests
from concurrent.futures import ThreadPoolExecutor
import argparse
import sys

def print_info_and_exit():
    print("""
  ____  ___  ______   ___   _ ____  _____ ____ 
 / ___|/ _ \|  _ \ \ / / | | / ___|| ____/ ___|
| |  _| | | | | | \ V /| | | \___ \|  _|| |    
| |_| | |_| | |_| || | | |_| |___) | |__| |___ 
 \____|\___/|____/ |_|  \___/|____/|_____\____|

AWD内网探测工具 Author By-GODYUSEC
""")
    print("使用方法：示例 python search.py -u 192.168.111.* 或 python search.py -u 192.168.*.1:21087\n注:支持url,请不要带http|https,可更改端口,默认端口为80,脚本会对*部分进行遍历，并输出存活的url")
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

def get_ip(ip):
    url = f"http://{ip}:{port}"
    try:
        resp = requests.get(url, timeout=1)
        if resp.status_code == 200:
            print(f"存活: {url}")
       
    except requests.exceptions.RequestException:
        pass  



with ThreadPoolExecutor(max_workers=100) as executor:
    for part in parts:
        if '*' in part:
            for i in range(1, 255):
                new_parts = parts.copy()
                new_parts[new_parts.index('*')] = str(i)
                ip = '.'.join(new_parts)
                executor.submit(get_ip, ip)
            break  