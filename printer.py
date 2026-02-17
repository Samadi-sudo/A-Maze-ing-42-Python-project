import os
import platform


class Color:
    walls = 0
    block = 0


def print_maze(maze, path=None, entry=(), exit=(), message=None, color_wa=None, color_42=None, animation = True):
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    height = len(maze)
    width = len(maze[0])
    if color_wa is not None:
        Color.walls = color_wa
    if color_42 is not None:
        Color.block = color_42

    wall_colors = ['🟩', '🟫', '🟥', '🟨', '🟧', '🟪']
    block_colors = ['🔥', '⛔️', '❌', '🐱']
    wall = wall_colors[Color.walls]
    corner = wall_colors[Color.walls]
    path_icon = '🐾'
    end = '🦴'
    start = '🐕' 
    block = block_colors[Color.block]
    space = "  "

    if path is None:
        path = []


    def is_in_path(x, y):
        if x >= width or y >= height:
            return False
        return maze[y][x] in path
    if message:
        print(message)
    for y in range(height):
        top_line = ""
        for x in range(width):
            top_line += corner
            cell = maze[y][x]
            if cell.walls['top']:
                top_line += wall
            elif is_in_path(x, y) and is_in_path(x, y-1):
                top_line += path_icon
            else:
                top_line += space
        top_line += corner
        print(top_line)

        midel_line = ""
        for x in range(width):
            cell = maze[y][x]
            if cell.walls['left']:
                midel_line += wall
            elif is_in_path(x, y) and is_in_path(x-1, y):
                midel_line += path_icon
            else:
                midel_line += space

            if cell.closed:
                midel_line += block
            elif x == entry[0] and y == entry[1]:
                midel_line += start
            elif x == exit[0] and y == exit[1]:
                midel_line += end
            elif cell in path:
                midel_line += path_icon
            else:
                midel_line += space

        if maze[y][-1].walls['right']:
            midel_line += wall
        else:
            midel_line += space
        print(midel_line)
        btom_line = ""
    for x in range(width):
        btom_line += corner
        cell = maze[-1][x]
        if cell.walls['bottom']:
            btom_line += wall
        else:
            btom_line += space
    btom_line += corner
    print(btom_line)
    if path == []:
        show_or_hide = 'Show'
    else:
        show_or_hide = 'Hide'
    if animation is False:
        an = 'Activate'
        s = '  '
    else:
        an = 'Deactivate'
        s = ''
    print('════════════════ A-Maze-ing ══════════════')
    print('| 1. Re-generate a new maze              |')
    print(f'| 2. {show_or_hide} path from entry to exit        |')
    print('| 3. Rotate maze colors                  |')
    print('| 4. Change color pattern 42             |')
    print(f'| 5. {an} animation           {s}     |')
    print(f'| 6. Change in algorithm                 |')
    print('| 7. Quit                                |')
    print('══════════════════════════════════════════')



                



