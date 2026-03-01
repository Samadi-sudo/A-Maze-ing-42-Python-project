import random
from typing import Optional, Any

N, E, S, W = 1, 2, 4, 8

DIRS = {
    'N': (0, -1, N, S),
    'E': (1, 0, E, W),
    'S': (0, 1, S, N),
    'W': (-1, 0, W, E)
}


class Cell:
    def __init__(self) -> None:
        self.walls = N | E | S | W
        self.visited = False

    def remove(self, wall_bit: int) -> None:
        self.walls &= ~wall_bit


class Maze:
    def __init__(self, w: int, h: int) -> None:
        self.w, self.h = w, h
        self.grid = [[Cell() for _ in range(w)] for _ in range(h)]

    def carve(self, x: int, y: int, direction: str) -> tuple:
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

    def moved(self, x: int, y: int, direction: str) -> tuple:
        if direction not in DIRS:
            raise ValueError("Bad direction")
        dx, dy, wall_here, _ = DIRS[direction]
        nx, ny = x + dx, y + dy
        if not (0 <= nx < self.w and 0 <= ny < self.h):
            return (x, y)
        if self.grid[y][x].walls & wall_here:
            return (x, y)
        if self.grid[ny][nx].visited:
            return (x, y)
        return (nx, ny)


class MazeGenerator:
    def __init__(self, width: int, height: int,
                 perfect: bool = True, seed: Optional[int] = None) -> None:
        if width < 2 or height < 2:
            raise ValueError("Width and height must both be >= 2.")
        self.width = width
        self.height = height
        self.perfect = perfect
        self.seed = seed
        self.maze = Maze(width, height)
        self.solution: list[tuple[int, int]] = []
        self.moves: list[tuple[int, int]] = []

    def p42(self) -> None:
        cell_closed = [
            (-1, 0), (-2, 0), (-3, 0), (-3, -1),
            (-3, -2), (-1, 1), (-1, 2),
            (1, 0), (1, 1), (1, 2), (2, 2),
            (3, 2), (2, 0), (3, 0), (3, -1), (3, -2),
            (1, -2), (2, -2)
        ]
        x = self.width // 2
        y = self.height // 2

        for dx, dy in cell_closed:
            new_x = x + dx
            new_y = y + dy
            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                self.maze.grid[new_y][new_x].visited = True

    def dfs_backtracking_recursive(self, x: int, y: int) -> bool:
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
                self.dfs_backtracking_recursive(nx, ny)
        return True

    def dfs_backtracking_iterative(self, x: int, y: int) -> None:
        stack = [(x, y)]
        while stack:
            x, y = stack[-1]
            self.maze.grid[y][x].visited = True
            directions = ["N", "E", "S", "W"]
            if self.seed is not None:
                rng: Any = random.Random(self.seed + x * self.height + y)
            else:
                rng = random
            rng.shuffle(directions)
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
        if self.perfect is False:
            self.make_imperfect(rng)

    def prims_algorithm(self, x: int, y: int) -> bool:
        """Generate maze using Prim's algorithm."""
        frontier = {}

        if self.maze.grid[y][x].visited:
            return False
        self.maze.grid[y][x].visited = True

        directions = ["N", "E", "S", "W"]
        frontier[(x, y)] = directions.copy()

        while frontier:
            if self.seed is not None:
                rng: Any = random.Random(self.seed + len(frontier))
                from_cell = rng.choice(list(frontier.keys()))
            else:
                from_cell = random.choice(list(frontier.keys()))

            fx, fy = from_cell

            if frontier[from_cell]:
                if self.seed is not None:
                    rng = random.Random(self.seed + sum(from_cell))
                else:
                    rng = random
                direction = rng.choice(frontier[from_cell])

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
        if self.perfect is False:
            self.make_imperfect(rng)
        return True

    def kruskal_algorithm(self) -> None:
        parent = dict()
        cell_to_root = {}
        for y in range(self.height):
            for x in range(self.width):
                parent[(x, y)] = [(x, y)]
                cell_to_root[(x, y)] = (x, y)

        def ft_find(pos: tuple) -> tuple:
            return (cell_to_root[pos])

        def ft_union(a: tuple, b: tuple) -> bool:
            root_a = ft_find(a)
            root_b = ft_find(b)
            if root_a == root_b:
                return False
            if len(parent[root_a]) < len(parent[root_b]):
                root_a, root_b = root_b, root_a
            for i in parent[root_b]:
                cell_to_root[i] = root_a

            parent[root_a].extend(parent[root_b])
            del parent[root_b]
            return (True)

        walls = []
        for y in range(self.height):
            for x in range(self.width):
                if x + 1 < self.width:
                    walls.append((x, y, 'E'))
                if y + 1 < self.height:
                    walls.append((x, y, 'S'))

        if self.seed is not None:
            rng: Any = random.Random(self.seed)
        else:
            rng = random
        rng.shuffle(walls)

        for x, y, direction in walls:
            dx, dy, cell, neighbor = DIRS[direction]
            nx, ny = x + dx, y + dy
            if (self.maze.grid[y][x].visited
                    or self.maze.grid[ny][nx].visited):
                continue
            if (ft_union((x, y), (nx, ny))):
                self.maze.grid[y][x].remove(cell)
                self.maze.grid[ny][nx].remove(neighbor)
                self.moves.append((nx, ny))

        if self.perfect is False:
            self.make_imperfect(rng)

    def dfs_solution(self, entry: tuple, sorti: tuple) -> list:
        stack = []
        stack.append(entry)
        history = []
        while stack:
            x, y = stack[-1]
            if (x, y) == sorti:
                break
            self.maze.grid[y][x].visited = True
            directions = ['N', 'E', 'S', 'W']
            moved = False
            for direction in directions:
                nx, ny = self.maze.moved(x, y, direction)
                if (nx != x or ny != y):
                    stack.append((nx, ny))
                    if (x, y) != entry:
                        history.append((x, y, 0xAF0FFF00))
                    moved = True
                    break
            if not moved:
                x, y = stack.pop()
                history.append((x, y, 0xFF000000))
        self.solution = stack
        return history

    def bfs_solution(self, entry: tuple, sorti: tuple) -> list:
        queue: list = [[entry, [entry]]]
        direction = ['N', 'E', 'S', 'W']
        history: list = []
        self.maze.grid[entry[1]][entry[0]].visited = True
        while queue:
            current, path = queue.pop(0)
            if current == sorti:
                self.solution = path
                return history
            x, y = current
            self.maze.grid[y][x].visited = True
            for i in direction:
                nx, ny = self.maze.moved(x, y, i)
                if (x != nx or y != ny):
                    history.append((nx, ny))
                    self.maze.grid[ny][nx].visited = True
                    queue.append([(nx, ny), path + [(nx, ny)]])
        return []

    def a_star_solution(self, entry: tuple, sorti: tuple) -> list:
        def ft_manhaten(pos: tuple, sorti: tuple) -> Any:
            xa, ya = pos
            xb, yb = sorti
            return (abs(xb - xa) + abs(yb - ya))
        
        # [(f, g, poinet, [path])]
        open_list = [(0, 0, entry, [entry])]
        directions = ['N', 'E', 'S', 'W']
        history: list = []
        while open_list:
            # get the point that has the smallest f
            best_index = 0
            for i in range(1, len(open_list)):
                if open_list[i][0] < open_list[best_index][0]:
                    best_index = i
            # remove the point on open_list
            f, g, current, path = open_list.pop(best_index)
            x, y = current
            if current == sorti:
                self.solution = path
                return history
            if self.maze.grid[y][x].visited:
                continue
            self.maze.grid[y][x].visited = True
            # Add neighbors to open_list
            for direction in directions:
                nx, ny = self.maze.moved(x, y, direction)
                if (nx, ny) == (x, y):
                    continue
                new_g = g + 1
                new_h = ft_manhaten((nx, ny), sorti)
                new_f = new_g + new_h
                history.append((nx, ny))
                open_list.append((new_f, new_g, (nx, ny), path + [(nx, ny)]))

        self.solution = []
        return history

    def make_imperfect(self, rng: Any = random) -> None:
        for y in range(self.height):
            for x in range(self.width):
                if self.maze.grid[y][x].walls == N | E | S | W:
                    self.maze.grid[y][x].visited = True
                else:
                    self.maze.grid[y][x].visited = False
        extra_passages = max(1, (self.width * self.height) // 10)
        for _ in range(extra_passages):
            x = rng.randint(0, self.width - 2)
            y = rng.randint(0, self.height - 2)
            direction = rng.choice(['E', 'S'])
            if (not self.maze.grid[y][x].visited
               and bin(self.maze.grid[y][x].walls).count('1') > 2):
                nx, ny = self.maze.carve(x, y, direction)
                self.maze.grid[y][x].visited = True
                if (nx, ny) != (x, y):
                    self.maze.grid[ny][nx].visited = True

