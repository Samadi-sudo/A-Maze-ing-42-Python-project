from mlx import Mlx
from maze import Maze
from draw_maze import CELL, MazeDrawer
from parsing import parsing
import time
import random

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

    def bfs_backtracking(start_x, start_y, WIDTH, HEIGHT):
        from collections import deque
        
        queue = deque([(start_x, start_y)])
        maze.grid[start_y][start_x].visited = True
        
        while queue:
            # For true BFS, use popleft(). For randomized BFS, choose randomly
            if SEED is not None:
                rng = random.Random(SEED + len(queue))
                idx = rng.randint(0, len(queue) - 1)
                x, y = queue[idx]
                del queue[idx]
            else:
                idx = random.randint(0, len(queue) - 1)
                x, y = queue[idx]
                del queue[idx]
            
            # Get all valid directions
            directions = ["N", "E", "S", "W"]
            if SEED is not None:
                rng = random.Random(SEED + x * HEIGHT + y)
                rng.shuffle(directions)
            else:
                random.shuffle(directions)
            
            # Try to carve in each direction
            for direction in directions:
                nx, ny = maze.carve(x, y, direction)
                
                # If we successfully carved (moved to a new cell)
                if (nx != x or ny != y) and not maze.grid[ny][nx].visited:
                    maze.grid[ny][nx].visited = True
                    queue.append((nx, ny))
                    
                    # Optional: visualize
                    m.mlx_clear_window(mlx_ptr, win_ptr)
                    drawer.draw_maze(WIDTH, HEIGHT, maze, 0xFF00F0F0)

    bfs_backtracking(0,0, WIDTH, HEIGHT)
    m.mlx_clear_window(mlx_ptr, win_ptr)
    drawer.draw_maze(WIDTH, HEIGHT, maze, 0xFF00F0F0)
    def on_close(data):
        m.mlx_loop_exit(mlx_ptr)
        return 0

    m.mlx_hook(win_ptr, 33, 0, on_close, None)
    m.mlx_loop(mlx_ptr)