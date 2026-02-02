from mlx import Mlx
from maze import Maze
from draw_maze import draw_cell, CELL
import sys

WIDTH, HEIGHT = 10, 10

# create maze
maze = Maze(WIDTH, HEIGHT)

# carve something for testing
for i in range(100):
    maze.carve(0, i, 'S')
# maze.carve(1, 0, 'E')
# maze.carve(2, 0, 'S')
# maze.carve(2, 1, 'S')

# init mlx
m = Mlx()
mlx_ptr = m.mlx_init()
win_ptr = m.mlx_new_window(mlx_ptr, WIDTH * CELL, HEIGHT * CELL, "Maze")

# draw maze
for y in range(maze.h):
    for x in range(maze.w):
        draw_cell(m, mlx_ptr, win_ptr, maze.grid[y][x], x, y)

def on_close(data):
    m.mlx_loop_exit(mlx_ptr)
    return 0

m.mlx_hook(win_ptr, 33, 0, on_close, None)
m.mlx_loop(mlx_ptr)