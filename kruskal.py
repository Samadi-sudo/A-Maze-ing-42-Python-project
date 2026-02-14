import random
import a_star
import time
import printer


class DisjointSet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.closed = False
        self.parent = self
        self.rank = 0
        self.walls = {"top": 1, "bottom": 4, "left": 8, "right": 2}
        self.walls_total = 15


def ft_cells(height, width):
    maze = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(DisjointSet(x, y))
        maze.append(row)
    return (maze)


def ft_walls(maze):
    walls = []
    height = len(maze)
    width = len(maze[0])
    for row in maze:
        for cell in row:
            x = cell.x
            y = cell.y
            if x+1 < width:
                walls.append((cell, maze[y][x+1]))
            if y+1 < height:
                walls.append((cell, maze[y+1][x]))
    return (walls)


def ft_find(cell):
    if cell.parent != cell:
        cell.parent = ft_find(cell.parent)
    return (cell.parent)


def ft_union(cell_a, cell_b):
    root_a = ft_find(cell_a)
    root_b = ft_find(cell_b)
    if root_a is root_b:
        return False

    if root_a.rank < root_b.rank:
        root_a.parent = root_b
    elif root_a.rank > root_b.rank:
        root_b.parent = root_a
    elif root_a.rank == root_b.rank:
        root_b.parent = root_a
        root_a.rank += 1
    return True


def remove_wall(cell_a, cell_b):
    dx = cell_b.x - cell_a.x
    dy = cell_b.y - cell_a.y

    if dx == 1:
        cell_b.walls["left"] = 0
        cell_a.walls["right"] = 0
    elif dx == -1:
        cell_b.walls["right"] = 0
        cell_a.walls["left"] = 0

    if dy == 1:
        cell_b.walls["top"] = 0
        cell_a.walls["bottom"] = 0
    elif dy == -1:
        cell_b.walls["bottom"] = 0
        cell_a.walls["top"] = 0


def ft_sumwalls(maze):
    for row in maze:
        for cell in row:
            cell.walls_total = sum(cell.walls.values())


def ft_closing_exterior(maze, height: int, width: int):
    for raw in maze:
        for cell in raw:
            if cell.y == 0:
                cell.walls["top"] = 1
            if cell.y == height - 1:
                cell.walls["bottom"] = 4

            if cell.x == 0:
                cell.walls["left"] = 8
            if cell.x == width - 1:
                cell.walls["right"] = 2

def check_exit_entry(
                x: int, y: int, cell_closed: list,
                entry: tuple, exit: tuple, height: int, width: int):
    shift_dir = [
        (0, 0),
        (-1, 0),
        (0, -1),
        (1, 0),
        (0, 1),
        (1, 1),
        (-1, -1),
        (-1, 1),
        (1, -1),
    ]
    for dx, dy in shift_dir:
        test_x = dx + x
        test_y = dy + y
        is_safe = True
        for clo_x, clo_y in cell_closed:
            final_x = clo_x + test_x
            final_y = clo_y + test_y
            if not (0 <= final_x < width and 0 <= final_y < height):
                is_safe = False
                break
            if ((final_x, final_y) == entry or (final_x, final_y) == exit):
                is_safe = False
                break
        if is_safe:
            return (test_x, test_y)
    raise ValueError(
        "Cannot place '42' pattern without collision. "
        "Try larger maze or different entry/exit positions."
    )


def ft_42(maze: list, height: int, width: int, entry, exit):
    if width < 8 or height < 6:
        return ("Cannot place '42' pattern without collision. "
                "Try larger maze")
    x, y = width // 2, height // 2
    cell_closed = [
            (-1, 0), (-2, 0), (-3, 0), (-3, -1),
            (-3, -2), (-1, 1), (-1, 2), (-1, -1),
            (-1, -2), (1, 0), (1, 1), (1, 2), (2, 2),
            (3, 2), (2, 0), (3, 0), (3, -1), (3, -2),
            (1, -2), (2, -2)
        ]
    try:
        x, y = check_exit_entry(x, y, cell_closed, entry, exit, height, width)
    except ValueError as e:
        return e
    for i, j in cell_closed:
        n_x = x+i
        n_y = y+j
        maze[n_y][n_x].closed = True
    return None


def generator(height, width, entry, exit, perfect, seed=None):
    maze = ft_cells(height, width)
    walls = ft_walls(maze)
    error = ft_42(maze, height, width, entry, exit)

    if seed is None:
        random.shuffle(walls)
    else:
        random.seed(seed)
        random.shuffle(walls)
    loop_probability = 0.2
    for cell_a, cell_b in walls:
        if not cell_a.closed and not cell_b.closed:
            if ft_union(cell_a, cell_b) is True:
                remove_wall(cell_a, cell_b)
            elif (perfect is False and random.random() < loop_probability):
                remove_wall(cell_a, cell_b)
        printer.print_maze(maze, None, entry, exit, error, None, None)
        time.sleep(0.2)
    ft_sumwalls(maze)
    ft_closing_exterior(maze, height, width)
    if error:
        return (error, maze)
    return (None, maze)


def ft_output(maze, filename, path, entry, exit):
    try:
        with open(filename, "w") as file:
            for raw in maze:
                for cell in raw:
                    file.write(format(cell.walls_total, 'X'))

                file.write("\n")
            i = 0
            file.write("\n")
            file.write(f"{entry[0]},{entry[1]}\n")
            file.write(f"{exit[0]},{exit[1]}\n")
            while i < len(path)-1:
                x = path[i].x
                y = path[i].y
                next_x = path[i+1].x
                next_y = path[i+1].y
                if next_x - x == 1:
                    file.write("E")
                if next_x - x == -1:
                    file.write("W")
                if next_y - y == 1:
                    file.write("S")
                if next_y - y == -1:
                    file.write("N")
                i += 1
    except Exception:
        return
# kruskal_generator(height, width)
# this function is return
# [
#     [cell,cell,cell,cell,cell,cell ...]
#     [cell,cell,cell,cell,cell,cell ...]
#     [cell,cell,cell,cell,cell,cell ...]
#     [cell,cell,cell,cell,cell,cell ...]
#     [cell,cell,cell,cell,cell,cell ...]
#     [cell,cell,cell,cell,cell,cell ...]
# ]
# cell.x => The horizontal position of the cell in the grid
# cell.y => The vertical position of the cell in the grid
# cell.walls_total => The sum of the numeric values of the existing walls

