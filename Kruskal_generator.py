import random


class DisjointSet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
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


def ft_walls(maze, width, height):
    walls = []
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


def kruskal_generator(height, width):
    maze = ft_cells(height, width)
    walls = ft_walls(maze, width, height)
    random.shuffle(walls)
    for cell_a, cell_b in walls:
        if ft_union(cell_a, cell_b) is True:
            remove_wall(cell_a, cell_b)
    ft_sumwalls(maze)
    return (maze)


def ft_output(maze, filename):
    try:
        with open(filename, "w") as file:
            for raw in maze:
                for cell in raw:
                    file.write(format(cell.walls_total, 'X'))
                file.write("\n")
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
