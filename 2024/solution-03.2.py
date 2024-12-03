# imports
import re
import logging
import colorlog
import argparse
import sys

# constants
year = "2024"
day = "03"
part = "2"

# script description
aoc_name = f"Advent of Code {year} - Day {day} - Part {part}"

# file paths
infile  = f"inputs/input-{day}.txt"
outfile = f"outputs/output-{day}.{part}.txt"
logfile = f"logs/solution-{day}.{part}.log"

# logger
logger = logging.getLogger(aoc_name)
logger.setLevel(logging.DEBUG)

# functions
def find_matches(line):
    # find the matches in the line
    regex = re.compile(r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)")
    matches = regex.findall(line)
    logger.debug(f"Matches: {matches}")
    return matches

def calculate(matches):
    enabled = True
    acc = 0
    for m in matches:
        logger.debug(f"Match: {m}")
        match m:
            case "do()":
                enabled = True
            case "don't()":
                enabled = False
            case _:
                if enabled:
                    l,r = re.match(r"mul\((\d{1,3}),(\d{1,3})\)", m).groups()
                    acc += int(l) * int(r)
                    logger.debug(f"l: {l} r: {r} acc: {acc}")
    return acc

def main():
    # setup
    arg_parser = argparse.ArgumentParser(description=aoc_name)
    arg_parser.add_argument("-l", "--log", help="set file log level [default: %(default)s]", default="DEBUG", metavar="LEVEL")
    arg_parser.add_argument("-c", "--con", help="set console log level [default: %(default)s]", default="WARNING", metavar="LEVEL")
    args = arg_parser.parse_args()

    log_level = getattr(logging, args.log.upper(), logging.DEBUG)
    console_level = getattr(logging, args.console.upper(), logging.WARNING)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_formatter = colorlog.ColoredFormatter("%(asctime)s %(name)s %(log_color)s%(levelname)-8s%(reset)s %(message)s")
    stderr_handler.setFormatter(stderr_formatter)
    stderr_handler.setLevel(console_level)
    logger.addHandler(stderr_handler)

    logfile_handler = logging.FileHandler(logfile, mode="w")
    logfile_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)-8s %(message)s")
    logfile_handler.setFormatter(logfile_formatter)
    logfile_handler.setLevel(log_level)
    logger.addHandler(logfile_handler)
    
    logger.info("Starting")

    # initialize variables
    total = 0
    lines = ""

    with open(infile, "r") as f:
        # Read the input file
        for line in f:
            lines += line

    values = find_matches(lines)
    total += calculate(values)

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
