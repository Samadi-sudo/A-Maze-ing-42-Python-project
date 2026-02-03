from mlx import Mlx

m = Mlx()

mlx_ptr = m.mlx_init()
win_ptr = m.mlx_new_window(mlx_ptr, 1280, 720, "Draw with mouse")

# ---------------- STATE ----------------
state = {
    "color": 0xFFFF0000,   # Red
    "mouse_down": False
}

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
    if button == 1:  # Left button
        data["mouse_down"] = True
        m.mlx_pixel_put(mlx_ptr, win_ptr, x, y, data["color"])
    return 0

def on_mouse_release(button, x, y, data):
    if button == 1:
        data["mouse_down"] = False
    return 0

def on_mouse_move(x, y, data):
    if data["mouse_down"]:
        m.mlx_pixel_put(mlx_ptr, win_ptr, x, y, data["color"])
    return 0

def on_close(data):
    m.mlx_loop_exit(mlx_ptr)
    return 0

# ---------------- HOOKS ----------------
m.mlx_key_hook(win_ptr, on_key, state)

# Button press
m.mlx_mouse_hook(win_ptr, on_mouse_press, state)

# Button release (ButtonRelease = 5, ButtonReleaseMask = 1 << 3)
m.mlx_hook(win_ptr, 5, 1 << 3, on_mouse_release, state)

# Mouse motion (MotionNotify = 6, PointerMotionMask = 1 << 6)
m.mlx_hook(win_ptr, 6, 1 << 6, on_mouse_move, state)

# Window close
m.mlx_hook(win_ptr, 33, 0, on_close, None)

# ---------------- LOOP ----------------
m.mlx_loop(mlx_ptr)
