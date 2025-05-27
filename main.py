#!/usr/bin/env python3
"""
生日快乐歌播放器
功能：播放生日歌并生成临时壁纸
"""

from config import get_config
from audio import generate_song, play_audio
from wallpaper import create_and_set_wallpaper

def main():
    config = get_config()
    
    try:
        create_and_set_wallpaper(config["message"])
        song = generate_song(config["bpm"])
        play_audio(song)
        
    except Exception as e:
        pass

if __name__ == "__main__":
    main() 