def ft_manhaten(a: object, b: object):
    return (abs(b.x - a.x) + abs(b.y - a.y))


def ft_openlist(open_list, closed_list, poinet, maze,
                height, width, g_scord, new_g):
    directions = [
        (-1, 0, "left"),
        (1, 0, "right"),
        (0, -1, "top"),
        (0, 1, "bottom"),
    ]
    for dx, dy, wall in directions:
        new_x, new_y = poinet.x + dx, poinet.y + dy
        if 0 <= new_x < width and 0 <= new_y < height:
            neighbor = maze[new_y][new_x]
            if (poinet.walls[wall] == 0 and neighbor not in closed_list):
                if (neighbor not in open_list):
                    open_list.add(neighbor)
                    g_scord[neighbor] = new_g
                    neighbor.parent = poinet
                elif (new_g < g_scord[neighbor]):
                    g_scord[neighbor] = new_g
                    neighbor.parent = poinet


def solve(a, b, maze):
    width = len(maze[0])
    height = len(maze)
    open_list = set()
    closed_list = set()
    next = a
    path = []
    g_scord = {a: 0}
    brakes = 0
    while brakes < (height * width * 3):
        brakes += 1
        if next == b:
            while next != a:
                path.append(next)
                next = next.parent
            path.append(a)
            path.reverse()
            return (path)

        new_g = g_scord.get(next, 0) + 1
        ft_openlist(open_list, closed_list, next, maze,
                    height, width, g_scord, new_g)
       # dirct = dict()
        if not open_list:
            return None
       # for item in open_list:
        #    dirct.update({item: ft_manhaten(item, b) + g_scord[item]})
        next_point = min(open_list, key=lambda item: g_scord[item] + ft_manhaten(item, b))  # يجب فهم هدا السطر جيدا
        closed_list.add(next)
        next = next_point
        open_list.discard(next)   # remove
