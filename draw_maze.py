from maze import N, E, S, W
CELL = 20
WALL_COLOR = 0xFFFFFFFF

def hline(mlx, mlx_ptr, img_ptr, x1, x2, y, color):
    for x in range(x1, x2):
        mlx.mlx_pixel_put(mlx_ptr, img_ptr, x, y, color)

def vline(mlx, mlx_ptr, img_ptr, x, y1, y2, color):
    for y in range(y1, y2):
        mlx.mlx_pixel_put(mlx_ptr, img_ptr, x, y, color)

def draw_cell(mlx, mlx_ptr, img_ptr, cell, x, y):
    px = x * CELL
    py = y * CELL

    if cell.walls & N:
        hline(mlx, mlx_ptr, img_ptr, px, px + CELL, py, WALL_COLOR)

    if cell.walls & E:
        vline(mlx, mlx_ptr, img_ptr, px + CELL, py, py + CELL, WALL_COLOR)

    if cell.walls & S:
        hline(mlx, mlx_ptr, img_ptr, px, px + CELL, py + CELL, WALL_COLOR)

    if cell.walls & W:
        vline(mlx, mlx_ptr, img_ptr, px, py, py + CELL, WALL_COLOR)

def fill_cell(mlx, mlx_ptr, img_ptr,x , y, color):
    px = x * CELL
    py = y * CELL
    for i in range(px + 2, px + CELL - 1):
        for j in range(py + 2, py + CELL - 1):
            mlx.mlx_pixel_put(mlx_ptr, img_ptr, i, j, color)

def draw_42(mlx, mlx_ptr, img_ptr, color, centre):
    from main import maze
    x, y = centre
    lst_4 = [
                (x-3, y-2),
                (x-3, y-1),
                (x-3, y),(x-2, y), (x-1, y),
                                   (x - 1, y + 1),
                                   (x - 1, y + 2)
            ]
    lst_2 = [
                (x + 1, y - 2), (x + 2, y -2), (x + 3, y -2),
                                                (x + 3, y - 1),
                        (x + 1, y),(x + 2, y),(x + 3, y),
                        (x + 1, y + 1),
                        (x + 1, y + 2),(x + 2, y + 2), (x + 3, y + 2)

    ]
    for x, y in lst_4:
        fill_cell(mlx, mlx_ptr, img_ptr, x, y ,0xFFFFFF00)
        maze.grid[y][x].visited = True
    for x, y in lst_2:
        fill_cell(mlx, mlx_ptr, img_ptr, x, y ,0xFFFFFF00)
        maze.grid[y][x].visited = True
