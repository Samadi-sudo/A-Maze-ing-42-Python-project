from mlx import Mlx

WIDTH = 1280
HEIGHT = 720

m = Mlx()

mlx_ptr = m.mlx_init()
win_ptr = m.mlx_new_window(mlx_ptr, WIDTH, HEIGHT, "Fast Draw (Frame-Based)")

# ---------------- IMAGE ----------------
img = m.mlx_new_image(mlx_ptr, WIDTH, HEIGHT)
addr, bpp, line_len, endian = m.mlx_get_data_addr(img)

# ---------------- STATE ----------------
state = {
    "color": 0xFFFF0000,   # ARGB red
    "mouse_down": False,
    "img": img,
    "addr": addr,
    "bpp": bpp,
    "line_len": line_len,
    "dirty": True          # needs redraw?
}

# ---------------- DRAWING ----------------
def img_pixel_put(data, x, y, color):
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return
    offset = y * data["line_len"] + x * (data["bpp"] // 8)
    data["addr"][offset:offset + 4] = color.to_bytes(4, "little")
    data["dirty"] = True

# ---------------- EVENTS ----------------
def on_key(key, data):
    if key == 65307:  # ESC
        m.mlx_loop_exit(mlx_ptr)
    elif key == 114:  # r
        data["color"] = 0xFFFF0000
    elif key == 103:  # g
        data["color"] = 0xFF00FF00
    return 0

def on_mouse_press(button, x, y, data):
    if button == 1:
        data["mouse_down"] = True
        img_pixel_put(data, x, y, data["color"])
    return 0

def on_mouse_release(button, x, y, data):
    if button == 1:
        data["mouse_down"] = False
    return 0

def on_mouse_move(x, y, data):
    if data["mouse_down"]:
        img_pixel_put(data, x, y, data["color"])
    return 0

def on_close(data):
    m.mlx_loop_exit(mlx_ptr)
    return 0

# ---------------- RENDER LOOP ----------------
def render(data):
    if data["dirty"]:
        m.mlx_put_image_to_window(
            mlx_ptr, win_ptr, data["img"], 0, 0
        )
        data["dirty"] = False
    return 0

# ---------------- HOOKS ----------------
m.mlx_key_hook(win_ptr, on_key, state)

m.mlx_mouse_hook(win_ptr, on_mouse_press, state)
m.mlx_hook(win_ptr, 5, 1 << 3, on_mouse_release, state)
m.mlx_hook(win_ptr, 6, 1 << 6, on_mouse_move, state)

m.mlx_hook(win_ptr, 33, 0, on_close, None)

# Frame-based rendering
m.mlx_loop_hook(mlx_ptr, render, state)

# ---------------- LOOP ----------------
m.mlx_loop(mlx_ptr)
