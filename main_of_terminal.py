import a_star
import kruskal
import printer
import time
import random


WIDTH = 8
HEIGHT = 8
ENTRY = (0, 1)
EXIT = (6, 2)
OUTPUT_FILE  = 'maze.txt'
PERFECT = True
SEED = None


choice = 1
color = 0
while choice != 5:
    if choice == 1:  # generate a new maze
        error, maze = kruskal.generator(HEIGHT, WIDTH, ENTRY, EXIT, PERFECT, SEED)
        solve = a_star.solve(maze[ENTRY[1]][ENTRY[0]], maze[EXIT[1]][EXIT[0]], maze)
        if solve:
            kruskal.ft_output(maze, 'hamza', solve, ENTRY, EXIT)
        choice = int(input('Choice ?(1-4):'))
    elif choice == 2:  # show path
        if solve:
            for i in range(len(solve)):
                path = solve[:i+1]
                if error:
                    print(error)
                printer.print_maze(maze, path, ENTRY, EXIT, error, None, None)
                time.sleep(0.3)
            choice = int(input('Choice ?(1-4): '))
            if choice == 2:
                printer.print_maze(maze, None, ENTRY, EXIT, error, None, None)
                choice = int(input('Choice ?(1-4): '))

        else:   # No path
            print("Not solve of this maze !")
            printer.print_maze(maze, None, ENTRY, EXIT, error, None, None)
            choice = int(input('Choice ?(1-4): '))
    elif choice == 3:
        color = None
        while color is None:
            color = int(input("0:🟩 1:🟫 2:🟥 3:🟨 4:🟧 5:🟪 "))
            if color not in [0,1,2,3,4,5]:
                printer.print_maze(maze, None, ENTRY, EXIT, error, None, None)
                print("The color is incorrect")
                color = None
            else:
                printer.print_maze(maze, None, ENTRY, EXIT, error, color, None)
                choice = int(input('Choice ?(1-4): '))
                break
    elif choice == 4:
        color = None
        while color is None:
            color = int(input("0:🔥 1:⛔️ 2:❌ 3:🐱 "))
            if color not in [0, 1, 2, 3]:
                printer.print_maze(maze, None, ENTRY, EXIT, error, None, None)
                print("The color is incorrect")
                color = None
            else:
                printer.print_maze(maze, None, ENTRY, EXIT, error, None, color)
                choice = int(input('Choice ?(1-4): '))
                break
# mazal bzaf deyal l7wayj khasni n9adhom ila 3tayto ikhtar color o dar Entrer blama ikhtar 4aytkracha ila dakhel value not incorrect 4adir ValueError

# printer.print_maze(maze,None ,ENTRY, EXIT)
# for item in solv:
#     print(f"({item.x},{item.y})")


