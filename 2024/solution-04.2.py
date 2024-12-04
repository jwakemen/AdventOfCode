# imports
import logging
import colorlog
import argparse
import sys
import numpy as np

# constants
day = 4
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
    arg_parser.add_argument("-l", "--log", help="set file log level [default: %(default)s]", default="DEBUG", metavar="LEVEL")
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

def find_xmas(lines, center_row, center_col):
    logger.debug(f"Checking: {center_row}, {center_col}")
    
    # check for space
    if center_row - 1 < 0 or center_row + 1 >= len(lines) or center_col - 1 < 0 or center_col + 1 >= len(lines[0]):
        logger.debug(f"Out of bounds: {center_row}, {center_col}")
        return 0
    
    # check for crossed MAS
    d1 = lines[center_row - 1][center_col - 1] + lines[center_row][center_col] + lines[center_row + 1][center_col + 1]
    d2 = lines[center_row - 1][center_col + 1] + lines[center_row][center_col] + lines[center_row + 1][center_col - 1]
    logger.debug(f"Diagonals: {center_row}, {center_col} - {d1} - {d2}")
    if (d1 != "MAS" and d1 != "SAM") or (d2 != "MAS" and d2 != "SAM"):
        logger.debug(f"Not X-MAS: {center_row}, {center_col}")
        return 0
    logger.debug(f"Found X-MAS: {center_row}, {center_col}")
    return 1
    
def count_xmas(lines):
    count = 0
    for row in range(1, len(lines) - 1):
        for col in range(1, len(lines[row]) - 1):
            if lines[row][col] == "A":
                count += find_xmas(lines, row, col)
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
