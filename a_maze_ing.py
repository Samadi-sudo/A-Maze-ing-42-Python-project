from mlx import Mlx
from maze import Maze
from draw_maze import CELL, MazeDrawer
from parsing import parsing
import time
import random
import sys

sys.setrecursionlimit(1000000)
config = parsing()
WIDTH, HEIGHT = config['WIDTH'], config['HEIGHT']
SEED = config.get('seed', None)
# create maze
maze = Maze(WIDTH, HEIGHT)

# carve something for testing
# maze.carve(2, 0, 'S')
# maze.carve(2, 1, 'S')
if __name__ == "__main__":
    # init mlx
    m = Mlx()
    mlx_ptr = m.mlx_init()
    win_ptr = m.mlx_new_window(mlx_ptr, WIDTH * CELL + 1, HEIGHT * CELL + 1, "Maze")

    # draw maze
    drawer = MazeDrawer(m,mlx_ptr, win_ptr)
    drawer.draw_maze(WIDTH, HEIGHT, maze, 0xFF00F0F0)
    def dfs_Backtracking(x, y, WIDTH, HEIGHT):
        if maze.grid[y][x].visited:
            return False

        m.mlx_clear_window(mlx_ptr, win_ptr)
        drawer.draw_maze(WIDTH, HEIGHT, maze, 0xFF00F0F0)
        maze.grid[y][x].visited = True
        directions = ["N", "E", "S", "W"]
        if SEED is not None:
            rng = random.Random(SEED + x * HEIGHT + y)
            rng.shuffle(directions)
        else:
            random.shuffle(directions)
        
        for direction in directions:
            nx, ny = maze.carve(x, y, direction)

            if (nx != x or ny != y):
                dfs_Backtracking(nx, ny, WIDTH, HEIGHT)
        return True

    def prims_Backtracking(x, y, WIDTH, HEIGHT, frontier=None):
        if frontier is None:
            frontier = {}

        if maze.grid[y][x].visited:
            return False
        maze.grid[y][x].visited = True

        m.mlx_clear_window(mlx_ptr, win_ptr)
        drawer.draw_maze(WIDTH, HEIGHT, maze, 0xFF00F0F0)

        directions = ["N", "E", "S", "W"]
        frontier[(x, y)] = directions.copy()

        while frontier:
            if SEED is not None:
                rng = random.Random(SEED + len(frontier))
                from_cell = rng.choice(list(frontier.keys()))
            else:
                from_cell = random.choice(list(frontier.keys()))
            
            fx, fy = from_cell
            
            # Randomly select a direction
            if frontier[from_cell]:
                if SEED is not None:
                    rng = random.Random(SEED + sum(from_cell))
                    direction = rng.choice(frontier[from_cell])
                else:
                    direction = random.choice(frontier[from_cell])

                nx, ny = maze.carve(fx, fy, direction)

                frontier[from_cell].remove(direction)
                if not frontier[from_cell]:
                    del frontier[from_cell]

                if (nx != fx or ny != fy):
                    prims_Backtracking(nx, ny, WIDTH, HEIGHT, frontier)
            else:
                del frontier[from_cell]
        
        return True
        
        return True

    prims_Backtracking(0,0, WIDTH, HEIGHT)
    m.mlx_clear_window(mlx_ptr, win_ptr)
    drawer.draw_maze(WIDTH, HEIGHT, maze, 0xFF00F0F0)
    def on_close(data):
        m.mlx_loop_exit(mlx_ptr)
        return 0

    m.mlx_hook(win_ptr, 33, 0, on_close, None)
    m.mlx_loop(mlx_ptr)