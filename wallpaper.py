import os
import sys
import subprocess
import platform
import time
import uuid
from PIL import Image, ImageDraw, ImageFont

def get_system_fonts():
    """获取系统中可用的字体路径（楷体相关）"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        font_paths = [
            "/System/Library/Fonts/PingFang.ttc",   # 苹方
            "/Library/Fonts/Kaiti.ttc",            # 楷体 (可能的位置)
            "/System/Library/Fonts/Supplemental/Kaiti.ttc",  # 楷体补充字体
            "/System/Library/Fonts/Helvetica.ttc", # 备选西文字体
        ]
    elif system == "Windows":
        font_paths = [
            "C:/Windows/Fonts/simkai.ttf",         # 楷体
            "C:/Windows/Fonts/SIMKAI.TTF",         # 楷体 (大写)
            "C:/Windows/Fonts/kaiti.ttf",          # 楷体
            "C:/Windows/Fonts/simsun.ttc",         # 宋体备选
            "C:/Windows/Fonts/msyh.ttc",           # 微软雅黑备选
        ]
    else:  # Linux等其他系统
        font_paths = [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    
    return font_paths

def create_wallpaper(message: str, output_path: str = None):
    # 生成唯一的文件名避免冲突
    if output_path is None:
        timestamp = int(time.time())
        unique_id = str(uuid.uuid4())[:8]
        output_path = f"birthday_wallpaper_{timestamp}_{unique_id}.png"
    
    # 尝试加载底图
    base_image_path = "wallpaper_basic.png"
    
    # PyInstaller打包后的路径处理
    if hasattr(sys, '_MEIPASS'):
        # 打包后的临时目录
        base_image_path = os.path.join(sys._MEIPASS, "wallpaper_basic.png")
    
    try:
        if os.path.exists(base_image_path):
            # 加载底图
            image = Image.open(base_image_path)
        else:
            # 如果底图不存在，创建黑色背景
            width, height = 2560, 1600  # MacBook Pro 常见分辨率
            image = Image.new("RGB", (width, height), color="black")
    except Exception as e:
        # 如果加载失败，创建黑色背景
        width, height = 2560, 1600
        image = Image.new("RGB", (width, height), color="black")
    
    width, height = image.size
    draw = ImageDraw.Draw(image)
    
    font_size = 80
    font = None
    
    try:
        font_paths = get_system_fonts()
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    font = ImageFont.truetype(font_path, font_size)
                    break
                except Exception as e:
                    continue
        
        if font is None:
            font = ImageFont.load_default()
            
    except Exception as e:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), message, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    shadow_offset = 3
    draw.text((x + shadow_offset, y + shadow_offset), message, fill="black", font=font)
    draw.text((x, y), message, fill="white", font=font)
    
    # 保存图像
    image.save(output_path)
    return output_path

def set_wallpaper_macos(image_path: str):
    try:
        abs_path = os.path.abspath(image_path)
        
        if not os.path.exists(abs_path):
            return False
        
        script = f'''
        tell application "System Events"
            tell every desktop
                set picture to "{abs_path}"
            end tell
        end tell
        '''
        
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            verify_script = '''
            tell application "System Events"
                tell desktop 1
                    get picture
                end tell
            end tell
            '''
            
            verify_result = subprocess.run(
                ["osascript", "-e", verify_script],
                capture_output=True,
                text=True
            )
            
            if verify_result.returncode == 0:
                current_wallpaper = verify_result.stdout.strip()
                if abs_path in current_wallpaper or current_wallpaper.endswith(os.path.basename(abs_path)):
                    return True
                else:
                    return False
            else:
                return True  # 假设设置成功，因为原始命令成功
        else:

            return False
            
    except Exception as e:

        return False

def set_wallpaper_windows(image_path: str):
    """设置桌面壁纸 (Windows)"""
    try:
        import ctypes
        abs_path = os.path.abspath(image_path)
        
        # 使用Windows API设置壁纸
        ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 0)
        return True
    except Exception as e:

        return False

def set_wallpaper_linux(image_path: str):
    """未测试"""
    try:
        abs_path = os.path.abspath(image_path)
        
        commands = [
            ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", f"file://{abs_path}"],  # GNOME
            ["feh", "--bg-scale", abs_path],  
            ["nitrogen", "--set-scaled", abs_path]  
        ]
        
        for cmd in commands:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    return True
            except FileNotFoundError:
                continue
        
        return False
    except Exception as e:

        return False

def set_wallpaper(image_path: str, delete_after: bool = True):
    if not os.path.exists(image_path):

        return False
    
    system = platform.system()
    success = False
    
    try:
        if system == "Darwin":  # macOS
            success = set_wallpaper_macos(image_path)
        elif system == "Windows":
            success = set_wallpaper_windows(image_path)
        elif system == "Linux":
            success = set_wallpaper_linux(image_path)
        else:

            return False
        
        if success:

            
            # 设置成功后删除临时文件
            if delete_after:
                # 对于macOS，稍等一下再删除，确保系统完成壁纸设置
                if system == "Darwin":
                    time.sleep(1)  # 等待1秒
                
                try:
                    os.remove(image_path)
                except Exception as e:
                    pass
        else:
            pass
            if delete_after:
                try:
                    os.remove(image_path)
                except Exception as e:
                    pass
        
        return success
        
    except Exception as e:
        return False

def cleanup_old_wallpapers():
    """清理旧的壁纸文件"""
    try:
        current_dir = os.getcwd()
        for filename in os.listdir(current_dir):
            if filename.startswith("birthday_wallpaper_") and filename.endswith(".png"):
                file_path = os.path.join(current_dir, filename)
                if os.path.getctime(file_path) < time.time() - 3600:
                    try:
                        os.remove(file_path)
                    except:
                        pass
    except Exception as e:
        pass  

def create_and_set_wallpaper(message: str):
    cleanup_old_wallpapers()
    
    wallpaper_path = create_wallpaper(message)
    
    if os.path.exists(wallpaper_path):
        success = set_wallpaper(wallpaper_path, delete_after=True)
        if not success:
            try:
                os.remove(wallpaper_path)
            except:
                pass
        return success
    else:
        return False 