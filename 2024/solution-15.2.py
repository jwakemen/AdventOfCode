# imports
import logging
import colorlog
import argparse
import sys
from warehouse_visualizer import WarehouseVisualizer

# constants
day = 15
part = 2
year = "2024"

# script description
aoc_name = f"Advent of Code {year:04} - Day {day:02} - Part {part:01}"

# file paths
infile  = f"inputs/input-{day:02}.txt"
outfile = f"outputs/output-{day:02}.{part:01}.txt"
logfile = f"logs/solution-{day:02}.{part:01}.log"

# logger
logger = logging.getLogger(aoc_name)
logger.setLevel(logging.DEBUG)

# map
map = []

# functions
def get_args():
    arg_parser = argparse.ArgumentParser(description=aoc_name, epilog=f"see: https://adventofcode.com/{year:04}/day/{day}")
    arg_parser.add_argument("-l", "--log", help="set file log level [default: %(default)s]", default="INFO", metavar="LEVEL")
    arg_parser.add_argument("-c", "--con", help="set console log level [default: %(default)s]", default="WARNING", metavar="LEVEL")
    return arg_parser.parse_args()

def setup_logger(args):
    log_level = getattr(logging, args.log.upper(), logging.DEBUG)
    con_level = getattr(logging, args.con.upper(), logging.WARNING)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_formatter = colorlog.ColoredFormatter("%(asctime)s %(name)s %(log_color)s%(levelname)-8s%(reset)s %(message)s")
    stderr_handler.setFormatter(stderr_formatter)
    stderr_handler.setLevel(con_level)
    logger.addHandler(stderr_handler)

    logfile_handler = logging.FileHandler(logfile, mode="w")
    # logfile_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)-8s %(message)s")
    # logfile_handler.setFormatter(logfile_formatter)
    logfile_handler.setLevel(log_level)
    logger.addHandler(logfile_handler)

    return logger

def parse_line(line):
    parsed = []
    for char in line:
        match char:
            case '#':
                parsed += [char, char]
            case '.':
                parsed += [char, char]
            case '@':
                parsed += ['@', '.']
            case 'O':
                parsed += ['[', ']']
    return parsed

def move_robot(robot, direction):
    logger.debug(f"move_robot: {robot} - {direction}")
    if is_movable(robot, direction):
        robot = move_thing(robot, direction)
    return robot

def move_thing(item, direction):
    logger.debug(f"move_thing: {item} - {direction}")
    char = map[item[0]][item[1]]
    logger.debug(f"move: {item[0]}, {item[1]} - {char}")
    if char == '.' or char == '#':
        return item
    
    match direction:
        case '^':
            if char == '[':
                move_thing([item[0] - 1, item[1]], direction)
                move_thing([item[0] - 1, item[1] + 1], direction)
                map[item[0] - 1][item[1]] = '['
                map[item[0] - 1][item[1] + 1] = ']'
                map[item[0]][item[1]] = '.'
                map[item[0]][item[1] + 1] = '.'
            elif char == ']':
                move_thing([item[0] - 1, item[1] - 1], direction)
                move_thing([item[0] - 1, item[1]], direction)
                map[item[0] - 1][item[1] - 1] = '['
                map[item[0] - 1][item[1]] = ']'
                map[item[0]][item[1] - 1] = '.'
                map[item[0]][item[1]] = '.'
            else:
                move_thing([item[0] - 1, item[1]], direction)
                map[item[0] - 1][item[1]] = char
                map[item[0]][item[1]] = '.'
            return [item[0] - 1, item[1]]
        case '>':
            move_thing([item[0], item[1] + 1], direction)
            map[item[0]][item[1] + 1] = char
            map[item[0]][item[1]] = '.'
            return [item[0], item[1] + 1]
        case 'v':
            if char == '[':
                move_thing([item[0] + 1, item[1]], direction)
                move_thing([item[0] + 1, item[1] + 1], direction)
                map[item[0] + 1][item[1]] = '['
                map[item[0] + 1][item[1] + 1] = ']'
                map[item[0]][item[1]] = '.'
                map[item[0]][item[1] + 1] = '.'
            elif char == ']':
                move_thing([item[0] + 1, item[1] - 1], direction)
                move_thing([item[0] + 1, item[1]], direction)
                map[item[0] + 1][item[1] - 1] = '['
                map[item[0] + 1][item[1]] = ']'
                map[item[0]][item[1] - 1] = '.'
                map[item[0]][item[1]] = '.'
            else:
                move_thing([item[0] + 1, item[1]], direction)
                map[item[0] + 1][item[1]] = char
                map[item[0]][item[1]] = '.'
            return [item[0] + 1, item[1]]
        case '<':
            move_thing([item[0], item[1] - 1], direction)
            map[item[0]][item[1] - 1] = char
            map[item[0]][item[1]] = '.'
            return [item[0], item[1] - 1]

