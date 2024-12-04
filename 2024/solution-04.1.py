# imports
import logging
import colorlog
import argparse
import sys
import numpy as np

# constants
day = 4
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

dirs = [(-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)]

def find_xmas(lines, start_row, start_col, direction):
    row, col = start_row, start_col
    logger.debug(f"Checking: {row}, {col}, {direction}")
    
    # check for space
    if row + (3 * direction[0]) < 0 or row + (3 * direction[0]) >= len(lines) or col + (3 * direction[1]) < 0 or col + (3 * direction[1]) >= len(lines[0]):
        logger.debug(f"Out of bounds: {row}, {col}, {direction}")
        return 0
    
    # check for XMAS
    c1 = lines[row][col]
    c2 = lines[row + direction[0]][col + direction[1]]
    c3 = lines[row + (2 * direction[0])][col + (2 * direction[1])]
    c4 = lines[row + (3 * direction[0])][col + (3 * direction[1])]
    if c1 + c2 + c3 + c4 != "XMAS":
        logger.debug(f"Not XMAS: {row}, {col}, {direction} - {c1 + c2 + c3 + c4}")
        return 0
    logger.info(f"Found XMAS: {start_row}, {start_col}, {direction} - {c1 + c2 + c3 + c4}")
    return 1

def count_xmas_from_point(lines, row, col):
    count = 0
    logger.debug(f"Checking: {row}, {col} - Char: {lines[row][col]}")
    if lines[row][col] == "X":
        logger.info(f"Found X: {row}, {col} - Checking directions")       
        for direction in dirs:
            count += find_xmas(lines, row, col, direction)

    return count

def count_xmas(lines):
    count = 0
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            count += count_xmas_from_point(lines, row, col)
    return count

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
        lines = np.loadtxt(f, dtype=str)
    logger.debug(f"input: {lines}")

    logger.info(f"Starting check - lines: {len(lines)} - cols: {len(lines[0])}")
    total = count_xmas(lines)

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
