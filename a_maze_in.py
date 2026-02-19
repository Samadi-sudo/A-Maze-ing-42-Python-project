from mlx import Mlx
from draw_maze import MazeDrawer, fill_cell
from parsing import parsing
from mazegen_package.mazegen import Maze, MazeGenerator
import time
import sys

sys.setrecursionlimit(2147483647)
config = parsing()
WIDTH, HEIGHT = config['WIDTH'], config['HEIGHT']
PERFECT = config['PERFECT']
ENTRY = config['ENTRY']
EXIT = config['EXIT']
SEED = config.get('seed')
ALGORITHM = config.get('algorithm', 'dfs')

# create maze
maze_gen = MazeGenerator(WIDTH, HEIGHT, seed=SEED)
maze = maze_gen.maze

if __name__ == "__main__":
    # init mlx
    m = Mlx()
    mlx_ptr = m.mlx_init()
    _, screen_width, screen_height = m.mlx_get_screen_size(mlx_ptr)
    screen_height -= 40
    screen_width -= 40
    CELL = min(screen_width // WIDTH, screen_height // HEIGHT)
    CELL = max(5, min(CELL, 50))
    win_ptr = m.mlx_new_window(mlx_ptr, WIDTH * CELL + 1, HEIGHT * CELL + 1, "Maze")

    # draw maze
    drawer = MazeDrawer(m, mlx_ptr, win_ptr, CELL)
    drawer.draw_maze(WIDTH, HEIGHT, maze, 0xFF00F0F0)

    if ALGORITHM.lower() == 'dfs':
        maze_gen.dfs_backtracking_iterative(0, 0)
    else:
        maze_gen.prims_algorithm(0, 0)

    for x, y in maze_gen.moves:
            drawer.draw_cell(maze, x, y)
            if ((y % 19 == 0) and (x % 19 == 0)):
                m.mlx_do_sync(mlx_ptr)
    # i = 0
    # while i < 5:
    #     img = drawer.draw_image(0,i, "./images/mouse/Cute_Mouse_Runaway.png")
    #     m.mlx_destroy_image(mlx_ptr, img)
    #     m.mlx_clear_window(mlx_ptr, win_ptr)
    #     drawer.draw_maze(WIDTH, HEIGHT, maze, 0xFF00F0F0)
    #     i += 1
    drawer.draw_image(0,0, "./images/mouse/Cute_Mouse_Runaway.png")
    drawer.draw_image(382,200, "./images/mouse/cheese.png")
    drawer.draw_maze(WIDTH, HEIGHT, maze, 0xFF00F0F0)
    path, history = maze_gen.bfs_solution((0,0), (382,200))
    for x, y in history:
            fill_cell(m, mlx_ptr, win_ptr,x , y, 0xFF0FFF00, CELL)
            if ((y % 10 == 0) and (x % 10 == 0)):
                m.mlx_do_sync(mlx_ptr)
    m.mlx_clear_window(mlx_ptr, win_ptr)
    drawer.draw_maze(WIDTH, HEIGHT, maze, 0xFF00F0F0)
    for x, y in path:
            fill_cell(m, mlx_ptr, win_ptr,x , y, 0xFF0FFF00, CELL)
            if ((y % 2 == 0) and (x % 2 == 0)):
                m.mlx_do_sync(mlx_ptr)

    drawer.draw_image(382,200, "./images/mouse/cheese.png")
    drawer.draw_image(0,0, "./images/mouse/Cute_Mouse_Runaway.png")
    drawer.draw_maze(WIDTH, HEIGHT, maze, 0xFF00F0F0)

    def on_close(data):
        m.mlx_loop_exit(mlx_ptr)
        return 0

    m.mlx_hook(win_ptr, 33, 0, on_close, None)
    m.mlx_loop(mlx_ptr)

