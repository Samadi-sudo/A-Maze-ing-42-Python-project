from maze import N, E, S, W

CELL = 50
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