# imports
import logging
import colorlog
import argparse
import sys

# constants
day = "12"
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
    
    # initialize variables
    total = 0
    lines = []

    logger.info("Starting")
    
    # open the input file
    with open(infile, "r") as f:
        # Read the input file
        for line in f:
            lines.append(line.strip())

    # process the input into lists
    map = ['.' for _ in range(len(lines[0]) + 2)]
    map = [map] + [['.'] + [char for char in line] + ['.'] for line in lines] + [map]

    # process the map
    for row in range(1, len(map) - 1):
        for col in range(1, len(map[0]) - 1):
            if map[row][col].isupper():
                logger.debug(f"found a uncounted plot at {row}, {col}")
                area = 0
                fences = 0
                plant = map[row][col]
                queue = [(row, col)]
                while queue:
                    r, c = queue.pop()
                    if map[r][c] == plant:
                        map[r][c] = plant.lower()
                        area += 1
                        # count corners
                        corner_list = [[(r, c-1), (r-1, c-1), (r-1, c)], 
                                       [(r-1, c), (r-1, c+1), (r, c+1)], 
                                       [(r, c+1), (r+1, c+1), (r+1, c)], 
                                       [(r+1, c), (r+1, c-1), (r, c-1)]]
                        for corner in corner_list:
                            p_count = 0
                            l_count = 0
                            if map[corner[0][0]][corner[0][1]] == plant:
                                queue.append(corner[0])
                            for i, j in corner:
                                if map[i][j].upper() == plant:
                                    p_count += 1
                                if map[i][j] == plant.lower():
                                    l_count += 1
                                logger.debug(f"corner: {corner}, checking: {map[i][j]}, u_count: {p_count}, l_count: {l_count}")
                            logger.debug(f"corner: {corner}, u_count: {p_count}, l_count: {l_count}")
                            match p_count:
                                case 0:
                                    fences += 1
                                case 1:
                                    if map[corner[1][0]][corner[1][1]].upper() == plant:
                                        fences += 1
                                case 2:
                                    if l_count == 0:
                                        fences += 1
                                case 3:
                                    pass
                    logger.debug(f"area: {area}, fences: {fences}")
                total += area * fences
                    
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
