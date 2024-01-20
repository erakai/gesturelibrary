import math


def dist_2d(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt(math.pow(abs(x1 - x2), 2) + math.pow(abs(y1 - y2), 2))
