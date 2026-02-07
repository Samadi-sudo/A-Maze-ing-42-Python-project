from mlx import Mlx
from maze import Maze
from draw_maze import CELL, MazeDrawer
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
    drawer = MazeDrawer(m,mlx_ptr, win_ptr)
    for i in range(10):
        m.mlx_clear_window(mlx_ptr, win_ptr)
        drawer.draw_maze(WIDTH, HEIGHT, maze,0xFFFFFFFF)
        # time.sleep(0.5)
        maze.carve(2, i, 'S')
        # maze.carve(3, i, 'S')
        # maze.carve(4, i, 'S')
        # maze.carve(5, i, 'S')
        # maze.carve(6, i, 'S')
        # maze.carve(7, i, 'S')
        # maze.carve(8, i, 'S')
    def on_close(data):
        m.mlx_loop_exit(mlx_ptr)
        return 0

    m.mlx_hook(win_ptr, 33, 0, on_close, None)
    m.mlx_loop(mlx_ptr)