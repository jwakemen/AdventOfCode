# imports
import logging
import colorlog
import argparse
import sys
from functools import cache

# constants
day = 19
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

# data
towels = []
patterns = []

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

def check(pat, towels):
    logger.debug(f"check({pat})")
    @cache
    def count(pat):
        return sum(count(pat.removeprefix(t)) for t in towels if pat.startswith(t)) if pat else 1
    
    c = count(pat)
    logger.debug(f"stats: {count.cache_info()}")
    logger.debug(f"count: {c}")
    return c

# main function
def main():
    # setup
    args = get_args()
    logger = setup_logger(args)
    
    # initialize variables
    total = 0
    towels = []

    logger.info("Starting")
    
    # open the input file
    f = open(infile, "r")
    # Read the input file
    line = f.readline()
    towels += [p.strip() for p in line.strip().split(',')]
    for line in f:
        if line == "\n":
            break

    patterns = [line.strip() for line in f]

    # log the input
    logger.info(f"number of towels: {len(towels)}")
    logger.info(f"number of patterns: {len(patterns)}")
    logger.info(f"towels: {towels}")
    logger.info(f"patterns: {patterns}")

    for pattern in patterns:
        c = check(pattern, towels)
        logger.info(f"Pattern: {pattern} - Count: {c}")
        total += c

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
