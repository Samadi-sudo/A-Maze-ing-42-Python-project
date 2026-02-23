from parsing import parsing
from mazegen_package.mazegen import MazeGenerator
from mlx import Mlx
from draw_maze import MazeDrawer, fill_cell
from menu import menu_ptr
import sound
from output_gen import output_maze
import signal

signal.signal(signal.SIGINT, signal.SIG_IGN)

config = parsing()
WIDTH, HEIGHT = config['WIDTH'], config['HEIGHT']
PERFECT = config['PERFECT']
ENTRY = config['ENTRY']
EXIT = config['EXIT']
SEED = config.get('seed')
OUTPUT_FILE = config.get('OUTPUT_FILE')
ALGORITHM = config.get('algorithm', 'dfs')
colors = [0xFF00F0F0, 0xFF0000FF, 0xFFFF00FF]

# create maze
maze_gen = MazeGenerator(WIDTH, HEIGHT, PERFECT, SEED)
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
    win_ptr = m.mlx_new_window(
        mlx_ptr, WIDTH * CELL + 1, HEIGHT * CELL + 1, "Maze")
    state = menu_ptr(m, mlx_ptr)
    display = {'path': False}
    # draw maze
    drawer = MazeDrawer(m, mlx_ptr, win_ptr, CELL)
    drawer.draw_maze(WIDTH, HEIGHT, maze_gen.maze, colors[state['3']])

    def gen_animation(speed):
        for x, y in maze_gen.moves:
            drawer.draw_cell(maze_gen.maze, x, y, colors[state['3']])
            if ((y % speed*2 == 0) and (x % speed*2 == 0)):
                m.mlx_do_sync(mlx_ptr)

    def history_annimation(speed, animation, algo, color):
        history = algo(ENTRY, EXIT)
        if animation:
            for x, y in history:
                fill_cell(m, mlx_ptr, win_ptr, x, y, color, CELL)
                if ((y % speed * 2 == 0) and (x % speed * 2 == 0)):
                    m.mlx_do_sync(mlx_ptr)

    def history_annimation_dfs(speed, animation):
        history = maze_gen.dfs_solution(ENTRY, EXIT)
        for x, y, color in history:
            fill_cell(m, mlx_ptr, win_ptr, x, y, color, CELL)
            if ((y % speed * 2 == 0) and (x % speed * 2 == 0) and animation):
                m.mlx_do_sync(mlx_ptr)

    def path_animation(speed, animation):
        path = maze_gen.solution
        for x, y in path:
            fill_cell(m, mlx_ptr, win_ptr, x, y, 0xAF0FFF00, CELL)
            if ((y % 2 == 0) and (x % 2 == 0) and animation):
                m.mlx_do_sync(mlx_ptr)

    if ALGORITHM.lower() == 'dfs':
        maze_gen.dfs_backtracking_iterative(ENTRY[0], ENTRY[1])
    elif ALGORITHM.lower() == 'kruskal':
        maze_gen.kruskal_algorithm()
    else:
        maze_gen.prims_algorithm(ENTRY[0], ENTRY[1])

    m.mlx_clear_window(mlx_ptr, win_ptr)
    drawer.draw_image(ENTRY[0], ENTRY[1],
                      "./images/mouse/Cute_Mouse_Runaway.png")
    drawer.draw_image(EXIT[0], EXIT[1], "./images/mouse/cheese.png")
    drawer.draw_maze(WIDTH, HEIGHT, maze_gen.maze, colors[state['3']])
    m.mlx_do_sync(mlx_ptr)
    output_maze(maze_gen, OUTPUT_FILE, ENTRY, EXIT)

    def show_path(animation, color, take_prize=False):
        if display['path'] == False or take_prize == True:
            if state['4'] == 1:
                algo = maze_gen.a_star_solution
                history_annimation(5, animation, algo, 0xAF0000FF)
                m.mlx_clear_window(mlx_ptr, win_ptr)
                drawer.draw_maze(WIDTH, HEIGHT, maze_gen.maze, color)
                path_animation(5, animation)
            elif state['4'] == 0:
                algo = maze_gen.bfs_solution
                history_annimation(5, animation, algo, 0xAF0FFF00)
                m.mlx_clear_window(mlx_ptr, win_ptr)
                drawer.draw_maze(WIDTH, HEIGHT, maze_gen.maze, color)
                path_animation(5, animation)
            else:
                history_annimation_dfs(3, animation)
                m.mlx_clear_window(mlx_ptr, win_ptr)
                drawer.draw_maze(WIDTH, HEIGHT, maze_gen.maze, color)
                path_animation(5, animation)
                
            display['path'] = True
        else:
            m.mlx_clear_window(mlx_ptr, win_ptr)
            drawer.draw_maze(WIDTH, HEIGHT, maze_gen.maze, color)
            m.mlx_do_sync(mlx_ptr)
            display['path'] = False

    def take_prize():
        sound.play_song("./sound_effect/start.wav")
        sound.stop_song("./sound_effect/mouse/mouse-squeek.wav")
        show_path(False, colors[state['3']], True)
        drawer.draw_image(EXIT[0], EXIT[1], "./images/mouse/cheese.png")
        prev = None
        for x, y in maze_gen.solution:
            if prev:
                fill_cell(m, mlx_ptr, win_ptr,
                          prev[0], prev[1], 0xFF0FFF00, CELL)
            drawer.draw_image(x, y, "./images/mouse/Cute_Mouse_Runaway.png")
            sound.play_song("./sound_effect/mouse/mouse-walking.wav")
            prev = (x, y)
        fill_cell(m, mlx_ptr, win_ptr, prev[0], prev[1], 0xFF0FFF00, CELL)
        sound.stop_song("./sound_effect/start.wav")
        sound.stop_song("./sound_effect/mouse/mouse-walking.wav")
        sound.play_song("./sound_effect/Win.wav")
        drawer.draw_image(x, y, "./images/mouse/Cute Mouse_Eating_Cheese.png")
        sound.play_song("./sound_effect/mouse/mouse-squeek.wav")

    def regenerate(color):
        maze_gen.__init__(WIDTH, HEIGHT, PERFECT, SEED)
        m.mlx_clear_window(mlx_ptr, win_ptr)
        drawer.draw_maze(WIDTH, HEIGHT, maze_gen.maze, color)
        m.mlx_do_sync(mlx_ptr)
        if ALGORITHM.lower() == 'dfs':
            maze_gen.dfs_backtracking_iterative(ENTRY[0], ENTRY[1])
        elif ALGORITHM.lower() == 'kruskal':
            maze_gen.kruskal()
        else:
            maze_gen.prims_algorithm(ENTRY[0], ENTRY[1])
        if state['6'] == True:
            gen_animation(2)
        else:
            m.mlx_clear_window(mlx_ptr, win_ptr)
        drawer.draw_image(ENTRY[0], ENTRY[1],
                          "./images/mouse/Cute_Mouse_Runaway.png")
        drawer.draw_image(EXIT[0], EXIT[1], "./images/mouse/cheese.png")
        drawer.draw_maze(WIDTH, HEIGHT, maze_gen.maze, color)
        m.mlx_do_sync(mlx_ptr)
        if SEED is None:
            output_maze(maze_gen, OUTPUT_FILE, ENTRY, EXIT)

    def on_loop(data):
        if state['1']:
            regenerate(colors[state['3']])
            state['1'] = False
            display['path'] = False
        if state['2']:
            show_path(state['6'], colors[state['3']])
            drawer.draw_image(ENTRY[0], ENTRY[1],
                              "./images/mouse/Cute_Mouse_Runaway.png")
            drawer.draw_image(EXIT[0], EXIT[1], "./images/mouse/cheese.png")
            output_maze(maze_gen, OUTPUT_FILE, ENTRY, EXIT)
            state['2'] = False
        if state['5']:
            take_prize()
            output_maze(maze_gen, OUTPUT_FILE, ENTRY, EXIT)
            state['5'] = False
        return 0

    def on_close(data):
        m.mlx_loop_exit(mlx_ptr)
        return 0

    m.mlx_loop_hook(mlx_ptr, on_loop, None)
    m.mlx_hook(win_ptr, 33, 0, on_close, None)
    m.mlx_loop(mlx_ptr)
