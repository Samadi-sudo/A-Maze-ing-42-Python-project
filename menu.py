def draw_rectangle_border(mlx, mlx_ptr, win_ptr, x, y, w, h, color):
    for i in range(w):
        mlx.mlx_pixel_put(mlx_ptr, win_ptr, x + i, y, color)
        mlx.mlx_pixel_put(mlx_ptr, win_ptr, x + i, y + h, color)

    for j in range(h):
        mlx.mlx_pixel_put(mlx_ptr, win_ptr, x, y + j, color)
        mlx.mlx_pixel_put(mlx_ptr, win_ptr, x + w, y + j, color)


def find_area(button, x, y, w, h):
    nx, ny = button
    if ((x + 1) <= nx <= (x + w - 1)) and ((y + 1) <= ny <= (y + h - 1)):
        return True
    else:
        return False


def fill_rectangle(x, y, w, h, mlx, mlx_ptr, win_ptr):
    for i in range(x + 1, x + w):
        for j in range(y + 1, y + h):
            mlx.mlx_pixel_put(mlx_ptr, win_ptr, i, j, 0xF500F0F0)
    draw_menu(mlx, mlx_ptr, win_ptr)
    for i in range(21, 470):
        for j in range(10, 540):
            mlx.mlx_pixel_put(mlx_ptr, win_ptr, i, j, 0xFF000000)
            if (i % 235 == 0 and j == 0):
                mlx.mlx_do_sync(mlx_ptr)
    draw_menu(mlx, mlx_ptr, win_ptr)


def draw_menu(mlx, mlx_ptr, menu_ptr):
    mlx.mlx_string_put(mlx_ptr, menu_ptr, 190, 10,
                       0xFF00F0F0, "Welcome to my:")
    mlx.mlx_string_put(mlx_ptr, menu_ptr, 180, 30,
                       0xFF00F0F0, "A_Maze_In_python")
    initial = 60
    mlx.mlx_do_sync(mlx_ptr)
    lst_buttons = []
    for i in range(6):
        draw_rectangle_border(mlx, mlx_ptr, menu_ptr, 20,
                              initial, 450, 60, 0xFFFFFFFF)
        lst_buttons.append((20, initial))
        initial += 70
        if i % 3 == 0:
            mlx.mlx_do_sync(mlx_ptr)
    mlx.mlx_string_put(mlx_ptr, menu_ptr, 120, 80,
                       0xFFFFFFFF, "1-Re-generate a new maze.")
    mlx.mlx_string_put(mlx_ptr, menu_ptr, 165, 150,
                       0xFFFFFFFF, "2-Show/Hide path.")
    mlx.mlx_string_put(mlx_ptr, menu_ptr, 150, 220,
                       0xFFFFFFFF, "3-Rotate maze color.")
    mlx.mlx_do_sync(mlx_ptr)
    mlx.mlx_string_put(mlx_ptr, menu_ptr, 135, 290,
                       0xFFFFFFFF, "4-find_path A*/dfs/bfs.")
    mlx.mlx_string_put(mlx_ptr, menu_ptr, 160, 360,
                       0xFFFFFFFF, "5-Take the prize.")
    mlx.mlx_string_put(mlx_ptr, menu_ptr, 150, 430,
                       0xFFFFFFFF, "6-Annimation ON/OFF.")
    mlx.mlx_string_put(mlx_ptr, menu_ptr, 100, 480,
                       0xFF00F0F0, "to quit the menu you can just")
    mlx.mlx_string_put(mlx_ptr, menu_ptr, 150, 500,
                       0xFF00F0F0, "press the x button.")
    mlx.mlx_do_sync(mlx_ptr)
    return lst_buttons


