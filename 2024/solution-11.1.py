# imports
import logging
import colorlog
import argparse
import sys
import functools

# constants
day = 11
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

@functools.lru_cache(maxsize=None)
def blink_rock(rock, times):
    logger.debug(f"blinking rock: {rock} {times} times")
    if times == 0:
        return 1
    if rock == 0:
        return blink_rock(1, times - 1)
    if len(str(rock)) % 2 == 0:
        rock_str = str(rock)
        logger.debug(f"rock_str: {rock_str}")
        split_point = len(rock_str) // 2
        # logger.info(f"split_point: {split_point} [{rock_str[:split_point]}][{rock_str[split_point:]}]")
        return blink_rock(int(rock_str[:split_point]), times - 1) + blink_rock(int(rock_str[split_point:]), times - 1)
    return blink_rock(rock * 2024, times - 1)

# main function
def main():
    # setup
    args = get_args()
    logger = setup_logger(args)
    
    # initialize variables
    total = 0
    line = ""

    logger.info("Starting")
    
    # open the input file
    with open(infile, "r") as f:
        # Read the input file
        line = f.readline().strip()
    logger.info(f"input: {line}")

    # split the line into a list of ints
    rocks = [int(x) for x in line.split(" ")]
    logger.info(f"rocks length: {len(rocks)}")
    logger.debug(f"rocks: {rocks}")

    # loop through the blinks
    for rock in rocks:
        total += blink_rock(rock, 25)
        logger.info(f"cache stats: {blink_rock.cache_info()}")

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
