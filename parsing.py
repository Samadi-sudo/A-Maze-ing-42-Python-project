from typing import Dict, Tuple
import sys

def parsing():
    if len(sys.argv) != 2:
        print("ERROR you should do: python3 a_maze_in.py <config_file>")
        sys.exit(1)
    config_path = sys.argv[1]
    config: Dict[str, object] = {}
    with open(config_path) as file:
        print(file.readlines())

parsing()