# imports
import logging
import colorlog
import argparse
import sys
import fileinput
import networkx as nx

# constants
day = 16
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

# map
map = []

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

    logger.info("Starting")
    
    # open the input file
    map = {(x, y): c
        for y, r in enumerate(fileinput.input(infile))
        for x, c in enumerate(r.strip())}
    start = min(k for k, v in map.items() if v == 'S')
    end = min(k for k, v in map.items() if v == 'E')

    logger.info(f"Start: {start}")
    logger.info(f"End: {end}")
    logger.debug(f"Graph: {map}")

    # create the graph
    G = nx.DiGraph()
    for (row, col), char in map.items():
        if char != '#':
            for dir in range(4):
                dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1) ][dir]
                G.add_edge((row, col, dir), (row + dx, col + dy, dir), weight = 1)
                G.add_edge((row, col, dir), (row, col, (dir - 1) % 4), weight = 1000)
                G.add_edge((row, col, dir), (row, col, (dir + 1) % 4), weight = 1000)

    m = [nx.shortest_path_length(G, (*start, 0), (*end, d), "weight") for d in range(4)]
    logger.info(f"Shortest paths: {m}")

    min_path = min(m)
    shortest_paths = [nx.all_shortest_paths(G, (*start, 0), (*end, d), "weight") for d in range(4) if m[d] == min_path]
    nodes = [set(tuple(p) for t in paths for *p, h in t) for paths in shortest_paths]
    logger.info(f"Nodes: {nodes}")
    total = len(set.intersection(*nodes))

    # finish up and log the total
    logger.info("Complete")

    # write the output
    final_output = f"{aoc_name} - total: {total}\n"
    sys.stdout.write(final_output)
    with open(outfile, "w") as f:
        f.write(final_output)

if __name__ == "__main__":
    main()
