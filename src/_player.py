import shutil
import random
from src._audioPlayer import *
from src._scoreHandler import *
from src._configHandler import gameConfigFileName
import json
import os

__all__ = [
    "SCREEN_SIZE",
    "Snake",
    "Food",
]

SCREEN_SIZE = (shutil.get_terminal_size().columns, shutil.get_terminal_size().lines)

highscore = getTopScore() if os.path.exists(gameConfigFileName) else 0

class Food:
    def __init__(self, border_range: tuple):
        self.border_range = border_range
        self.allLocations = []
        for xOffset in range(border_range["x"][0]+1, border_range["x"][1]-1):
            for yOffset in range(border_range["y"][0]+1, border_range["y"][1]-1):
                self.allLocations.append((xOffset, yOffset))
        self.position = random.randint(self.border_range["x"][0]+1, self.border_range["x"][1]-1), random.randint(self.border_range["y"][0]+1, self.border_range["y"][1]-1)
        self.active = True
        self.char = "\u271c"
    def getAvailableLocations(self, snakeBody: list[tuple]):
        return [i for i in self.allLocations if not i in snakeBody]
    def relocate(self, snakeBody: list[tuple]):
        self.position = random.choice(self.getAvailableLocations(snakeBody))
        self.active = True

class Snake:
    def __init__(self):
        self.score = 0
        self.points_per_food = 7
        self.body_char = "\u2588"
        self.direction = "right"
        self.paused = True
        self.collisionStreak = 0
        self.maxCollisionStreak = 2
    def _initBody(self, head_pos: tuple):
        self.body: list[tuple] = [head_pos]
        for i in range(1, 9):
            self.body.append((head_pos[0]-i, head_pos[1]))
    def consumeFood(self, foodEaten: int = 1):
        self.score += self.points_per_food * foodEaten
        playAudio("food")
        tail = self.body[len(self.body)-1]
        self.body.insert(-1, tail)
    def move(self) -> list:
        for i in range(len(self.body)-1, 0, -1):
            self.body[i] = self.body[i-1]
        match self.direction:
            case "up":
                newHeadPos = (self.body[0][0], self.body[0][1]-1)
            case "down":
                newHeadPos = (self.body[0][0], self.body[0][1]+1)
            case "right":
                newHeadPos = (self.body[0][0]+1, self.body[0][1])
            case "left":
                newHeadPos = (self.body[0][0]-1, self.body[0][1])
        self.body[0] = newHeadPos
    def gameOver(self, score: int, useAudio: bool = True):
        if score > highscore:
            gameConfig = readGameConfig()
            gameConfig["topScore"] = score
            with open(gameConfigFileName, "w+") as f:
                f.write(json.dumps(gameConfig, indent=4))
        if useAudio: playAudio("gameover" if score < highscore else "highscore")

