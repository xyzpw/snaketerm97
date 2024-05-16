#!/usr/bin/env python3

import curses
import menuchoice
from src._snakeCurses import *

def play():
    score = curses.wrapper(startGame)
    menuchoice.MenuSelector(["OK"], str(score)).highlight_select(center=True)
    raise SystemExit(0)

def displayHighScores():
    with open("highscore.txt", "r") as f:
        highscore = str(int(f.read().strip()))
    menuchoice.MenuSelector(["OK"], "High Scores", highscore).highlight_select(center=True)
    raise SystemExit(0)

gameOptions = ["New game", "High scores", "Quit"]

playerOption = menuchoice.MenuSelector(gameOptions, "Snake!").highlight_select(center=True)[0]

match playerOption[0]:
    case 0:
        play()
    case 1:
        displayHighScores()
    case 2:
        raise SystemExit(0)
