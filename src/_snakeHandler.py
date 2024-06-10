__all__ = [
    "getDirectionAxis",
    "getNewDirection",
    "checkWallCollision",
    "checkFoodEaten",
    "checkTailCollision",
    "getBorderPosition",
    "checkOutOfBounds",
    "getNewHeadPos",
    "checkNextHeadPosInBounds",
    "getCollidingBorder",
    "checkNextHeadPosHitsTail",
]

def getDirectionAxis(direction: str) -> str:
    return "x" if direction in ["right", "left"] else "y"

def getNewDirection(newDirection: str, currentDirection: str) -> str:
    return newDirection if getDirectionAxis(newDirection) != getDirectionAxis(currentDirection) else currentDirection

def checkWallCollision(position: tuple, borderPosition: tuple) -> bool:
    if position[0] <= 0 or position[0] >= borderPosition[0] or position[1] <= 0 or position[1] >= borderPosition[1]:
        return True
    return False

def checkFoodEaten(headPosition: tuple, foodPosition: tuple) -> bool:
    return headPosition == foodPosition

def checkTailCollision(snakeBody: list) -> bool:
    for i in range(1, len(snakeBody)):
        if snakeBody[0] == snakeBody[i]:
            return True
    return False

def getBorderPosition(screen_size: tuple[int, int], border_size: tuple = (20, 10)) -> dict[str, tuple]:
    x = screen_size[0]//2 - border_size[0]//2, screen_size[0]//2 + border_size[0]//2
    y = screen_size[1]//2 - border_size[1]//2, screen_size[1]//2 + border_size[1]//2
    return {"x": x, "y": y}

def checkOutOfBounds(range_x: tuple, range_y: tuple, headPosition: tuple) -> bool:
    inXBounds = headPosition[0] in range(range_x[0]+1, range_x[1])
    inYBounds = headPosition[1] in range(range_y[0]+1, range_y[1])
    if not inXBounds or not inYBounds:
        return True
    return False

def getNewHeadPos(direction: str, currentPosition: tuple, boundsRange: dict[str, tuple]) -> tuple:
    match direction:
        case "up" | "down":
            newHeadPos = (currentPosition[0], currentPosition[1]-1 if direction=="up" else currentPosition[1]+1)
        case "right" | "left":
            newHeadPos = (currentPosition[0]+1 if direction=="right" else currentPosition[0]-1, currentPosition[1])
    if checkOutOfBounds(boundsRange["x"], boundsRange["y"], newHeadPos):
        return currentPosition
    return newHeadPos

def checkNextHeadPosInBounds(direction: str, currentPosition: tuple, boundsRange: dict[str, tuple]) -> bool:
    newPos = getNewHeadPos(direction, currentPosition, boundsRange)
    return not checkOutOfBounds(boundsRange["x"], boundsRange["y"], newPos)

def getCollidingBorder(currentPosition: tuple, boundsRange: dict[str, tuple]) -> str:
    xBounds = boundsRange["x"]
    yBounds = boundsRange["y"]
    collidingBorder = None
    if currentPosition[0] <= xBounds[0]:
        collidingBorder = "left"
    elif currentPosition[0] >= xBounds[1]:
        collidingBorder = "right"
    elif currentPosition[1] <= yBounds[0]:
        collidingBorder = "up"
    elif currentPosition[1] >= yBounds[1]:
        collidingBorder = "down"
    return collidingBorder

def checkNextHeadPosHitsTail(direction: str, currentPosition: tuple, boundsRange: dict, snakeBody: list[tuple]) -> bool:
    nextHeadPos = getNewHeadPos(direction, currentPosition, boundsRange)
    if nextHeadPos in snakeBody:
        return True
    return False
