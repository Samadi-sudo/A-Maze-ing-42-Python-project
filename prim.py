import random
import printer
import time
import minitouls
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = {"top": 1, "bottom": 4, "left": 8, "right": 2}
        self.walls_total = 15
        self.closed = False



def grid(height, width):
    maze = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(Cell(x, y))
        maze.append(row)
    return (maze)



def ft_frontier(maze, cell, frontier, height, width, visited):
    fron = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    for x, y in fron:
        n_x = x + cell.x
        n_y = y + cell.y
        if (0 <= n_x < width and 0 <= n_y < height
                and maze[n_y][n_x] not in frontier
                and maze[n_y][n_x].visited is visited):
            frontier.append(maze[n_y][n_x])
    return (frontier)


def imperfect(maze, height, width):
    cels = [cel for row in maze for cel in row if not cel.closed]
    cel = random.choice(cels)
    if cel.y > 0 and not maze[cel.y - 1][cel.x].closed:
        cel.walls["top"] = 0
    if cel.x < width - 1 and not maze[cel.y][cel.x + 1].closed:
        cel.walls["right"] = 0


def generator(height, width, entry, exit, perfect, seed=None, animation=True):
    if seed is not None:
        random.seed(seed)
    frontier = []
    maze = grid(height, width)
    error = minitouls.ft_42(maze, height, width, entry, exit)
    cell = maze[entry[1]][entry[0]]
    cell.visited = True
    # if perfect is False and random.random() < 0.2:
    #     ft_frontier(maze, cell, frontier, height, width, True)
    # else:
    ft_frontier(maze, cell, frontier, height, width, False)
    while frontier:
        neighbor = random.choice(frontier)
        frontier.remove(neighbor)

        neighbors_visited = []
        ft_frontier(maze, neighbor, neighbors_visited, height, width, True)
        if neighbors_visited:
            target = random.choice(neighbors_visited)
            if not target.closed and not neighbor.closed:
                minitouls.remove_wall(target, neighbor)
                neighbor.visited = True
                ft_frontier(maze, neighbor, frontier, height, width, False)
        if not perfect and random.random() < 0.25:
            imperfect(maze, height, width)

        if animation:
            printer.print_maze(maze, None, entry, exit, None, None, None, None)
            time.sleep(0.15)
    if not animation:
        printer.print_maze(maze, None, entry, exit, None, None, None, None)
    minitouls.ft_closing_exterior(maze, height, width)
    minitouls.ft_sumwalls(maze)
    if error:
        return (error, maze)
    return (None, maze)


# generator(3, 3, (0, 0), (1, 1), False,3)
#generator(3, 3, (0, 0), (1, 1), False, None, True)
