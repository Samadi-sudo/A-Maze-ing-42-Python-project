# A-Maze-ing-42-Python-project

_This project has been created as part of the 42 curriculum by [abantari, hrabh]._

## Description:

amazing is a project with the main goal of creating a maze in Python using different algorithms like DFS, Prim's, and Kruskal for maze generation, and also DFS, BFS, and A* for finding the solution between point A and point B.

## Instructions:

All you have to do to run the project is run the command `make run` in the terminal. If any package is missing, you can run `make install` to install them. All packages are mandatory and should be at the root.

## Resources:

To understand the fundamentals, here are the main resources that helped us:
<strong>Prim's algorithm:</strong> https://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm <strong>Backtracking</strong>: https://www.youtube.com/watch?v=ioUl1M77hww 
<strong>Kruskal:</strong> https://weblog.jamisbuck.org/2011/1/3/maze-generation-kruskal-s-algorithm 
<strong>BFS</strong>: https://www.youtube.com/watch?v=V1oZQm1HtVw 
<strong>A*:</strong> [https://www.youtube.com/watch?v=yoVKXBLybZY](https://www.youtube.com/watch?v=yoVKXBLybZY "https://www.youtube.com/watch?v=yoVKXBLybZY") 
**Minilibx:** https://harm-smits.github.io/42docs/libs/minilibx and the documentation left in the wrapper

**We used AI to clarify some questions that the videos or blogs couldn't answer. You could say we used it as a teacher that knows the answer to every question.**

### 1) Complete config structure and format:

[config.txt:]

```bash
WIDTH=20 #(mandatory) can't be float or negative
HEIGHT=20 #(mandatory) can't be float or negative
ENTRY=0,0 #(mandatory) can't be float or negative
EXIT=19,19 #(mandatory) can't be float or negative
OUTPUT_FILE=maze.txt #(mandatory) where the output should be written
PERFECT=0 #(mandatory) defines if the maze will have two or one solution
seed=333   #(optional) negatives and 0 are included
algorithm= dfs #(optional) can use (prims, kruskal) instead
display_mode = Mlx #(optional) can use (ascii) instead
```

### 2) Maze generation algorithm chosen:

Primary chosen algorithm (for default runs): DFS:
**We chose DFS because:**
- Very simple and intuitive to implement.
- Produces long, deep corridors that are visually clean and easy to debug.
- Perfect for educational purposes since it clearly demonstrates stack-based backtracking.
- <u>And because it was the first one we started with, so obviously it's the default one.</u>

Secondary ones are: Prim's and Kruskal

- For learning purposes.

### 3) What part of your code is reusable, and how:

The entirety of the code is reusable. The `sound.py` file contains functions like `python play_song()` and `stop_song()` that only need the path of the song file to work and prevent the file from being opened twice. The `draw_maze()` function takes literally any maze that uses N, E, S, W = 1, 2, 4, 8 for its walls.

Of course the **package** works independently, as well as the **ascii_printer**.

### 4) Team & project management

- **Team members & roles**
    
    - `abantari`: Done the Mlx part and focused on DFS and Prim's generators, and for solutions used DFS and BFS.
        
    - `hrabh`: Done the ASCII part and focused on the Kruskal generator, and for the solution used A*.
        
- **Planning & evolution**
    
    - Initial plan: implement generator + simple visualizer → add solvers → tests.
        
    - Evolved: we added characters into the maze and audio to feel like a little game, and made the choice of having two display modes instead of just one.
        
    - It took us some time but in the end we delivered :)
        
- **What worked well**
    
    - Modular design (easy to add algorithms).
        
    - Minilibx was a cool library (after getting the hang of it), even though the documentation for the Python wheel wasn't very intuitive for a first-time user (so I made my own documentation [link below]).
        
    - Caught edge cases early since everything was well structured.
        
    - Multiple algorithm choices and display modes.
        
- **What could be improved**
    
    - More thorough performance benchmarks (time/memory for large grids).
        
    - Code readability and structure.
        

### 5) Tools used

- Git + GitHub
    
- Python 3.10 (project code)
    
- Make (convenience commands)
    
- `minilibx` wrapper for native visualization.
    
- Excalidraw to manage ideas and explain concepts to each other.