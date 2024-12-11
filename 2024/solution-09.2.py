# imports
import logging
import colorlog
import argparse
import sys

# constants
day = 9
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

# main function
def main():
    # setup
    args = get_args()
    logger = setup_logger(args)
    logger.info("Starting")
    
    # open the input file
    with open(infile, "r") as f:
        # Read the input file
        line = [int(x) for x in list(f.readline().strip())]
    logger.info(f"input: {line}")
    logger.info(f"length: {len(line)}")
    logger.info(f"files: {len(line)//2 + 1}")
    logger.info(f"free spaces: {(len(line)-1)//2}")

    # initialize the files/free spaces
    spaces = []
    file = 0
    for i in range(len(line)):
        if i % 2 == 0:
            spaces.append((file, line[i]))
            file += 1
        else:
            spaces.append((-1, line[i]))

    compacted = []
    while len(spaces) > 0:
        space = spaces.pop()
        logger.debug(f"spaces: {spaces} compacted: {compacted}")
        logger.debug(f"space: {space} spaces: {len(spaces)} compacted: {len(compacted)}")
        if space[0] == -1:
            compacted.insert(0, space)
        else:
            i = 0
            found = False
            while not found and i < len(spaces):
                if spaces[i][0] == -1 and spaces[i][1] >= space[1]:
                    logger.debug(f"moving to unoccupied space: {space} -> {spaces[i]} at {i}")
                    found = True
                    compacted.insert(0, (-1, space[1]))
                    if spaces[i][1] > space[1]:
                        spaces[i] = (-1, spaces[i][1] - space[1])
                        spaces.insert(i, space)
                        logger.debug(f"result: {spaces[i]} - {spaces[i+1]}")
                    else:
                        spaces[i] = space
                        logger.debug(f"result: {spaces[i]}")
                i += 1
            if not found:
                compacted.insert(0, space)
    logger.debug(f"spaces: {spaces} compacted: {compacted}")                    
    block = 0
    checksum = 0
    for chunk in compacted:
        if chunk[0] != -1:
            for i in range(chunk[1]):
                checksum += chunk[0] * block
                block += 1
        else:
            block += chunk[1]

    logger.info(f"checksum: {checksum}")

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
