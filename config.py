import json
import os
import sys

def get_config():
    # 获取程序所在目录
    if hasattr(sys, '_MEIPASS'):
        # 打包后的程序，获取可执行文件所在目录
        exe_dir = os.path.dirname(sys.executable)
    else:
        # 开发环境，使用当前脚本所在目录
        exe_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 优先读取与程序同目录的config.json
    external_config_path = os.path.join(exe_dir, "config.json")
    
    try:
        # 尝试读取外部配置文件
        with open(external_config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # 外部配置文件不存在或损坏，尝试读取内嵌配置
        if hasattr(sys, '_MEIPASS'):
            internal_config_path = os.path.join(sys._MEIPASS, "config.json")
            try:
                with open(internal_config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                pass
        
        # 如果都失败，使用默认配置
        return {"bpm": 90, "message": "🎉 生日快乐歌播放完成！Happy Birthday! 🎂"}
