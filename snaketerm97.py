#!/usr/bin/env python3

import curses
import menuchoice
import os
from src._snakeCurses import *
from src._scoreHandler import *
from src._configHandler import *

if not os.path.exists(gameConfigFileName):
    createHighScoreFile()

gameOptions = ["New game", "Top score", "Quit"]

def play():
    score = curses.wrapper(startGame)
    topscore = getTopScore()
    menuchoice.MenuSelector(["OK"], getGameOverText(score, score >= topscore)).highlight_select(center=False)

def displayMainMenu():
    playerOption = menuchoice.MenuSelector(gameOptions, "Snake").highlight_select(center=True)[0]
    return playerOption

while True:
    playerOption = displayMainMenu()
    match playerOption[0]:
        case 0:
            play()
        case 1:
            displayTopScore()
        case 2:
            raise SystemExit(0)
