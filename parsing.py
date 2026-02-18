from typing import Dict, Tuple
import sys

# def check_erors():
#         config = parsing()

def parsing() -> Dict[str, object]:
    if len(sys.argv) != 2:
        print("ERROR you should do: python3 a_maze_in.py <config_file>")
        sys.exit(1)
    config_path = sys.argv[1]
    config: Dict[str, object] = {}
    with open(config_path) as file:
        for line_nbr, line in enumerate(file, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if '=' not in line:
                raise ValueError(f"Invalid config line {line_nbr}: '{line}'")

            key, value = line.split('=', 1)
            key= key.strip()
            value = value.strip()

            try:
                if key in ("WIDTH", "HEIGHT", "seed"):
                    if (int(value) <= 0):
                        raise ValueError
                    config[key] = int(value)

                elif key in ("ENTRY", "EXIT"):
                    x, y = value.split(",")
                    config[key] = (int(x), int(y))

                elif key == "PERFECT":
                    if value not in ("True", "False", "true", "false", '1', '0'):
                        raise ValueError
                    config[key] = value == "True" or value == "true" or value == '1'
                elif key in ("algorithm", "OUTPUT_FILE") :
                    config[key] = value
                else:
                    raise ValueError
            except ValueError:
                raise ValueError(
                    f"Invalid value for '{key}' on line {line_nbr}: '{value}'"
                )

    return config


print(parsing())