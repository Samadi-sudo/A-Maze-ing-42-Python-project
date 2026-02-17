import random
import a_star
import time
import printer
import minitouls


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


def generator(height, width, entry, exit, perfect, seed=None, animation=True):
    maze = ft_cells(height, width)
    walls = ft_walls(maze)
    error = minitouls.ft_42(maze, height, width, entry, exit)

    if seed is None:
        random.shuffle(walls)
    else:
        random.seed(seed)
        random.shuffle(walls)
    loop_probability = 0.2
    for cell_a, cell_b in walls:
        if not cell_a.closed and not cell_b.closed:
            if ft_union(cell_a, cell_b) is True:
                minitouls.remove_wall(cell_a, cell_b)
            elif (perfect is False and random.random() < loop_probability):
                minitouls.remove_wall(cell_a, cell_b)
        if animation:
            printer.print_maze(maze, None, entry, exit, error, None, None)
            time.sleep(0.1)
    if animation is False:
        printer.print_maze(maze, None, entry, exit, error,
                           None, None, animation)
    minitouls.ft_sumwalls(maze)
    minitouls.ft_closing_exterior(maze, height, width)
    if error:
        return (error, maze)
    return (None, maze)


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

