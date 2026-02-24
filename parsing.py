from typing import Dict, Tuple, cast
import sys


class ParsingError(Exception):
    pass


class SurfaceError(ParsingError):
    pass


class CordonateEroor(ParsingError):
    pass


def forbiden_cells(width: int, height: int) -> list:
    x = width // 2
    y = height // 2
    lst_4 = [
        (x-3, y-2),
        (x-3, y-1),
        (x-3, y), (x-2, y), (x-1, y),
        (x - 1, y + 1),
        (x - 1, y + 2)
    ]
    lst_2 = [
        (x + 1, y - 2), (x + 2, y - 2), (x + 3, y - 2),
        (x + 3, y - 1),
        (x + 1, y), (x + 2, y), (x + 3, y),
        (x + 1, y + 1),
        (x + 1, y + 2), (x + 2, y + 2), (x + 3, y + 2)

    ]
    if width > 8 and height > 6:
        return lst_2 + lst_4
    else:
        return []


def check_parsing(config: Dict[str, object]) -> Dict[str, object]:
    try:
        config['WIDTH'], config['HEIGHT'], config['ENTRY']
        config['EXIT'], config['OUTPUT_FILE'], config['PERFECT']
    except (ParsingError, KeyError):
        raise ParsingError("you should provide:"
                           " (WIDTH, HEIGHT, ENTRY, EXIT,"
                           " OUTPUT_FILE, PERFECT)\n"
                           "in config.txt to create the"
                           " maze otherwise i can't help you")
    if cast(int, config['WIDTH']) <= 3 or cast(int, config['HEIGHT']) <= 3:
        raise SurfaceError(
            "can't create a maze with a surface less than '9' (3x3)")

    if cast(int, config['WIDTH']) > 383 or cast(int, config['HEIGHT']) > 201:
        raise SurfaceError("sorry but my screen limit was width:383 and"
                           " height:201 so the max you can do is this"
                           " (still working on a solution to make it even"
                           " bigger lol)")
    if (cast(Tuple[int, int], config['ENTRY'])
       == cast(Tuple[int, int], config['EXIT'])):
        raise CordonateEroor("you are putting the exit exactly where the"
                             " start is don't be stupid it's a maze man")

    if (cast(Tuple[int, int], config['ENTRY'])
       in forbiden_cells(cast(int, config['WIDTH']),
                         cast(int, config['HEIGHT']))
       or cast(Tuple[int, int], config['EXIT'])
       in forbiden_cells(cast(int, config['WIDTH']),
                         cast(int, config['HEIGHT']))):
        raise CordonateEroor("you can't enter any cell that"
                             " are building the logo"
                             " they are forbiden")
    sx, sy = cast(Tuple[int, int], config['ENTRY'])
    ex, ey = cast(Tuple[int, int], config['EXIT'])
    if sx >= cast(int, config['WIDTH']) or sy >= cast(int, config['HEIGHT']):
        raise CordonateEroor(
            "you might want to reconsider where you want to put the ENTRY hhh")
    if ex >= cast(int, config['WIDTH']) or ey >= cast(int, config['HEIGHT']):
        raise CordonateEroor(
            "you might want to reconsider where you want to put the EXIT hhh")
    if len(str(config['OUTPUT_FILE'])) == 0:
        raise ParsingError("not a valid config file name")
    return config


def parsing() -> Dict[str, object]:
    if len(sys.argv) != 2:
        print("ERROR you should do: python3 a_maze_in.py <config_file>")
        sys.exit(1)
    config_path = sys.argv[1]
    config: Dict[str, object] = {}
    try:
        with open(config_path) as file:
            for line_nbr, line in enumerate(file, start=1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if '=' not in line:
                    raise ParsingError(
                        f"Invalid config line {line_nbr}: '{line}'")

                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()

                try:
                    if key in ("WIDTH", "HEIGHT"):
                        if (int(value) <= 0):
                            raise ParsingError
                        config[key] = int(value)
                    elif key in ("seed"):
                        config[key] = int(value)
                    elif key in ("ENTRY", "EXIT"):
                        x, y = value.split(",")
                        if (int(x) < 0 or int(y) < 0):
                            raise ParsingError
                        config[key] = (int(x), int(y))

                    elif key == "PERFECT":
                        if value.lower() not in ("true", "false", '1', '0'):
                            raise ParsingError
                        config[key] = value.lower() == "true" or value == '1'
                    elif key in ("algorithm", "OUTPUT_FILE"):
                        config[key] = value
                    else:
                        raise ParsingError
                except (ParsingError, ValueError):
                    raise ParsingError(
                        f"Invalid value for '{key}'"
                        f" on line {line_nbr}: '{value}'"
                    )
    except FileNotFoundError:
        raise ParsingError("file not found")
    except PermissionError:
        raise ParsingError(
            "you can't read from that file check your permissions bro")
    config = check_parsing(config)
    return config


try:
    config = parsing()
    print(config)
    if cast(int, config['WIDTH']) < 8 and cast(int, config['HEIGHT']) < 6:
        print("the maze is too small to print the 42 logo")
except (SurfaceError, CordonateEroor, ParsingError) as e:
    print(e)
    sys.exit(1)
