from gtts import gTTS
from pathlib import Path

AUDIO_DIR = Path("audio")
AUDIO_DIR.mkdir(exist_ok=True)

async def get_audio(filename: str, word: str):
    path = AUDIO_DIR / filename
    if path.exists():
        return path
    gTTS(word, lang="en").save(path)
    return path
