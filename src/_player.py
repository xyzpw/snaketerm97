import shutil
from random import randint
from src._audioPlayer import *
from src._snakeHandler import getPointsPerFood

__all__ = [
    "SCREEN_SIZE",
    "Snake",
    "Food",
]

SCREEN_SIZE = (shutil.get_terminal_size().columns, shutil.get_terminal_size().lines)

with open("highscore.txt", "r") as f:
    highscore = int(f.read().strip())
    del f

class Food:
    def __init__(self):
        self.position = randint(3, SCREEN_SIZE[0]-3), randint(3, SCREEN_SIZE[1]-3)
        self.active = True
        self.char = "*"
    def relocate(self):
        self.position = randint(3, SCREEN_SIZE[0]-3), randint(3, SCREEN_SIZE[1]-3)
        self.active = True

class Snake:
    def __init__(self):
        self.score = 0
        self.points_per_food = getPointsPerFood(SCREEN_SIZE)
        self.body_char = "#"
        self.body: list = [(i, SCREEN_SIZE[1]-i) for i in range(1, 7)]
        self.direction = "right"
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
    def gameOver(self, score: int, audioOn: bool = True):
        if score > highscore:
            with open("highscore.txt", "w") as f:
                f.write(str(self.score))
                del f
        if audioOn: playAudio("gameover" if score <= highscore else "highscore")
