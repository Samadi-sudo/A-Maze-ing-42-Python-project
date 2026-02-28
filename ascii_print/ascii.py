import sys
import os
import time
import platform
from typing import Any
from output_gen import output_maze
from ascii_print import printer
import sound


def animation(hestory: list, entry: tuple,
              exit: tuple, anim: bool, maze: list, mesage: str,
              template: Any) -> bool:
    """ Displays the process of creating the maze step
        by step as an animation or no"""
    template.p42
    t_maze = template.maze.grid
    if anim:
        for x, y in hestory:
            t_maze[y][x] = maze[y][x]
            printer.print_maze(t_maze, None, entry, exit, None,
                               None, None, False)
            time.sleep(0.3)
    printer.print_maze(maze, None, entry, exit, mesage, None, None, False)
    return (anim)


def path_animation(path: list, grid: list, entry: tuple, exit: tuple,
                   anim: bool = True, mesage: str = "") -> bool:
    """Displays the process of solving the
       maze (path) as an animation or no."""
    if anim:
        for i in range(len(path)):
            solve = path[:i+1]
            printer.print_maze(grid, solve, entry, exit, mesage,
                               None, None, anim)
            time.sleep(0.3)
    else:
        printer.print_maze(grid, path, entry, exit, mesage, None, None, anim)
    return (anim)


def desplay(choice: int, grid: list, path: list | None, ENTRY: tuple,
            EXIT: tuple, mesage: str, color_walls: int,
            color_42: int, anim: bool) -> int:
    """Manages the display interface and updates options after
      each selection from the menu"""
    if choice not in [1, 2, 3, 4, 5, 6, 7, 8]:
        printer.print_maze(grid, path, ENTRY, EXIT, mesage, color_walls,
                           color_42, anim)
        print("The option is incorrect 😵")
        choice = int(input('Choice ?(1-9): '))
    elif choice == 9:
        return 9
    else:
        printer.print_maze(grid, path, ENTRY, EXIT, mesage, color_walls,
                           color_42, anim)
        choice = int(input('Choice ?(1-9): '))
    return choice


def main(HEIGHT: int, WIDTH: int, ENTRY: tuple, EXIT: tuple,
         OUTPUT_FILE: str, PERFECT: bool, maze: Any, template: Any,
         SEED: int | None = None, algo: str = "kruskal") -> Any:
    """    This function manages: maze generation, color changes,
    sound activation, selection of  generation algorithms (Kruskal,
    Prim's, DFS) and solution algorithms (A*, BFS, DFS)"""
    choice = 1
    anim = False
    color_walls = 0
    color_42 = 0
    path = None
    solve_algo = 1
    mesage = ""
    while choice != 9:
        try:
            if choice == 1:
                maze.__init__(WIDTH, HEIGHT, PERFECT, SEED)
                if WIDTH < 6 or WIDTH < 8:
                    mesage = "Cannot place '42' pattern without collision"
                else:
                    maze.p42()
                if algo is None or algo == "kruskal":
                    maze.kruskal_algorithm()
                elif algo == "prims":
                    maze.prims_algorithm(ENTRY[0], ENTRY[1])
                else:
                    maze.dfs_backtracking_iterative(ENTRY[0], ENTRY[1])
                hestory = maze.moves
                grid = maze.maze.grid
                for x in range(WIDTH):
                    for y in range(HEIGHT):
                        if maze.maze.grid[y][x].walls != 15:
                            maze.maze.grid[y][x].visited = False
                        template.maze.grid[y][x].walls = 15
                        template.maze.grid[y][x].visited = False
                if solve_algo == 2:
                    maze.bfs_solution(ENTRY, EXIT)
                elif solve_algo == 3:
                    maze.dfs_solution(ENTRY, EXIT)
                else:
                    maze.a_star_solution(ENTRY, EXIT)
                animation(hestory, ENTRY, EXIT, anim,
                          grid, mesage, template)
                output_maze(maze, OUTPUT_FILE, ENTRY, EXIT)
                choice = int(input('Choice ?(1-9): '))
                continue
            elif choice == 2:
                path = maze.solution
                path_animation(path, grid, ENTRY, EXIT, anim, mesage)
                choice = int(input('Choice ?(1-9): '))
                path = None
                if choice == 2:
                    choice = desplay(choice, grid, path, ENTRY, EXIT, mesage,
                                     color_walls, color_42, anim)
            elif choice == 3:
                test = int(input("0:🟩 1:🟫 2:🟥 3:🟨 4:🟧 5:🟪 "))
                if test not in [0, 1, 2, 3, 4, 5]:
                    choice = 127
                else:
                    color_walls = test
                choice = desplay(choice, grid, path, ENTRY, EXIT, mesage,
                                 color_walls, color_42, anim)
            elif choice == 4:
                test = int(input("0:🔥 1:⛔️ 2:❌ 3:🐱 "))
                if test not in [0, 1, 2, 3]:
                    choice = 127
                else:
                    color_42 = test
                choice = desplay(choice, grid, path, ENTRY, EXIT, mesage,
                                 color_walls, color_42, anim)
            elif choice == 5:
                if anim:
                    anim = False
                else:
                    anim = True
                choice = desplay(choice, grid, path, ENTRY, EXIT, mesage,
                                 color_walls, color_42, anim)
            elif choice == 6:
                a = int(input("1:Prim's algorithm 2:Kruskal's algorithm"
                              " 3:dfs algorithm"))
                if a in [1, 2, 3]:
                    algos = ["prims", "kruskal", "dfs"]
                    algo = algos[a-1]
                    choice = 1
                else:
                    choice = 127
            elif choice == 7:
                solve_algo = int(input("1:A* 2:BFS 3:DFS "))
                if solve_algo in [1, 2, 3]:
                    choice = desplay(choice, grid, path, ENTRY, EXIT, mesage,
                                     color_walls, color_42, anim)
                else:
                    solve_algo = 1
                    choice = 127
            elif choice == 8:
                solve = maze.solution
                if solve:
                    for i in solve:
                        sound.play_song("./sound_effect/dog/dog.wav")
                        printer.print_maze(grid, path, i, EXIT, mesage,
                                           color_walls, color_42, anim)
                        time.sleep(0.3)
                    sound.stop_song("./sound_effect/dog/dog.wav")
                    sound.play_song("./sound_effect/dog/eat.wav")
                    time.sleep(1.5)
                    sound.stop_song("./sound_effect/dog/eat.wav")
                    choice = int(input('Choice ?(1-9): '))
            else:
                choice = desplay(choice, grid, path, ENTRY, EXIT, mesage,
                                 color_walls, color_42, anim)
        except (ValueError, KeyboardInterrupt, EOFError):
            choice = 127
            path = None
    if platform.system() == "Windows":
        os.system("clc")
    else:
        os.system("clear")
    print("Thanks, see you soon 🤗")
    sys.exit()
    return (maze)


# main(config["HEIGHT"], config["WIDTH"], config["ENTRY"], config["EXIT"],
#      config["OUTPUT_FILE"], config["PERFECT"], config.get('seed', None),
#      config.get("algorithm", "kruskal"))
