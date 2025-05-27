#!/usr/bin/env python3
"""
支持打包为 Windows (.exe) 和 macOS (.app) 版本
"""

import os
import sys
import platform
import subprocess
import shutil

def install_pyinstaller():
    """安装PyInstaller"""
    try:
        import PyInstaller
        return True
    except ImportError:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

def get_pyinstaller_args():
    """获取PyInstaller打包参数"""
    system = platform.system()
    
    # 基础参数
    args = [
        "pyinstaller",
        "--onefile",          # 打包成单文件
        "--windowed",         # 隐藏控制台窗口
        "--clean",            # 清理临时文件
        "--noconfirm",        # 不询问覆盖
    ]
    
    # 添加数据文件
    if os.path.exists("config.json"):
        args.extend(["--add-data", f"config.json{os.pathsep}."])
    
    if os.path.exists("wallpaper_basic.png"):
        args.extend(["--add-data", f"wallpaper_basic.png{os.pathsep}."])
    
    # 系统特定设置
    if system == "Darwin":  # macOS
        args.extend([
            "--icon=icon.icns" if os.path.exists("icon.icns") else "",
            "--name=BirthdayPlayer"
        ])
    elif system == "Windows":
        args.extend([
            "--icon=icon.ico" if os.path.exists("icon.ico") else "",
            "--name=BirthdayPlayer"
        ])
    
    # 过滤空字符串
    args = [arg for arg in args if arg]
    
    # 添加主文件
    args.append("main.py")
    
    return args

def create_spec_file():
    """创建自定义的spec文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.json', '.'),
        ('wallpaper_basic.png', '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BirthdayPlayer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# macOS app bundle
app = BUNDLE(
    exe,
    name='BirthdayPlayer.app',
    icon='icon.icns' if os.path.exists('icon.icns') else None,
    bundle_identifier='com.birthday.player',
)
'''
    
    with open("BirthdayPlayer.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)

def pack_application():
    """打包应用程序"""
    system = platform.system()
    
    # 检查必要文件
    if not os.path.exists("main.py"):
        return False
    
    # 安装PyInstaller
    if not install_pyinstaller():
        return False
    
    # 清理之前的构建
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    try:
        if system == "Darwin":  # macOS
            # 创建spec文件用于macOS app bundle
            create_spec_file()
            cmd = ["pyinstaller", "BirthdayPlayer.spec"]
        else:
            # 直接使用命令行参数
            cmd = get_pyinstaller_args()
        
        # 执行打包
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        # 检查输出文件
        if system == "Darwin":
            if os.path.exists("dist/BirthdayPlayer.app"):
                return True
        elif system == "Windows":
            if os.path.exists("dist/BirthdayPlayer.exe"):
                return True
        else:  # Linux
            if os.path.exists("dist/BirthdayPlayer"):
                return True
        
        return False
        
    except subprocess.CalledProcessError as e:
        return False

def create_basic_info():
    """创建基础信息文件"""
    system = platform.system()
    
    if system == "Darwin":
        info = "🎂 Birthday Player - macOS版本"
    elif system == "Windows":
        info = "🎂 Birthday Player - Windows版本"
    else:
        info = "🎂 Birthday Player - Linux版本"
    
    with open("dist/README.txt", "w", encoding="utf-8") as f:
        f.write(info)

def main():
    """主函数"""
    if pack_application():
        # 创建基础信息
        create_basic_info()
        
        # 复制配置文件到输出目录
        if os.path.exists("config.json"):
            shutil.copy2("config.json", "dist/")
        
        # 清理临时文件
        if os.path.exists("BirthdayPlayer.spec"):
            os.remove("BirthdayPlayer.spec")
        if os.path.exists("build"):
            shutil.rmtree("build")
        
        return True
    else:
        return False

if __name__ == "__main__":
    success = main()
    if success:
        sys.exit(0)
    else:
        sys.exit(1) 