def menu_ptr(mlx, mlx_ptr):
    menu_ptr = mlx.mlx_new_window(mlx_ptr, 500, 550, "Menu/User_interface")
    mlx.mlx_clear_window(mlx_ptr, menu_ptr)
    lst_buttons = draw_menu(mlx, mlx_ptr, menu_ptr)

    state = {
        '1': False,  # Re-generate maze
        '2': False,  # Show/Hide path
        '3': 0,      # Color rotation index
        '4': 0,      # DFS(0) or BFS(1)
        '5': False,  # Take the prize
        '6': True,   # Animation on/off
    }

    def on_mouse(button, x, y, data):
        if button == 1:
            mlx.mlx_do_sync(mlx_ptr)
            if find_area((x, y), lst_buttons[0][0],
                         lst_buttons[0][1], 450, 60):
                fill_rectangle(
                    lst_buttons[0][0], lst_buttons[0][1],
                    450, 60, mlx, mlx_ptr, menu_ptr)
                state['1'] = True
            if find_area((x, y), lst_buttons[1][0],
                         lst_buttons[1][1], 450, 60):
                fill_rectangle(
                    lst_buttons[1][0], lst_buttons[1][1],
                    450, 60, mlx, mlx_ptr, menu_ptr)
                state['2'] = not state['2']
            if find_area((x, y), lst_buttons[2][0],
                         lst_buttons[2][1], 450, 60):
                fill_rectangle(
                    lst_buttons[2][0], lst_buttons[2][1],
                    450, 60, mlx, mlx_ptr, menu_ptr)
                state['3'] = (state['3'] + 1) % 3
            if find_area((x, y), lst_buttons[3][0],
                         lst_buttons[3][1], 450, 60):
                fill_rectangle(
                    lst_buttons[3][0], lst_buttons[3][1],
                    450, 60, mlx, mlx_ptr, menu_ptr)
                state['4'] = (state['4'] + 1) % 3
            if find_area((x, y), lst_buttons[4][0],
                         lst_buttons[4][1], 450, 60):
                fill_rectangle(
                    lst_buttons[4][0], lst_buttons[4][1],
                    450, 60, mlx, mlx_ptr, menu_ptr)
                state['5'] = True
            if find_area((x, y), lst_buttons[5][0],
                         lst_buttons[5][1], 450, 60):
                fill_rectangle(
                    lst_buttons[5][0], lst_buttons[5][1],
                    450, 60, mlx, mlx_ptr, menu_ptr)
                state['6'] = not state['6']
        print(f"Mouse Button {button} at ({x},{y})")
        return 0

    def on_key(keycode, data):
        if keycode == 49:
            mlx.mlx_do_sync(mlx_ptr)
            fill_rectangle(lst_buttons[0][0], lst_buttons[0]
                           [1], 450, 60, mlx, mlx_ptr, menu_ptr)
            state['1'] = True
        if keycode == 50:
            mlx.mlx_do_sync(mlx_ptr)
            fill_rectangle(lst_buttons[1][0], lst_buttons[1]
                           [1], 450, 60, mlx, mlx_ptr, menu_ptr)
            state['2'] = not state['2']
        if keycode == 51:
            mlx.mlx_do_sync(mlx_ptr)
            fill_rectangle(lst_buttons[2][0], lst_buttons[2]
                           [1], 450, 60, mlx, mlx_ptr, menu_ptr)
            state['3'] = (state['3'] + 1) % 3
        if keycode == 52:
            mlx.mlx_do_sync(mlx_ptr)
            fill_rectangle(lst_buttons[3][0], lst_buttons[3]
                           [1], 450, 60, mlx, mlx_ptr, menu_ptr)
            state['4'] = (state['4'] + 1) % 2
        if keycode == 53:
            mlx.mlx_do_sync(mlx_ptr)
            fill_rectangle(lst_buttons[4][0], lst_buttons[4]
                           [1], 450, 60, mlx, mlx_ptr, menu_ptr)
            state['5'] = True
        if keycode == 54:
            mlx.mlx_do_sync(mlx_ptr)
            fill_rectangle(lst_buttons[5][0], lst_buttons[5]
                           [1], 450, 60, mlx, mlx_ptr, menu_ptr)
            state['6'] = not state['6']
        return 0

    mlx.mlx_key_hook(menu_ptr, on_key, None)
    mlx.mlx_mouse_hook(menu_ptr, on_mouse, None)
    return state
