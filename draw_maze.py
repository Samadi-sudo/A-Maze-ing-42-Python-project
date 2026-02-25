from typing import Any
from mazegen_package.mazegen import N, E, S, W
import tkinter as tk
import os


def hline(mlx: Any, mlx_ptr: Any, img_ptr: Any, x1: int,
          x2: int, y: int, color: Any) -> None:
    for x in range(x1, x2):
        mlx.mlx_pixel_put(mlx_ptr, img_ptr, x, y, color)


def vline(mlx: Any, mlx_ptr: Any, img_ptr: Any,
          x: int, y1: int, y2: int, color: Any) -> None:
    for y in range(y1, y2):
        mlx.mlx_pixel_put(mlx_ptr, img_ptr, x, y, color)


def draw_cell(mlx: Any, mlx_ptr: Any, img_ptr: Any, cell: Any,
              x: int, y: int, WALL_COLOR: Any, CELL: int) -> None:
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


def fill_cell(mlx: Any, mlx_ptr: Any, img_ptr: Any,
              x: int, y: int, color: Any, CELL: int) -> None:
    px = x * CELL
    py = y * CELL
    for i in range(px+2, px + CELL-1):
        for j in range(py+2, py + CELL-1):
            mlx.mlx_pixel_put(mlx_ptr, img_ptr, i, j, color)


def draw_42(mlx: Any, mlx_ptr: Any, img_ptr: Any, color: Any,
            centre: tuple, maze: Any, CELL: int) -> Any:
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


def resize_image_to_fit(input_path: str, size: int) -> str:
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
    def __init__(self, m: Any, mlx_ptr: Any, win_ptr: Any, CELL: int) -> None:
        self.m = m
        self.mlx_ptr = mlx_ptr
        self.win_ptr = win_ptr
        self.CELL = CELL

    def draw_maze(self, WIDTH: int, HEIGHT: int,
                  maze: Any, color: Any) -> None:
        for y in range(maze.h):
            for x in range(maze.w):
                draw_cell(self.m, self.mlx_ptr, self.win_ptr,
                          maze.grid[y][x], x, y, color ^ 0x00FF0F0F, self.CELL)
                maze.grid[y][x].visited = False
        if WIDTH > 8 and HEIGHT > 6:
            draw_42(self.m, self.mlx_ptr, self.win_ptr, color,
                    (WIDTH // 2, HEIGHT // 2), maze, self.CELL)

    def draw_cell(self, maze: Any, x: int, y: int, color: Any) -> None:
        tmp = maze.grid[y][x].walls
        maze.grid[y][x].walls = 15
        draw_cell(self.m, self.mlx_ptr, self.win_ptr,
                  maze.grid[y][x], x, y, 0xFF000000, self.CELL)
        maze.grid[y][x].walls = tmp
        draw_cell(self.m, self.mlx_ptr, self.win_ptr,
                  maze.grid[y][x], x, y, color ^ 0x00FF0F0F, self.CELL)

    def draw_image(self, x: int, y: int, player: str) -> Any:
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
