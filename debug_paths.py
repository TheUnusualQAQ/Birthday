#!/usr/bin/env python3
"""
调试脚本：显示PyInstaller打包后的文件路径
"""

import os
import sys

def show_paths():
    """显示文件路径信息"""
    print("🔍 文件路径调试信息")
    print("=" * 50)
    
    # 当前工作目录
    print(f"当前工作目录: {os.getcwd()}")
    
    # 脚本所在目录
    if hasattr(sys, '_MEIPASS'):
        print(f"PyInstaller临时目录: {sys._MEIPASS}")
        print("📦 这是打包后的运行环境")
        
        # 列出临时目录的文件
        try:
            files = os.listdir(sys._MEIPASS)
            print(f"临时目录中的文件: {files}")
            
            # 检查wallpaper_basic.png
            wallpaper_path = os.path.join(sys._MEIPASS, "wallpaper_basic.png")
            if os.path.exists(wallpaper_path):
                size = os.path.getsize(wallpaper_path)
                print(f"✅ wallpaper_basic.png 存在: {wallpaper_path} ({size} bytes)")
            else:
                print("❌ wallpaper_basic.png 不存在")
                
        except Exception as e:
            print(f"无法读取临时目录: {e}")
    else:
        print("📝 这是开发环境（未打包）")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"脚本目录: {script_dir}")
    
    # 检查当前目录的文件
    print(f"\n当前目录文件:")
    try:
        files = [f for f in os.listdir('.') if f.endswith('.png') or f.endswith('.json')]
        for file in files:
            if os.path.exists(file):
                size = os.path.getsize(file)
                print(f"  {file}: {size} bytes")
    except Exception as e:
        print(f"无法读取当前目录: {e}")

if __name__ == "__main__":
    show_paths() 