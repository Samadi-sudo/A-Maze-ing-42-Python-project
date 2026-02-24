import sys
from pathlib import Path
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))
from mazegen_package.mazegen import MazeGenerator
from output_gen import output_maze
import printer
import time
import os
import platform
import parsing
import sound
config = parsing.parsing()


def animation(hestory, height, width, entry, exit, anim, maze, mesage):
    template = MazeGenerator(height, width, entry, exit)
    template.p42
    t_maze = template.maze.grid
    if anim:
        for x, y in hestory:
            t_maze[y][x] = maze[y][x]
            printer.print_maze(t_maze, None, entry, exit, None, None, None, False)
            time.sleep(0.3)
    printer.print_maze(maze, None, entry, exit, mesage, None, None, False)

def path_animation(path, grid, entry, exit, anim=True, mesage=""):
    if anim:
        for i in range(len(path)):
            solve = path[:i+1]
            printer.print_maze(grid, solve, entry, exit, mesage, None, None, False)
            time.sleep(0.3)
    else:
        printer.print_maze(grid, path, entry, exit, mesage, None, None, False)
def desplay(choice, grid, path, ENTRY, EXIT, mesage, color_walls, color_42, anim):
    if choice not in [1, 2, 3, 4, 5, 6, 7, 8]:
        printer.print_maze(grid, path, ENTRY, EXIT, mesage, color_walls, color_42, anim)
        print("The option is incorrect 😵")
        choice = int(input('Choice ?(1-9): '))
    elif choice == 9:
        return 9
    else:
        printer.print_maze(grid, path, ENTRY, EXIT, mesage, color_walls, color_42, anim)
        choice = int(input('Choice ?(1-9): '))
    return choice

def main(HEIGHT, WIDTH, ENTRY, EXIT, OUTPUT_FILE, PERFECT, SEED=None, algo="kruskal"):
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
                maze = MazeGenerator(HEIGHT, WIDTH, PERFECT, SEED)
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
                if solve_algo == 2:
                    maze.bfs_solution(ENTRY, EXIT)
                elif solve_algo == 3:
                    maze.dfs_solution(ENTRY, EXIT)
                else:
                    maze.a_star_solution(ENTRY, EXIT)
                animation(hestory, HEIGHT, WIDTH, ENTRY, EXIT, anim, grid,mesage)
                solve = maze.solution
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
                a = int(input("1:Prim's algorithm 2:Kruskal's algorithm 3:dfs algorithm"))
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
                if solve:
                    for i in solve:
                        sound.play_song("dog.wav")
                        printer.print_maze(grid, path, i, EXIT, mesage, color_walls, color_42, anim)
                        time.sleep(0.3)
                    sound.stop_song("dog.wav")
                    sound.play_song("eat.wav")
                    time.sleep(1.5)
                    sound.stop_song("eat.wav")
                    choice = int(input('Choice ?(1-9): '))
            else:
                
                choice = desplay(choice, grid, path, ENTRY, EXIT, mesage,
                                 color_walls, color_42, anim)
        except (ValueError, KeyboardInterrupt, EOFError):
            choice = 127
    if platform.system() == "Windows":
        os.system("clc")
    else:
        os.system("clear")
    print("Thanks, see you soon 🤗")


#main(9,9,(0,0),(8,8),None,None,None,"kru")
main(config["HEIGHT"], config["WIDTH"], config["ENTRY"], config["EXIT"],
     config["OUTPUT_FILE"], config["PERFECT"], config.get('seed', None), config.get("algorithm", "kruskal"))