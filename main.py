from mlx import Mlx
from maze import Maze
from draw_maze import draw_cell, CELL, draw_42
import time

WIDTH, HEIGHT = 10, 10

# create maze
maze = Maze(WIDTH, HEIGHT)

# carve something for testing
# maze.carve(1, 0, 'E')
# maze.carve(2, 0, 'S')
# maze.carve(2, 1, 'S')
if __name__ == "__main__":
    # init mlx
    m = Mlx()
    mlx_ptr = m.mlx_init()
    win_ptr = m.mlx_new_window(mlx_ptr, WIDTH * CELL + 1, HEIGHT * CELL + 1, "Maze")

    # draw maze
    for i in range(10):
        m.mlx_clear_window(mlx_ptr, win_ptr)
        for y in range(maze.h):
            for x in range(maze.w):
                draw_cell(m, mlx_ptr, win_ptr, maze.grid[y][x], x, y)
        #time.sleep(0.5)
        if maze.grid[y][i].visited == False:
            maze.carve(2, i, 'S')
    if (WIDTH > 8 and HEIGHT > 6):
        draw_42(m, mlx_ptr, win_ptr, 0xFFFFFF00, (WIDTH // 2, HEIGHT // 2))
    def on_close(data):
        m.mlx_loop_exit(mlx_ptr)
        return 0

    m.mlx_hook(win_ptr, 33, 0, on_close, None)
    m.mlx_loop(mlx_ptr)