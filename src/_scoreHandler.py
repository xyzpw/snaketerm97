import json
import menuchoice
from src._configHandler import *

__all__ = [
    "getGameOverText",
    "getTopScore",
    "displayTopScore",
    "createHighScoreFile",
    "readGameConfig",
]

def getGameOverText(score: int, record: bool = False):
    return "Game over!\nYour score:\n%d" % score if not record else "Game over!\nTOP SCORE:\n%d" % score

def readGameConfig():
    with open(gameConfigFileName, "r") as f:
        return json.loads(f.read())

def getTopScore():
    gameConfig = readGameConfig()
    return gameConfig["topScore"]

def displayTopScore():
    topscore = getTopScore()
    if topscore != None:
        menuchoice.MenuSelector(["OK"], "Top score:\n%d" % topscore).highlight_select(center=False)

def createHighScoreFile():
    newContent = {"topScore": 0}
    with open(gameConfigFileName, "w") as f:
        f.write(json.dumps(newContent, indent=4))
