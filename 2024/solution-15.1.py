# imports
import logging
import colorlog
import argparse
import sys

# constants
day = 15
part = 1
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
    logfile_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)-8s %(message)s")
    logfile_handler.setFormatter(logfile_formatter)
    logfile_handler.setLevel(log_level)
    logger.addHandler(logfile_handler)

    return logger

def move_robot(robot, direction):
    logger.debug(f"move_robot: {robot} - {direction}")
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
            space = [item[0] - 1, item[1]]
        case '>':
            space = [item[0], item[1] + 1]
        case 'v':
            space = [item[0] + 1, item[1]]
        case '<':
            space = [item[0], item[1] - 1]

    move_thing(space, direction)
    if map[space[0]][space[1]] == '.':
        map[space[0]][space[1]] = char
        map[item[0]][item[1]] = '.'
        return space
    return item

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
        map.append([c for c in line])

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
    
    for move in moves:
        robot = move_robot(robot, move)

    logger.info(f"---- End ----")
    for row in map:
        logger.info(f"map: {"".join(row)}")

    # caclulate the total
    for row in range(len(map)):
        for col in range(len(map[row])):
            if map[row][col] == 'O':
                total += 100 * row + col

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
