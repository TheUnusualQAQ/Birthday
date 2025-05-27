#!/usr/bin/env python3
"""
全平台构建脚本
自动化打包和发布准备
"""

import os
import sys
import platform
import subprocess
import shutil
import zipfile
from datetime import datetime

def create_release_package():
    """创建发布包"""
    if not os.path.exists("dist"):
        return False
    
    system = platform.system()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 创建发布目录
    release_dir = f"release_{timestamp}"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    if system == "Darwin":  # macOS
        # 复制 .app 文件
        if os.path.exists("dist/BirthdayPlayer.app"):
            shutil.copytree("dist/BirthdayPlayer.app", f"{release_dir}/BirthdayPlayer.app")
        
        # 复制配置文件
        if os.path.exists("dist/config.json"):
            shutil.copy2("dist/config.json", release_dir)
        
        # 复制说明文件
        if os.path.exists("dist/README.txt"):
            shutil.copy2("dist/README.txt", release_dir)
        
        # 创建压缩包
        zip_name = f"BirthdayPlayer_macOS_{timestamp}.zip"
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(release_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, release_dir)
                    zipf.write(file_path, arcname)
        
        print(f"macOS版本已打包：{zip_name}")
        
    elif system == "Windows":
        # 复制 .exe 文件
        if os.path.exists("dist/BirthdayPlayer.exe"):
            shutil.copy2("dist/BirthdayPlayer.exe", release_dir)
        
        # 复制配置文件
        if os.path.exists("dist/config.json"):
            shutil.copy2("dist/config.json", release_dir)
        
        # 复制说明文件
        if os.path.exists("dist/README.txt"):
            shutil.copy2("dist/README.txt", release_dir)
        
        # 创建压缩包
        zip_name = f"BirthdayPlayer_Windows_{timestamp}.zip"
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(release_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, release_dir)
                    zipf.write(file_path, arcname)
        
        print(f"Windows版本已打包：{zip_name}")
    
    # 清理临时目录
    shutil.rmtree(release_dir)
    return True

def main():
    """主函数"""
    print("🎂 Birthday Player 构建工具")
    print("=" * 40)
    
    # 运行打包
    print("正在执行打包...")
    result = subprocess.run([sys.executable, "pack.py"], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 打包成功！")
        
        # 创建发布包
        print("正在创建发布包...")
        if create_release_package():
            print("✅ 发布包创建成功！")
        else:
            print("❌ 发布包创建失败")
    else:
        print("❌ 打包失败")
        if result.stderr:
            print(f"错误信息：{result.stderr}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 