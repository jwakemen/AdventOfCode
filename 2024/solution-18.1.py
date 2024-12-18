# imports
import logging
import colorlog
import argparse
import sys
import networkx as nx
from visualizer import GraphVisualizer

# constants
day = 18
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
    vis = GraphVisualizer()
    
    # initialize variables
    total = 0

    logger.info("Starting")
    map = {(x, y): "." for x in range(71) for y in range(71)}
    vis.show_frame(map)

    # open the input file
    with open(infile, "r") as f:
        # Read the input file
        for _ in range(1024):
            x, y = [int(n) for n in f.readline().strip().split(",")]
            map[(x,y)] = "#"
            vis.show_frame(map)

    # create the graph
    G = nx.Graph()
    for x in range(71):
        for y in range(71):
            if map[(x,y)] == ".":
                G.add_node((x,y))
                if x > 0 and map[(x-1,y)] == ".":
                    G.add_edge((x,y), (x-1,y))
                if x < 70 and map[(x+1,y)] == ".":
                    G.add_edge((x,y), (x+1,y))
                if y > 0 and map[(x,y-1)] == ".":
                    G.add_edge((x,y), (x,y-1))
                if y < 70 and map[(x,y+1)] == ".":
                    G.add_edge((x,y), (x,y+1))

    # find the shortest path
    start = (0,0)
    end = (70,70)
    total = nx.shortest_path_length(G, start, end)

    # show the path
    for x, y in nx.shortest_path(G, start, end):
        map[(x,y)] = "*"
        vis.show_frame(map)

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
