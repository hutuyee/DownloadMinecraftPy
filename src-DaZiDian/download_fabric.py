import os
import requests
import hashlib

# 创建目录
if not os.path.exists('versions/Fabric'):
    os.makedirs('versions/Fabric')

# 获取版本信息
print("正在获取游戏版本")
response = requests.get("https://meta.fabricmc.net/v2/versions")
data = response.json()

# 用户输入要下载的版本号
version = input('请输入要下载的版本号: ')

# 检查'game'键是否存在
if 'game' not in data:
    print("没有找到任何游戏版本。响应数据: {data}")

# 是否找到目标版本的标志
found_target_version = False

# 遍历每个游戏版本
for game_version in data['game']:
    game_version_number = game_version['version']
    
    # 如果游戏版本号与用户输入的版本号匹配，则进行下载
    if game_version_number == version:
        found_target_version = True
        print(f"正在处理游戏版本: {game_version_number}")
        
        # 获取每个游戏版本的加载器版本信息
        loader_response = requests.get(f"https://meta.fabricmc.net/v2/versions/loader/{game_version_number}")
        loader_data = loader_response.json()

        # 遍历每个加载器版本
        for loader_version in loader_data:
            loader_version_number = loader_version['loader']['version']
            print(f"正在处理加载器版本: {loader_version_number}")

            # 获取下载信息
            download_url = f"https://meta.fabricmc.net/v2/versions/loader/{game_version_number}/{loader_version_number}/server/jar"
            print(f"正在从以下地址下载: {download_url}")
            file_response = requests.get(download_url)
            file_path = f"versions/fabric/{game_version_number}/{loader_version_number}/server.jar"
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as f:
                f.write(file_response.content)
            print(f"成功下载到: {file_path}")

            # 计算md5
            md5 = hashlib.md5()
            md5.update(file_response.content)
            md5_value = md5.hexdigest()

            # 保存md5到txt文件
            with open(f"{file_path}.md5.txt", 'w') as f:
                f.write(md5_value)
            print(f"MD5值为: {md5_value}")
        break

if not found_target_version:
    print(f"找不到版本号为 {version} 的Fabric版本。")
