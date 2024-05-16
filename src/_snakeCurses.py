import curses
from src._player import *
from src._snakeHandler import *

snake = Snake()
food = Food()

UP = [curses.KEY_UP, ord("w"), ord("W")]
DOWN = [curses.KEY_DOWN, ord("s"), ord("S")]
RIGHT = [curses.KEY_RIGHT, ord("d"), ord("D")]
LEFT = [curses.KEY_LEFT, ord("a"), ord("A")]
QUIT = [curses.KEY_BACKSPACE, ord("q"), ord("Q")]

def startGame(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)
    while True:
        stdscr.clear()
        stdscr.refresh()
        stdscr.addstr(0, 0, str(snake.score))
        stdscr.addstr(food.position[1], food.position[0], food.char)
        for seg in snake.body:
            stdscr.addstr(seg[1], seg[0], snake.body_char)
        usrKey = stdscr.getch()
        if usrKey in UP:
            snake.direction = getNewDirection("up", snake.direction)
        elif usrKey in DOWN:
            snake.direction = getNewDirection("down", snake.direction)
        elif usrKey in RIGHT:
            snake.direction = getNewDirection("right", snake.direction)
        elif usrKey in LEFT:
            snake.direction = getNewDirection("left", snake.direction)
        elif usrKey in QUIT:
            snake.gameOver(snake.score, False)
            raise SystemExit(0)
        snake.move()
        if checkWallCollision(snake.body[0], SCREEN_SIZE) or checkTailCollision(snake.body):
            snake.gameOver(snake.score)
            return snake.score
        if checkFoodEaten(snake.body[0], food.position):
            snake.consumeFood(1)
            food.relocate()
