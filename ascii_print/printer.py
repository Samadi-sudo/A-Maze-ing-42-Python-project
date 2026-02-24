import os
import platform


class Color:
    walls = 0
    block = 0


def print_maze(maze, path=None, entry=(), exit=(), message=None, color_wa=None,
               color_42=None, animation=True):
    N , E, S , W = 1, 2, 4, 8
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    height = len(maze)
    width = len(maze[0])
    if color_wa:
        Color.walls = color_wa
    if color_42:
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
    draw = ""
    def is_in_path(x, y):
        if x >= width or y >= height:
            return False
        return (x, y) in path
    if message:
        print(message)
    for y in range(height):
        top_line = ""
        for x in range(width):
            top_line += corner
            cell = maze[y][x]
            if cell.walls & N:
                top_line += wall
            elif is_in_path(x, y) and is_in_path(x, y-1):
                top_line += path_icon
            else:
                top_line += space
        top_line += corner
        draw += top_line + "\n"

        midel_line = ""
        for x in range(width):
            cell = maze[y][x]
            if cell.walls & W:
                midel_line += wall
            elif is_in_path(x, y) and is_in_path(x-1, y):
                midel_line += path_icon
            else:
                midel_line += space

            if cell.visited and cell.walls == 15:
                midel_line += block
            elif x == entry[0] and y == entry[1]:
                midel_line += start
            elif x == exit[0] and y == exit[1]:
                midel_line += end
            elif (x, y) in path:
                midel_line += path_icon
            else:
                midel_line += space

        if maze[y][-1].walls & E:
            midel_line += wall
        else:
            midel_line += space
        draw += midel_line + "\n"
        btom_line = ""
    for x in range(width):
        btom_line += corner
        cell = maze[-1][x]
        if cell.walls & S:
            btom_line += wall
        else:
            btom_line += space
    btom_line += corner
    draw += btom_line + "\n"
    print(draw)
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
    print('═══════════════ A-Maze-ing ═══════════════')
    print('| 1. Re-generate a new maze              |')
    print(f'| 2. {show_or_hide} path from entry to exit        |')
    print('| 3. Rotate maze colors                  |')
    print('| 4. Change color pattern 42             |')
    print(f'| 5. {an} animation           {s}     |')
    print('| 6. Change generation algorithm         |')
    print('| 7. Change solution algorithm           |')
    print('| 8. Moving the dog                      |')
    print('| 9. Quit                                |')
    print('══════════════════════════════════════════')