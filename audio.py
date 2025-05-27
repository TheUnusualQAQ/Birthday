import numpy as np
import sys

# 尝试导入音频库，优先使用sounddevice
try:
    import sounddevice as sd
    AUDIO_METHOD = "sounddevice"
except ImportError:
    try:
        import simpleaudio as sa
        AUDIO_METHOD = "simpleaudio"
    except ImportError:
        pass
        sys.exit(1)

SAMPLE_RATE = 44_100
VOLUME = 0.2

NOTE_FREQ = {
    "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23,
    "G4": 392.00, "A4": 440.00, "B4": 493.88, "Bb4": 466.16,
    "C5": 523.25, "D5": 587.33, "E5": 659.25, "F5": 698.46, "G5": 783.99
}

MELODY = [
    ("G4", 0.75), ("G4", 0.25), ("A4", 1), ("G4", 1), ("C5", 1), ("B4", 2),
    ("G4", 0.75), ("G4", 0.25), ("A4", 1), ("G4", 1), ("D5", 1), ("C5", 2),
    ("G4", 0.75), ("G4", 0.25), ("G5", 1), ("E5", 1), ("C5", 1), ("B4", 1), ("A4", 1),
    ("F5", 0.75), ("F5", 0.25), ("E5", 1), ("C5", 1), ("D5", 1), ("C5", 2)
]

def synth_note(freq: float, duration: float) -> np.ndarray:
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    tone = np.sin(2 * np.pi * freq * t)
    envelope = np.linspace(1, 0.2, tone.size)  # 简单衰减
    return (tone * envelope * VOLUME).astype(np.float32)

def play_audio(song: np.ndarray):
    try:
        if AUDIO_METHOD == "sounddevice":
            sd.play(song, SAMPLE_RATE)
            sd.wait()
        else:
            audio = np.int16(song * 32767)
            play_obj = sa.play_buffer(audio, 1, 2, SAMPLE_RATE)
            play_obj.wait_done()
        return True
    except Exception as e:
        pass
        return False

def generate_song(bpm: int) -> np.ndarray:
    beat = 60 / bpm
    
    song = np.concatenate([
        synth_note(NOTE_FREQ[note], beat * beats)
        if note != "REST" else np.zeros(int(SAMPLE_RATE * beat * beats))
        for note, beats in MELODY
    ])
    
    return song 