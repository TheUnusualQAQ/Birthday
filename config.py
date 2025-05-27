import json
import os

def get_config():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:

        return {"bpm": 90, "message": "🎉 生日快乐歌播放完成！Happy Birthday! 🎂"}