def is_movable(item, direction):
    char = map[item[0]][item[1]]
    if char == '#':
        return False
    if char == '.':
        return True

    if direction == '<':
        if map[item[0]][item[1] - 1] == '.':
            return True
        return is_movable([item[0], item[1] - 1], direction)
    elif direction == '>':
        if map[item[0]][item[1] + 1] == '.':
            return True
        return is_movable([item[0], item[1] + 1], direction)
    elif direction == '^':
        if char == '[':
            if map[item[0] - 1][item[1]] == '.' and map[item[0] - 1][item[1] + 1] == '.':
                return True
            return is_movable([item[0] - 1, item[1]], direction) and is_movable([item[0] - 1, item[1] + 1], direction)
        elif char == ']':
            if map[item[0] - 1][item[1] - 1] == '.' and map[item[0] - 1][item[1]] == '.':
                return True
            return is_movable([item[0] - 1, item[1] - 1], direction) and is_movable([item[0] - 1, item[1]], direction)
        else:
            if map[item[0] - 1][item[1]] == '.':
                return True
            return is_movable([item[0] - 1, item[1]], direction)
    else:
        if char == '[':
            if map[item[0] + 1][item[1]] == '.' and map[item[0] + 1][item[1] + 1] == '.':
                return True
            return is_movable([item[0] + 1, item[1]], direction) and is_movable([item[0] + 1, item[1] + 1], direction)
        elif char == ']':
            if map[item[0] + 1][item[1] - 1] == '.' and map[item[0] + 1][item[1]] == '.':
                return True
            return is_movable([item[0] + 1, item[1] - 1], direction) and is_movable([item[0] + 1, item[1]], direction)
        else:
            if map[item[0] + 1][item[1]] == '.':
                return True
            return is_movable([item[0] + 1, item[1]], direction)

# main function
def main():
    # setup
    args = get_args()
    logger = setup_logger(args)
    
    # initialize variables
    total = 0
    moves = ""

    logger.info("Starting")
    
    # open the input file
    f = open(infile, "r")
    for line in f:
        line = line.strip()
        if line == "":
            break
        parsed = parse_line(line)
        map.append(parsed)

    for line in f:
        moves += line.strip()

    for row in map:
        logger.info(f"map: {"".join(row)}")

    logger.info(f"moves: {moves}")

    # find the robot
    robot = [-1, -1]
    for row in range(len(map)):
        for col in range(len(map[row])):
            if map[row][col] == '@':
                robot = [row, col]

    visualizer = WarehouseVisualizer()
    visualizer.show_frame(map)
    for move in moves:
        robot = move_robot(robot, move)
        visualizer.show_frame(map)

    logger.info(f"---- End ----")
    for row in map:
        logger.info(f"map: {"".join(row)}")

    # caclulate the total
    for row in range(len(map)):
        for col in range(len(map[row])):
            if map[row][col] == '[':
                gps = 100 * row + col
                total += gps
                logger.info(f"row: {row}, col: {col} - gps: {gps}, total: {total}")
                
    # finish up and log the total
    logger.info("Complete")
    logger.info(f"Total: {total}")

    # write the output
    final_output = f"{aoc_name} - total: {total}\n"
    sys.stdout.write(final_output)
    with open(outfile, "w") as f:
        f.write(final_output)

if __name__ == "__main__":
    main()
