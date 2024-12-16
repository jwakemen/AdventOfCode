# imports
import logging
import colorlog
import argparse
import sys
import re
from statistics import pvariance

# constants
day = 14
part = 2
year = "2024"


max_x = 101
max_y = 103
iterations = 100

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

# main function
def main():
    # setup
    args = get_args()
    logger = setup_logger(args)
    
    # initialize variables
    robots = []

    logger.info("Starting")
    
    # open the input file
    with open(infile, "r") as f:
        # Read the input file
        for line in f:
            matches = re.match(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line)
            x = int(matches.group(1))
            y = int(matches.group(2))
            vx = int(matches.group(3))
            vy = int(matches.group(4))
            robots.append([x, y, vx, vy])
            logger.debug(f"Robot: {x}, {y}, {vx}, {vy}")

    # Find the minimum variances for x and y
    min_x_v = min(range(max_x), key=lambda t: pvariance([(s+t*v) % max_x for (s,_,v,_) in robots]))
    min_y_v = min(range(max_y), key=lambda t: pvariance([(s+t*v) % max_y for (_,s,_,v) in robots]))

    # Find the time that the variance is minimized
    t = min_x_v + ((pow(max_x, -1, max_y) * (min_y_v - min_x_v)) % max_y) * max_x

    # finish up and log the total
    egg = []
    for _ in range(max_y):
        egg.append(["."]*max_x)

    for robot in robots:
        x = (robot[0] + t * robot[2]) % max_x
        y = (robot[1] + t * robot[3]) % max_y
        egg[y][x] = "#"

    for row in egg:
        logger.info("".join(row))

    logger.info("Complete")
    logger.info(f"Time: {t}")

    # write the output
    final_output = f"{aoc_name} - time: {t}\n"
    sys.stdout.write(final_output)
    with open(outfile, "w") as f:
        f.write(final_output)
        for row in egg:
            f.write("".join(row) + "\n")

if __name__ == "__main__":
    main()
