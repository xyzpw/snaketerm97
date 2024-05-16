__all__ = [
    "playAudio",
]

from playsound import playsound
import multiprocessing

def playAudio(name: str):
    if name not in ["food", "gameover", "highscore"]:
        raise FileNotFoundError("no audio with the name '%s' exists" % name)
    multiprocessing.Process(target=playsound, args=[f"audio/{name}.wav"]).start()
