import random
from typing import Optional

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
        self.visited = False

    def remove(self, wall_bit):
        self.walls &= ~wall_bit


class Maze:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.grid = [[Cell() for _ in range(w)] for _ in range(h)]

    def carve(self, x, y, direction):
        if direction not in DIRS:
            raise ValueError("bad direction")
        dx, dy, wall_here, wall_there = DIRS[direction]
        nx, ny = x + dx, y + dy
        if not (0 <= nx < self.w and 0 <= ny < self.h):
            return (x, y)
        if self.grid[ny][nx].visited:
            return (x, y)
        self.grid[y][x].remove(wall_here)
        self.grid[ny][nx].remove(wall_there)
        return (nx, ny)

class MazeGenerator:
    def __init__(self, width: int, height: int, entry: tuple[int, int] = (0, 0), end: tuple[int, int] | None = None, perfect: bool = True, seed: Optional[int] = None):
        if width < 2 or height < 2:
            raise ValueError("Width and height must both be >= 2.")
        self.width = width
        self.height = height
        self.entry = entry
        self.end = end
        self.perfect = perfect
        self.seed = seed
        self.maze = Maze(width, height)
        self.solution = []
        self.moves: list[tuple[int, int]] = []

    def dfs_backtracking_recursive(self, x: int, y: int):
        """Generate maze using Depth-First Search with backtracking."""
        if self.maze.grid[y][x].visited:
            return False

        self.maze.grid[y][x].visited = True
        directions = ["N", "E", "S", "W"]
        if self.seed is not None:
            rng = random.Random(self.seed + x * self.height + y)
            rng.shuffle(directions)
        else:
            random.shuffle(directions)

        for direction in directions:
            nx, ny = self.maze.carve(x, y, direction)

            if (nx != x or ny != y):
                self.moves.append((nx, ny))
                self.dfs_backtracking(nx, ny)
        return True

    def dfs_backtracking_iterative(self, x: int, y:int):
            stack = [(x, y)]
            while stack:
                x, y = stack[-1]
                self.maze.grid[y][x].visited = True
                directions = ["N", "E", "S", "W"]
                if self.seed is not None:
                    rng = random.Random(self.seed + x * self.height + y)
                    rng.shuffle(directions)
                else:
                    random.shuffle(directions)
                moved = False
                for direction in directions:
                    nx, ny = self.maze.carve(x, y, direction)
                    if (nx != x or ny != y):
                        self.moves.append((nx, ny))
                        stack.append((nx, ny))
                        moved = True
                        break
                if not moved:
                    stack.pop() 
                
    def prims_algorithm(self, x: int, y: int):
        """Generate maze using Prim's algorithm."""
        frontier = {}

        if self.maze.grid[y][x].visited:
            return False
        self.maze.grid[y][x].visited = True

        directions = ["N", "E", "S", "W"]
        frontier[(x, y)] = directions.copy()

        while frontier:
            if self.seed is not None:
                rng = random.Random(self.seed + len(frontier))
                from_cell = rng.choice(list(frontier.keys()))
            else:
                from_cell = random.choice(list(frontier.keys()))
            
            fx, fy = from_cell

            if frontier[from_cell]:
                if self.seed is not None:
                    rng = random.Random(self.seed + sum(from_cell))
                    direction = rng.choice(frontier[from_cell])
                else:
                    direction = random.choice(frontier[from_cell])

                nx, ny = self.maze.carve(fx, fy, direction)

                frontier[from_cell].remove(direction)
                if not frontier[from_cell]:
                    del frontier[from_cell]

                if (nx != fx or ny != fy):
                    if not self.maze.grid[ny][nx].visited:
                        self.maze.grid[ny][nx].visited = True
                        frontier[(nx, ny)] = ["N", "E", "S", "W"].copy()
                    self.moves.append((nx, ny))
            else:
                del frontier[from_cell]
        return True