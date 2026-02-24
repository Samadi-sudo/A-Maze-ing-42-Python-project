def draw_rectangle_border(mlx, mlx_ptr, win_ptr, x, y, w, h, color):
    for i in range(w):
        mlx.mlx_pixel_put(mlx_ptr, win_ptr, x + i, y, color)
        mlx.mlx_pixel_put(mlx_ptr, win_ptr, x + i, y + h, color)

    for j in range(h):
        mlx.mlx_pixel_put(mlx_ptr, win_ptr, x, y + j, color)
        mlx.mlx_pixel_put(mlx_ptr, win_ptr, x + w, y + j, color)


def find_area(button, x, y, w, h):
    nx, ny = button
    if ((x + 1)<= nx <= (x + w -1)) and ((y + 1)<= ny <= (y + h -1)):
        return True
    else:
        return False

def fill_rectangle(x, y, w, h, mlx, mlx_ptr, win_ptr):
    for i in range(x + 1, x + w):
        for j in range(y + 1, y+ h):
            mlx.mlx_pixel_put(mlx_ptr, win_ptr, i, j, 0xF500F0F0)
    draw_menu(mlx, mlx_ptr, win_ptr)
    for i in range(x + 1, x + w):
        for j in range(y + 1, y+ h):
            mlx.mlx_pixel_put(mlx_ptr, win_ptr, i, j, 0xFF000000)
    mlx.mlx_clear_window(mlx_ptr, win_ptr)
    draw_menu(mlx, mlx_ptr, win_ptr)

    

def draw_menu(mlx, mlx_ptr, menu_ptr):
    mlx.mlx_string_put(mlx_ptr, menu_ptr, 190, 10, 0xFF00F0F0, "Welcome to my:")
    mlx.mlx_string_put(mlx_ptr, menu_ptr, 180, 30, 0xFF00F0F0, "A_Maze_In_python")
    initial = 60
    mlx.mlx_do_sync(mlx_ptr)
    lst_buttons = []
    for i in range(6):
        draw_rectangle_border(mlx, mlx_ptr, menu_ptr, 20, initial, 450, 60, 0xFFFFFFFF)
        lst_buttons.append((20, initial))
        initial += 70
    mlx.mlx_do_sync(mlx_ptr)
    mlx.mlx_string_put(mlx_ptr, menu_ptr, 120, 80, 0xFFFFFFFF, "1-Re-generate a new maze.")
    mlx.mlx_string_put(mlx_ptr, menu_ptr, 165, 150, 0xFFFFFFFF, "2-Show/Hide path.")
    mlx.mlx_string_put(mlx_ptr, menu_ptr, 150, 220, 0xFFFFFFFF, "3-Rotate maze color.")
    mlx.mlx_string_put(mlx_ptr, menu_ptr, 150, 290, 0xFFFFFFFF, "4-find_path dfs/bfs.")
    mlx.mlx_string_put(mlx_ptr, menu_ptr, 160, 360, 0xFFFFFFFF, "5-Take the prize.")
    mlx.mlx_string_put(mlx_ptr, menu_ptr, 150, 430, 0xFFFFFFFF, "6-Annimation ON/OFF.")
    mlx.mlx_string_put(mlx_ptr, menu_ptr, 100, 480, 0xFF00F0F0, "to quit the menu you can just")
    mlx.mlx_string_put(mlx_ptr, menu_ptr, 150, 500, 0xFF00F0F0, "press the x button.")
    mlx.mlx_do_sync(mlx_ptr)
    return lst_buttons

def menu_ptr(mlx, mlx_ptr):
    menu_ptr = mlx.mlx_new_window(mlx_ptr, 500, 550, "Menu/User_interface")
    lst_buttons = draw_menu(mlx, mlx_ptr, menu_ptr)
    def on_mouse(button, x, y, data):
        if button == 1:
            if find_area((x,y), lst_buttons[0][0], lst_buttons[0][1], 450, 60):
                fill_rectangle(lst_buttons[0][0], lst_buttons[0][1], 450, 60, mlx, mlx_ptr, menu_ptr)
            if find_area((x,y), lst_buttons[1][0], lst_buttons[1][1], 450, 60):
                fill_rectangle(lst_buttons[1][0], lst_buttons[1][1], 450, 60, mlx, mlx_ptr, menu_ptr)
            if find_area((x,y), lst_buttons[2][0], lst_buttons[2][1], 450, 60):
                fill_rectangle(lst_buttons[2][0], lst_buttons[2][1], 450, 60, mlx, mlx_ptr, menu_ptr)
            if find_area((x,y), lst_buttons[3][0], lst_buttons[3][1], 450, 60):
                fill_rectangle(lst_buttons[3][0], lst_buttons[3][1], 450, 60, mlx, mlx_ptr, menu_ptr)
                

        print(f"Mouse Button {button} at ({x},{y})")
        return 0
    mlx.mlx_mouse_hook(menu_ptr, on_mouse, None)