def dfs_Backtracking(x, y, WIDTH, HEIGHT):
        if maze.grid[y][x].visited:
            return False

        maze.grid[y][x].visited = True
        directions = ["N", "E", "S", "W"]
        if SEED is not None:
            rng = random.Random(SEED + x * HEIGHT + y)
            rng.shuffle(directions)
        else:
            random.shuffle(directions)
        
        for direction in directions:
            nx, ny = maze.carve(x, y, direction)

            if (nx != x or ny != y):
                drawer.draw_cell(maze, nx, ny)
                m.mlx_do_sync(mlx_ptr)
                time.sleep(0.01)
                dfs_Backtracking(nx, ny, WIDTH, HEIGHT)
        return True

def prims_Backtracking(x, y, WIDTH, HEIGHT):
    frontier = {}

    if maze.grid[y][x].visited:
        return False
    maze.grid[y][x].visited = True

    directions = ["N", "E", "S", "W"]
    frontier[(x, y)] = directions.copy()

    while frontier:
        if SEED is not None:
            rng = random.Random(SEED + len(frontier))
            from_cell = rng.choice(list(frontier.keys()))
        else:
            from_cell = random.choice(list(frontier.keys()))
        
        fx, fy = from_cell

        # Randomly select a direction
        if frontier[from_cell]:
            if SEED is not None:
                rng = random.Random(SEED + sum(from_cell))
                direction = rng.choice(frontier[from_cell])
            else:
                direction = random.choice(frontier[from_cell])

            nx, ny = maze.carve(fx, fy, direction)

            frontier[from_cell].remove(direction)
            if not frontier[from_cell]:
                del frontier[from_cell]

            if (nx != fx or ny != fy):
                if not maze.grid[ny][nx].visited:
                    maze.grid[ny][nx].visited = True
                    frontier[(nx, ny)] = ["N", "E", "S", "W"].copy()
                drawer.draw_cell(maze, nx, ny)
                m.mlx_do_sync(mlx_ptr)
        else:
            del frontier[from_cell]
    return True