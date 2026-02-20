import a_star
import kruskal
import printer
import time
import minitouls
import prim
import os
import platform
import shutil


WIDTH = 10
HEIGHT = 10
ENTRY = (0, 0)
EXIT = (9, 9)
OUTPUT_FILE = 'maze.txt'
PERFECT = False
SEED = 5



def song(mode):
    if platform.system() == "Linux":
        if mode is True:
            if shutil.which("aplay"):
                os.system("aplay dog.wav &")
            elif shutil.which('cvlc'):
                os.system("while true; do cvlc --play-and-exit dog.wav ; "
                          "done &")
            elif shutil.which('paplay'):
                os.system("while true; do paplay dog.wav ; done &")
        else:
            if shutil.which("aplay"):
                os.system("pkill -f aplay")
            if shutil.which('cvlc'):
                os.system("pkill -f cvlc")
            elif shutil.which('paplay'):
                os.system("pkill -f paplay")

def main(HEIGHT, WIDTH, ENTRY, EXIT, OUTPUT_FILE,
         PERFECT, SEED=None, algo=kruskal.generator):

    if WIDTH > 200 or HEIGHT > 200:
        print("The width or height is too large "
              "(max width is 200, max height is 200 )")
        exit(1)
    choice = 1
    color = 0
    animation = True
    error, maze = algo(HEIGHT, WIDTH, ENTRY, EXIT, PERFECT, SEED, False)
    solve = a_star.solve(maze[ENTRY[1]][ENTRY[0]], maze[EXIT[1]][EXIT[0]], maze)
    while choice != 8:
        try:
            if choice == 1:  # generate a new maze
                error, maze = algo(HEIGHT, WIDTH, ENTRY, EXIT,
                                   PERFECT, SEED, animation)
                solve = a_star.solve(maze[ENTRY[1]][ENTRY[0]],
                                     maze[EXIT[1]][EXIT[0]], maze)
                if solve:
                    minitouls.ft_output(maze, OUTPUT_FILE, solve, ENTRY, EXIT)
                choice = int(input('Choice ?(1-7):'))
            elif choice == 2:  # show path
                if solve and animation is True:
                    for i in range(len(solve)):
                        path = solve[:i+1]
                        if error:
                            print(error)
                        printer.print_maze(maze, path, ENTRY, EXIT, error, None,
                                           None, animation)
                        time.sleep(0.3)
                    choice = int(input('Choice ?(1-7): '))
                    if choice == 2:
                        printer.print_maze(maze, None, ENTRY, EXIT, error, None,
                                           None, animation)
                        choice = int(input('Choice ?(1-7): '))
                elif solve and animation is False:
                    printer.print_maze(maze, solve, ENTRY, EXIT, error, None,
                                       None, animation)
                    choice = int(input('Choice ?(1-7): '))
                    if choice == 2:
                        printer.print_maze(maze, None, ENTRY, EXIT, error, None,
                                           None, animation)
                        choice = int(input('Choice ?(1-7): '))
                else:   # No path
                    print("Not solve of this maze !")
                    printer.print_maze(maze, None, ENTRY, EXIT, error, None,
                                       None, animation)
                    choice = int(input('Choice ?(1-7): '))
            elif choice == 3:
                color = 127
                while color == 127:
                    color = int(input("0:🟩 1:🟫 2:🟥 3:🟨 4:🟧 5:🟪 "))
                    if color not in [0, 1, 2, 3, 4, 5]:
                        printer.print_maze(maze, None, ENTRY, EXIT, error, None,
                                           None, animation)
                        print("The color is incorrect")
                        color = 127
                    else:
                        printer.print_maze(maze, None, ENTRY, EXIT, error, color,
                                           None, animation)
                        choice = int(input('Choice ?(1-7): '))
                        break
            elif choice == 4:
                color_42 = None
                while color_42 is None:
                    color_42 = int(input("0:🔥 1:⛔️ 2:❌ 3:🐱 "))
                    if color_42 not in [0, 1, 2, 3]:
                        printer.print_maze(maze, None, ENTRY, EXIT, error, None,
                                           None, animation)
                        print("The color is incorrect")
                        color_42 = None
                    else:
                        printer.print_maze(maze, None, ENTRY, EXIT, error, None,
                                           color_42, animation)
                        choice = int(input('Choice ?(1-7): '))
                        break
            elif choice == 5:
                if animation:
                    animation = False
                else:
                    animation = True
                printer.print_maze(maze, None, ENTRY, EXIT, error, None,
                                   None, animation)
                choice = int(input('Choice ?(1-7): '))
            elif choice == 6:
                printer.print_maze(maze, None, ENTRY, EXIT, error, None,
                                   None, animation)
                print("1:Prim's algorithm 2:Kruskal's algorithm")
                
                a = int(input('Choice ?(1-7): '))
                if a == 1:
                    algo = prim.generator
                    choice = 1
                elif a == 2:
                    algo = kruskal.generator
                    choice = 1
                else:
                    choice = 127
            elif choice == 7:
                if solve and animation is True:
                    song(True)
                    for i in (solve):
                        if error:
                            print(error)
                        printer.print_maze(maze, None,  (i.x, i.y), EXIT, error, None,
                                           None, animation)
                        time.sleep(0.3)
                    song(False)
                    choice = int(input('Choice ?(1-7): '))

            else:
                printer.print_maze(maze, None, ENTRY, EXIT, error, None,
                                   None, animation)
                print("The option is incorrect 😵")
                song(False)
                choice = int(input('Choice ?(1-7): '))
        except (ValueError, KeyboardInterrupt, EOFError):    #hena mazal 3andi lmachakil 
            choice = 127
    if platform.system() == "Windows":
        os.system("clc")
    else:
        os.system("clear")
    print("Thanks, see you soon 🤗")
    song(False)


# main(HEIGHT, WIDTH, ENTRY, EXIT, OUTPUT_FILE, PERFECT,SEED)

#        choice = input('Choice ?(1-7): ')
#        if choice in ['0', '1', '2', '3', '4', '5', '7', '7', '8', '9']:
#            choice = int(choice)
#        else:
#            choice = 12

# ma   zal bzaf deyal l7wayj khasni n9adhom ila 3tayto ikhtar color o dar Entrer blama ikhtar 4aytkracha ila dakhel value not incorrect 4adir ValueError

# pr   inter.print_maze(maze,None ,ENTRY, EXIT)
# for item in solv:
#     print(f"({item.x},{item.y})"




# chof raha catcracha mn wra ma kadir 2 mn be3dha kadir 5
