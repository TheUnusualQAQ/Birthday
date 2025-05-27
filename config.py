import json
import os
import sys

def get_config():
    # 获取配置文件路径
    config_path = "config.json"
    
    # PyInstaller打包后的路径处理
    if hasattr(sys, '_MEIPASS'):
        # 打包后的临时目录
        config_path = os.path.join(sys._MEIPASS, "config.json")
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"bpm": 90, "message": "🎉 生日快乐歌播放完成！Happy Birthday! 🎂"}
