from mazegen_package.mazegen import N, E, S, W
import tkinter as tk
import os


def hline(mlx, mlx_ptr, img_ptr, x1, x2, y, color):
    for x in range(x1, x2):
        mlx.mlx_pixel_put(mlx_ptr, img_ptr, x, y, color)


def vline(mlx, mlx_ptr, img_ptr, x, y1, y2, color):
    for y in range(y1, y2):
        mlx.mlx_pixel_put(mlx_ptr, img_ptr, x, y, color)


def draw_cell(mlx, mlx_ptr, img_ptr, cell, x, y, WALL_COLOR, CELL):
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


def fill_cell(mlx, mlx_ptr, img_ptr, x, y, color, CELL):
    px = x * CELL
    py = y * CELL
    for i in range(px+2, px + CELL-1):
        for j in range(py+2, py + CELL-1):
            mlx.mlx_pixel_put(mlx_ptr, img_ptr, i, j, color)


def draw_42(mlx, mlx_ptr, img_ptr, color, centre, maze, CELL):
    x, y = centre
    lst_4 = [
        (x-3, y-2),
        (x-3, y-1),
        (x-3, y), (x-2, y), (x-1, y),
        (x - 1, y + 1),
        (x - 1, y + 2)

    ]
    lst_2 = [
        (x + 1, y - 2), (x + 2, y - 2), (x + 3, y - 2),
        (x + 3, y - 1),
        (x + 1, y), (x + 2, y), (x + 3, y),
        (x + 1, y + 1),
        (x + 1, y + 2), (x + 2, y + 2), (x + 3, y + 2)

    ]
    for x, y in lst_4:
        fill_cell(mlx, mlx_ptr, img_ptr, x, y, color, CELL)
        maze.grid[y][x].visited = True
    for x, y in lst_2:
        fill_cell(mlx, mlx_ptr, img_ptr, x, y, color, CELL)
        maze.grid[y][x].visited = True
    return maze


def resize_image_to_fit(input_path, size):
    root = tk.Tk()
    root.withdraw()  # close the window

    img = tk.PhotoImage(file=input_path)
    w = img.width()
    h = img.height()

    longest_side = max(w, h)
    factor = longest_side // size + 1

    if factor > 1:
        img = img.subsample(factor, factor)

    # Save next to the original with a "_resized" suffix
    base, ext = os.path.splitext(input_path)
    output_path = f"{base}_resized{ext}"
    img.write(output_path)
    root.destroy()
    return output_path


class MazeDrawer:
    def __init__(self, m, mlx_ptr, win_ptr, CELL):
        self.m = m
        self.mlx_ptr = mlx_ptr
        self.win_ptr = win_ptr
        self.CELL = CELL

    def draw_maze(self, WIDTH, HEIGHT, maze, color):
        for y in range(maze.h):
            for x in range(maze.w):
                draw_cell(self.m, self.mlx_ptr, self.win_ptr,
                          maze.grid[y][x], x, y, color ^ 0x00FF0F0F, self.CELL)
                maze.grid[y][x].visited = False
        if WIDTH > 8 and HEIGHT > 6:
            draw_42(self.m, self.mlx_ptr, self.win_ptr, color,
                    (WIDTH // 2, HEIGHT // 2), maze, self.CELL)

    def draw_cell(self, maze, x, y, color):
        tmp = maze.grid[y][x].walls
        maze.grid[y][x].walls = 15
        draw_cell(self.m, self.mlx_ptr, self.win_ptr,
                  maze.grid[y][x], x, y, 0xFF000000, self.CELL)
        maze.grid[y][x].walls = tmp
        draw_cell(self.m, self.mlx_ptr, self.win_ptr,
                  maze.grid[y][x], x, y, color ^ 0x00FF0F0F, self.CELL)

    def draw_image(self, x, y, player):
        resized_path = resize_image_to_fit(player, self.CELL)

        resized, w, h = self.m.mlx_png_file_to_image(
            self.mlx_ptr, resized_path)

        if resized:
            px = x * self.CELL
            py = y * self.CELL
            offset_x = (self.CELL - w) // 2
            offset_y = (self.CELL - h) // 2
            self.m.mlx_put_image_to_window(
                self.mlx_ptr,
                self.win_ptr, resized, px + offset_x, py + offset_y)
        return resized
