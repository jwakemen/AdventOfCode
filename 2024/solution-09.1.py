# imports
import logging
import colorlog
import argparse
import sys

# constants
day = 9
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
    checksum = 0

    logger.info("Starting")
    
    # open the input file
    with open(infile, "r") as f:
        # Read the input file
        line = [int(x) for x in list(f.readline().strip())]
    logger.info(f"input: {line}")
    logger.info(f"length: {len(line)}")
    logger.info(f"files: {len(line)//2 + 1}")
    logger.info(f"free spaces: {(len(line)-1)//2}")

    current_file = 0
    current_index = 0

    last_file = len(line)//2
    last_index = len(line)-1

    block_no = 0

    while current_file <= last_file:
        if line[current_index] == 0:
            current_index += 1
        elif line[last_index] == 0:
            last_index -= 2

        elif current_index % 2 == 0:
            # allocate a block for the current file
            logger.debug(f"file - current_index: {current_index} current_file: {current_file} block: {block_no} remaining: {line[current_index]}")
            checksum += block_no * current_file
            block_no += 1
            line[current_index] -= 1
            if line[current_index] <= 0:
                current_file += 1
        else:
            # allocate block for the last file
            logger.debug(f"free - last_index: {last_index} last_file: {last_file} block: {block_no} remaining: {line[last_index]}")
            checksum += block_no * last_file
            block_no += 1
            line[last_index] -= 1
            if line[last_index] <= 0:
                last_file -= 1
            line[current_index] -= 1

    # finish up and log the total
    logger.info("Complete")
    logger.info(f"Final Checksum: {checksum}")

    # write the output
    final_output = f"{aoc_name} - total: {checksum}\n"
    sys.stdout.write(final_output)
    with open(outfile, "w") as f:
        f.write(final_output)

if __name__ == "__main__":
    main()
