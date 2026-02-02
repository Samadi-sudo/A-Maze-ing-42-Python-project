N , E , S , W = 1, 2, 4, 8

DIRS = {
    'N': (0, -1, N, S),
    'E': (1, 0, E, W),
    'S': (0, 1, S, N),
    'W': (-1, 0, W, E)
}

class Cell:
    def __init__(self):
        self.walls = N | E | S | W

    def remove(self, wall_bit):
        self.walls &= ~wall_bit

class Maze:
    def __init__(self, w, h):
            self.w , self.h = w, h
            self.grid = [[Cell() for _ in range(w)] for _ in range(h)]

    def carve(self, x, y, direction):
        if direction not in DIRS:
            raise ValueError("bad direction")
        dx, dy, wall_here, wall_there = DIRS[direction]
        nx, ny = x + dx, y + dy
        if not (0 <= nx < self.w and 0 <= ny < self.h):
            return False
        self.grid[y][x].remove(wall_here)
        self.grid[ny][nx].remove(wall_there)
        return True
