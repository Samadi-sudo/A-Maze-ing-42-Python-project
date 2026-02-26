# mazegen

A reusable Python package for maze generation and solving, built as part of the A-Maze-ing 42 project.

---

## Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

Or from source:

```bash
pip install .
```

---

## Quick Start

```python
from mazegen import MazeGenerator

# Create a 10x10 perfect maze with a fixed seed
gen = MazeGenerator(width=10, height=10, perfect=True, seed=42)

# Generate the maze using DFS (iterative)
gen.dfs_backtracking_iterative(x=0, y=0)

# Solve it using A*
entry = (0, 0)
exit_ = (9, 9)
gen.a_star_solution(entry, exit_)

# Print the solution path
print(gen.solution)
# [(0, 0), (1, 0), (1, 1), ..., (9, 9)]
```

---

## Instantiation & Parameters

```python
MazeGenerator(width, height, perfect=True, seed=None)
```

|Parameter|Type|Required|Description|
|---|---|---|---|
|`width`|`int`|Yes|Number of columns. Must be >= 2.|
|`height`|`int`|Yes|Number of rows. Must be >= 2.|
|`perfect`|`bool`|No|`True` = one solution (default). `False` = multiple solutions.|
|`seed`|`int\|None`|No|Fixed seed for reproducible mazes. `None` = random each time.|

---

## Generation Algorithms

After instantiating `MazeGenerator`, call one of the following to generate the maze. All generators accept a starting cell `(x, y)` (except Kruskal which uses no start point).

### DFS — Depth-First Search (iterative, recommended)

```python
gen.dfs_backtracking_iterative(x=0, y=0)
```

Produces long winding corridors. Stack-safe for large grids. This is the default algorithm.

### DFS — Depth-First Search (recursive)

```python
gen.dfs_backtracking_recursive(x=0, y=0)
```

Same result as iterative DFS but uses Python's call stack. May hit recursion limits on very large mazes.

### Prim's Algorithm

```python
gen.prims_algorithm(x=0, y=0)
```

Grows the maze outward from the start like a spreading tree. Produces more branchy, uniform mazes.

### Kruskal's Algorithm

```python
gen.kruskal_algorithm()
```

Randomly merges disjoint sets of cells. Produces very uniform mazes with no directional bias. No start point needed.

---

## Solving Algorithms

Before calling a solver, **reset the visited state** of every cell, since generation marks cells as visited:

```python
for row in gen.maze.grid:
    for cell in row:
        cell.visited = False
```

Then call one of the solvers:

### A* (recommended)

```python
history = gen.a_star_solution(entry=(0, 0), sorti=(9, 9))
```

Uses the Manhattan distance heuristic. Finds the shortest path efficiently.

### BFS — Breadth-First Search

```python
history = gen.bfs_solution(entry=(0, 0), sorti=(9, 9))
```

Guarantees the shortest path. Explores all directions evenly.

### DFS — Depth-First Search

```python
history = gen.dfs_solution(entry=(0, 0), sorti=(9, 9))
```

Fast but does not guarantee the shortest path.

---

## Accessing the Generated Structure

### `gen.maze.grid`

A 2D list of `Cell` objects: `grid[y][x]`.

Each `Cell` has:

- `cell.walls` — bitmask of remaining walls. Uses `N=1, E=2, S=4, W=8`.
    - Example: `cell.walls & N` is truthy if the north wall is still up.
- `cell.visited` — `True` if the cell was visited during generation/solving.

```python
from mazegen import N, E, S, W

cell = gen.maze.grid[3][5]  # cell at x=5, y=3
has_north_wall = bool(cell.walls & N)
has_east_wall  = bool(cell.walls & E)
```

### `gen.solution`

A list of `(x, y)` tuples representing the path from entry to exit, set after calling any solver.

```python
print(gen.solution)
# [(0, 0), (0, 1), (1, 1), ..., (9, 9)]
```

### `gen.moves`

A list of `(x, y)` tuples recording the order in which cells were carved during generation. Useful for step-by-step animation.

---

## Full Example

```python
from mazegen import MazeGenerator, N, E, S, W

# --- Generate ---
gen = MazeGenerator(width=20, height=20, perfect=True, seed=99)
gen.dfs_backtracking_iterative(0, 0)

# --- Reset visited flags before solving ---
for row in gen.maze.grid:
    for cell in row:
        cell.visited = False

# --- Solve ---
gen.a_star_solution(entry=(0, 0), sorti=(19, 19))
print("Solution length:", len(gen.solution))

# --- Inspect the grid ---
for y in range(gen.height):
    row_str = ""
    for x in range(gen.width):
        cell = gen.maze.grid[y][x]
        row_str += "X" if cell.walls & N else " "
    print(row_str)
```

---

## Wall Bitmask Reference

|Constant|Value|Direction|
|---|---|---|
|`N`|1|North|
|`E`|2|East|
|`S`|4|South|
|`W`|8|West|

A cell with `walls == 15` (i.e. `N|E|S|W`) has all four walls intact (isolated cell). A cell with `walls == 0` has no walls at all (fully open).

---

## Building from Source

```bash
# Install build tools
pip install build

# Build wheel and sdist
python -m build

# Output will be in dist/
# mazegen-1.0.0-py3-none-any.whl
# mazegen-1.0.0.tar.gz
```

---

## Authors

- **abantari** — DFS, Prim's generator, DFS & BFS solvers
- **hrabh** — Kruskal generator, A* solver