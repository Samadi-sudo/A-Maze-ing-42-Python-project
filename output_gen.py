from mazegen_package.mazegen import MazeGenerator, DIRS


def path(maze_gen: MazeGenerator) -> list:
    dic = DIRS
    coordinates = maze_gen.solution
    directions = []
    for i in range(len(coordinates) - 1):
        dx = coordinates[i+1][0] - coordinates[i][0]
        dy = coordinates[i+1][1] - coordinates[i][1]
        for name, (vx, vy, *_) in dic.items():
            if (dx, dy) == (vx, vy):
                directions.append(name)
    return directions


def output_maze(maze_gen: MazeGenerator,
                file: str, ENTRY: tuple, EXIT: tuple) -> None:
    rows = len(maze_gen.maze.grid)
    cols = len(maze_gen.maze.grid[0])
    sx, sy = ENTRY
    ex, ey = EXIT
    with open(file, 'w') as f:
        for y in range(rows):
            for x in range(cols):
                f.write(hex(maze_gen.maze.grid[y][x].walls)[2:])
            f.write('\n')
        f.write(f"\n{sx},{sy}\n")
        f.write(f"{ex},{ey}\n")
        for i in path(maze_gen):
            f.write(i)
