# imports
import logging
import colorlog
import argparse
import sys

# constants
day = 8
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

def parse_lines(lines):
    antennas = {}
    rows = len(lines)
    cols = len(lines[0])
    for r in range(len(lines)):
        for c in range(len(lines[r])):
            if lines[r][c] != ".":
                if lines[r][c] not in antennas:
                    antennas[lines[r][c]] = set()
                antennas[lines[r][c]].add((r,c))
    logger.debug(f"antennas: {antennas}")
    return antennas, rows, cols

def find_antinodes(antennas, rows, cols):
    antinodes = set()
    for ant_set in antennas.values():
        antinodes = antinodes.union(find_antinodes_by_freq(ant_set, rows, cols))
    return antinodes

def find_antinodes_by_freq(freq_set, rows, cols):
    antinodes = set()
    if len(freq_set) < 2:
        return antinodes
    
    a = freq_set.pop()
    for b in freq_set:
        r_diff = b[0] - a[0]
        c_diff = b[1] - a[1]

        c = (a[0], a[1])
        while c[0] >= 0 and c[0] < rows and c[1] >= 0 and c[1] < cols:
            antinodes.add(c)
            c = (c[0] + r_diff, c[1] + c_diff)
        
        c = (a[0], a[1])
        while c[0] >= 0 and c[0] < rows and c[1] >= 0 and c[1] < cols:
            antinodes.add(c)
            c = (c[0] - r_diff, c[1] - c_diff)
    return antinodes.union(find_antinodes_by_freq(freq_set, rows, cols))

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
        for line in f:
            lines.append(line.strip())
    for line in lines:
        logger.info(f"input: {line}")
    ants, rows, cols = parse_lines(lines)
    
    logger.info(f"rows: {rows} columns: {cols}")
    for ant in ants:
        logger.info(f"antenna: {ant} locations: {ants[ant]}")

    antinodes = find_antinodes(ants, rows, cols)
    logger.info(f"antinodes: {antinodes}")
    total = len(antinodes)

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
