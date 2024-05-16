__all__ = [
    "getDirectionAxis",
    "getNewDirection",
    "checkWallCollision",
    "checkFoodEaten",
    "checkTailCollision",
    "getPointsPerFood",
]

def getPointsPerFood(screen_size: tuple) -> int:
    ppf = int(212 / (screen_size[0] * screen_size[1]) * 100)
    return ppf if ppf <= 7 else 7

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
