import curses
from src._player import *
from src._snakeHandler import *

UP = [curses.KEY_UP, ord("w"), ord("W")]
DOWN = [curses.KEY_DOWN, ord("s"), ord("S")]
RIGHT = [curses.KEY_RIGHT, ord("d"), ord("D")]
LEFT = [curses.KEY_LEFT, ord("a"), ord("A")]
QUIT = [curses.KEY_BACKSPACE, ord("q"), ord("Q")]

def startGame(stdscr):
    BORDER_SIZE = (20, 11) # keep width greater than height
    borderPosition = getBorderPosition(SCREEN_SIZE, BORDER_SIZE)
    boundsRange = {
        "x": (borderPosition["x"][0], borderPosition["x"][1]),
        "y": (borderPosition["y"][0], borderPosition["y"][1]),
    }
    snake = Snake()
    pause = lambda makePaused: setattr(snake, "paused", makePaused)
    # Initializing snake body to fit inside border
    snake._initBody((borderPosition["x"][0]+9, borderPosition["y"][1]-1))
    food = Food(borderPosition)
    curses.use_default_colors()
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(125)
    while True:
        stdscr.refresh()
        stdscr.erase()
        stdscr.addstr(borderPosition["y"][0], borderPosition["x"][0], "\u2501"*BORDER_SIZE[0])
        stdscr.addstr(borderPosition["y"][1], borderPosition["x"][0], "\u2501"*BORDER_SIZE[0])
        for _ in range(borderPosition["y"][0], borderPosition["y"][1]+1):
            stdscr.addstr(_, borderPosition["x"][0], "\u2503")
            stdscr.addstr(_, borderPosition["x"][1], "\u2503")
        stdscr.addstr(borderPosition["y"][0]-1, borderPosition["x"][0], str(snake.score).zfill(4))
        stdscr.addstr(food.position[1], food.position[0], food.char)
        # Draw snake to display
        for seg in snake.body:
            stdscr.addstr(seg[1], seg[0], snake.body_char)
        usrKey = stdscr.getch()
        if usrKey in UP or usrKey in DOWN or usrKey in RIGHT or usrKey in LEFT:
            pause(False)
        if usrKey in UP:
            snake.direction = getNewDirection("up", snake.direction)
        elif usrKey in DOWN:
            snake.direction = getNewDirection("down", snake.direction)
        elif usrKey in RIGHT:
            snake.direction = getNewDirection("right", snake.direction)
        elif usrKey in LEFT:
            snake.direction = getNewDirection("left", snake.direction)
        elif usrKey in QUIT:
            if snake.paused:
                snake.gameOver(snake.score, False)
                return snake.score
            pause(True)
        if snake.paused:
            continue
        isOutOfBounds = checkOutOfBounds(boundsRange["x"], boundsRange["y"], snake.body[0]) or checkTailCollision(snake.body)
        collidingBorder = getCollidingBorder(snake.body[0], boundsRange)
        hasHitTail = checkTailCollision(snake.body)
        hasHitWall = isOutOfBounds and collidingBorder == snake.direction
        nextPosInBounds = checkNextHeadPosInBounds(snake.direction, getNewHeadPos(snake.direction, snake.body[0], boundsRange), boundsRange)
        nextPosCollidingBorder = getCollidingBorder(getNewHeadPos(snake.direction, snake.body[0], boundsRange), boundsRange)
        nextPosHasHitWall = not nextPosInBounds and nextPosCollidingBorder == snake.direction
        nextPosHasHitTail = checkNextHeadPosHitsTail(snake.direction, snake.body[0], boundsRange, snake.body)
        snakeIsMoving = not nextPosHasHitWall and not nextPosHasHitTail and not hasHitWall and not hasHitTail
        if snake.collisionStreak > snake.maxCollisionStreak:
            snake.gameOver(snake.score)
            return snake.score
        elif not snakeIsMoving:
            snake.collisionStreak += 1
        if snakeIsMoving:
            snake.move()
            snake.collisionStreak = 0
        if checkFoodEaten(snake.body[0], food.position):
            snake.consumeFood(1)
            food.relocate(snake.body)
