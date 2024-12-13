# imports
import logging
import colorlog
import argparse
import sys
import numpy as np
from collections import namedtuple
import re

# constants
day = 13
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

# data structures
Machine = namedtuple("Machine", ["A", "B", "P"])
Button = namedtuple("Button", ["x", "y"])
Prize = namedtuple("Prize", ["x", "y"])

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

# main function
def main():
    # setup
    args = get_args()
    logger = setup_logger(args)
    
    # initialize variables
    total = 0
    machines = []

    logger.info("Starting")
    
    # open the input file
    with open(infile, "r") as f:
        # Read the input file
        a_x, a_y, b_x, b_y, p_x, p_y = 0, 0, 0, 0, 0, 0
        for line in f:
            line = line.strip()
            logger.debug(f"line: {line}")

            if re.match(r"Button A: X\+\d+, Y\+\d+", line):
                matches = re.match(r"Button A: X\+(\d+), Y\+(\d+)", line)
                a_x = int(matches.group(1))
                a_y = int(matches.group(2))
            if re.match(r"Button B: X\+\d+, Y\+\d+", line):
                matches = re.match(r"Button B: X\+(\d+), Y\+(\d+)", line)
                b_x = int(matches.group(1))
                b_y = int(matches.group(2))
            if re.match(r"Prize: X=\d+, Y=\d+", line):
                matches = re.match(r"Prize: X=(\d+), Y=(\d+)", line)
                p_x = int(matches.group(1)) + 10000000000000
                p_y = int(matches.group(2)) + 10000000000000
            if a_x and a_y and b_x and b_y and p_x and p_y:
                m = Machine(Button(a_x, a_y), Button(b_x, b_y), Prize(p_x, p_y))
                logger.debug(f"machine: {m}")
                machines.append(m)
                a_x, a_y, b_x, b_y, p_x, p_y = 0, 0, 0, 0, 0, 0

    # log the input
    for machine in machines:
        logger.debug(f"machine: {machine}")

    # process the machines
    for machine in machines:
        logger.debug(f"machine: {machine}")
        c = np.linalg.solve([[machine.A.x, machine.B.x], [machine.A.y, machine.B.y]], [machine.P.x, machine.P.y])
        logger.debug(f"c: {c}")
        a, b = [round(x) for x in c]
        if a >= 0 and b >= 0 and machine.A.x * a + machine.B.x * b == machine.P.x and machine.A.y * a + machine.B.y * b == machine.P.y:
            logger.info(f"a: {a}, b: {b} cost: {3 * a + b} on target: {machine.A.x * a + machine.B.x * b == machine.P.x and machine.A.y * a + machine.B.y * b == machine.P.y}")
            c_total = 3 * a + b
            total += c_total

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
