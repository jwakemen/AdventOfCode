# imports
import logging
import colorlog
import argparse
import sys
import re
import functools

# constants
day = 5
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

def check_update(update, rules):
    def page_order(p1, p2):
        if [p1, p2] in rules:
            return -1
        elif [p2, p1] in rules:
            return 1
        else:
            return 0

    sorted_update = sorted(update, key=functools.cmp_to_key(page_order))
    logger.info(f"Checking update: {update}")
    logger.info(f"Sorted update:   {sorted_update}")

    if update == sorted_update:
        logger.info(f"Update {update} is valid")
        return 0
    
    logger.info(f"Update {update} is not valid")
    return int(sorted_update[len(sorted_update) // 2])

# main function
def main():
    # setup
    args = get_args()
    logger = setup_logger(args)
    
    # initialize variables
    total = 0
    lines = ""
    rules = []
    updates = []

    logger.info("Starting")

    rule_re = re.compile(r"(\d+)\|(\d+)")
    update_re = re.compile(r"^(?:(\d+),?)+$")
    
    # open the input file
    with open(infile, "r") as f:
        # Read the input file
        for line in f:
            line = line.strip()
            logger.debug(f"Read line: {line}")
            if rule_re.match(line):
                logger.debug(f"Found rule: {line} - match: {rule_re.match(line).groups()}")
                rule = [int(x) for x in rule_re.match(line).groups()]
                logger.debug(f"Rule: {rule}")
                rules.append(rule)
            elif update_re.match(line):
                logger.debug(f"Found update: {line} - match: {update_re.match(line).groups()}")
                update = [int(x) for x in line.split(",")]
                logger.debug(f"Update: {update}")
                updates.append(update)
            else:
                logger.debug(f"No match: {line}")

    logger.debug(f"Rules: {rules}")
    logger.debug(f"Updates: {updates}")
    
    # check the updates
    for update in updates:
        total += check_update(update, rules)

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
