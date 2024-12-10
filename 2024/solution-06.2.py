# imports
import logging
import colorlog
import argparse
import sys

# constants
day = 6
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

def find_start(lines):
    for row in range(len(lines)):
        if '^' in lines[row]:
            logger.debug(lines[row])
            col = lines[row].index('^')
            return row, col

def navigate(lines, row, col):
    loop = False
    dir = lines[row][col]
    visited = [[set() for _ in range(len(lines[row]))] for row in range(len(lines))]
    while not loop and row >= 0 and row < len(lines) and col >= 0 and col < len(lines[row]):
        if dir in visited[row][col]:
            loop = True
        else:
            visited[row][col].add(dir)

            match dir:
                case '^':
                    if row > 0 and lines[row-1][col] == '#':
                        dir = '>'
                    else:
                        row -= 1
                case '>':
                    if col < len(lines[row]) - 1 and lines[row][col+1] == '#':
                        dir = 'v'
                    else:
                        col += 1
                case 'v':
                    if row < len(lines) - 1 and lines[row+1][col] == '#':
                        dir = '<'
                    else:
                        row += 1
                case '<':
                    if col > 0 and lines[row][col-1] == '#':
                        dir = '^'
                    else:
                        col -= 1
    return loop

# main function
def main():
    # setup
    args = get_args()
    logger = setup_logger(args)
    
    # initialize variables
    total = 0
    lines = []

    logger.info("Starting")
    
    # open the input file
    with open(infile, "r") as f:
        # Read the input file
        for line in f:
            lines.append(list(line.strip()))
    logger.debug(f"input: {lines}")

    row, col = find_start(lines)
    logger.info(f"start position is (row: {row}, col: {col})")
    for o_row in range(len(lines)):
        for o_col in range(len(lines[o_row])):
            logger.debug(f"row: {o_row}, col: {o_col}, char: {lines[o_row][o_col]}")
            if lines[o_row][o_col] == '.':
                lines[o_row][o_col] = '#'
                if navigate(lines, row, col):
                    total += 1
                    logger.debug(f"loop found total: {total}")
                lines[o_row][o_col] = '.'
            logger.debug(f"loops found total: {total}")

    logger.debug(f"lines: {lines}")

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
