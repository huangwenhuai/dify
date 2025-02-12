# coding = utf-8

# pip install docker
import os
import docker

client = docker.from_env()

# 获取当前 Python 脚本所在的文件夹的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 读取文件
def file_get_contents(file_path):
    with open(file_path, "r", encoding = "utf-8") as file:
        return file.read()

# 写入文件
def file_put_contents(file_path, content):
    with open(file_path, "w", encoding = "utf-8") as file:
        file.write(content)

# 获取容器 IP
def get_container_ip(container_name):
    container = client.containers.get(container_name)
    return container.attrs ['NetworkSettings']['Networks'] ['docker_default']['IPAddress']

# 重启容器
def restart_container(container_name):
    container = client.containers.get(container_name)
    container.restart()

def main():
    # 获取 API 和 Web 容器的 IP 地址
    api_container_ip = get_container_ip('docker-api-1')
    web_container_ip = get_container_ip('docker-web-1')

    print(f'api_container_ip: {api_container_ip}')
    print(f'web_container_ip: {web_container_ip}')

    # 拼接模板文件路径和目标文件路径
    template_path = os.path.join(current_dir, 'nginx/conf.d/default.conf.template')
    target_path = os.path.join(current_dir, 'nginx/conf.d/default.conf')
    # 读取模板文件内容并替换 IP 地址
    tpl_contents = file_get_contents(template_path)
    tpl_contents = tpl_contents.replace('http://api', f'http://{api_container_ip}')
    tpl_contents = tpl_contents.replace('http://web', f'http://{web_container_ip}')

    # 将修改后的内容写入目标配置文件
    file_put_contents(target_path, tpl_contents)

    # 重启 Nginx 容器
    restart_container('docker-nginx-1')
    print("Nginx container restarted with updated configuration.")

if __name__ == '__main__':
    main()