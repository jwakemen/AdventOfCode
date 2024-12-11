# imports
import logging
import colorlog
import argparse
import sys

# constants
day = 10
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

# main function
def main():
    # setup
    args = get_args()
    logger = setup_logger(args)
    
    # initialize variables
    total = 0
    map = []

    logger.info("Starting")
    
    # open the input file
    with open(infile, "r") as f:
        # Read the input file
        for line in f:
            heights = [int(x) for x in line.strip()]
            map.append(heights)
    for row in map:
        logger.info(f"input: {row}")

    trails = [[set() for x in range(len(map[0]))] for y in range(len(map))]

    # find the summits
    for x in range(len(map)):
        for y in range(len(map[x])):
            if map[x][y] == 9:
                trails[x][y].add((x,y))
                logger.info(f"found {9} at {x}, {y}")
    for row in trails:
        logger.info(f"trails: {row}")

    # loop through the lower points one height at a time
    for h in range(8, -1, -1):
        logger.info(f"height: {h}")
        for x in range(len(map)):
            for y in range(len(map[x])):
                if map[x][y] == h:
                    logger.debug(f"found {h} at {x}, {y}")
                    for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        i, j = offset
                        if 0 <= x + i < len(map) and 0 <= y + j < len(map[x]):
                            if map[x+i][y+j] == h + 1:
                                trails[x][y] |= trails[x+i][y+j]
        for row in trails:
            logger.info(f"trails after {h}: {row}")

    # count the trails
    for x in range(len(map)):
        for y in range(len(map[x])):
            if map[x][y] == 0:
                logger.info(f"found trailhead at {x}, {y}, count: {len(trails[x][y])}")
                total += len(trails[x][y])

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
