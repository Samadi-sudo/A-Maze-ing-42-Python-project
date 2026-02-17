from mlx import Mlx
from maze import Maze
from draw_maze import CELL, MazeDrawer
from parsing import parsing
import time
import random
import sys

sys.setrecursionlimit(2147483647)
config = parsing()
WIDTH, HEIGHT = config['WIDTH'], config['HEIGHT']
SEED = config.get('seed')
ALGORITHM = config.get('algorithm')
# create maze
maze = Maze(WIDTH, HEIGHT)


if __name__ == "__main__":
    # init mlx
    from carve_algo import prims_Backtracking, dfs_Backtracking
    m = Mlx()
    mlx_ptr = m.mlx_init()
    win_ptr = m.mlx_new_window(mlx_ptr, WIDTH * CELL + 1, HEIGHT * CELL + 1, "Maze")

    # draw maze
    drawer = MazeDrawer(m,mlx_ptr, win_ptr)
    drawer.draw_maze(WIDTH, HEIGHT, maze, 0xFF00F0F0)

    

    def loop(data):
        dfs_Backtracking(0,0, WIDTH, HEIGHT)
        m.mlx_clear_window(mlx_ptr, win_ptr)
        drawer.draw_maze(WIDTH, HEIGHT, maze, 0xFF00F0F0)
        return 0
    def on_close(data):
        m.mlx_loop_exit(mlx_ptr)
        return 0
    m.mlx_hook(win_ptr, 33, 0, on_close, None)
    m.mlx_loop_hook(mlx_ptr, loop, None)
    print("salam")
    m.mlx_loop(mlx_ptr)
