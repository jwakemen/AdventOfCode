# imports
import logging
import colorlog
import argparse
import sys
import networkx as nx

# constants
day = 20
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
    maze = []

    logger.info("Starting")
    
    # open the input file
    f = open(infile, "r")
    # Read the input file
    for line in f:
       maze.append([c for c in line])
    
    # close the input file
    f.close()
    logger.debug(f"maze: {maze}")

    for row in maze:
        logger.debug(f"row: {row}")
    
    # create the maze graph
    graph = nx.Graph()
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == "S":
                start = (row, col)
            elif maze[row][col] == "E":
                end = (row, col)

            if maze[row][col] in ".SE":
                for (dr, dc) in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    if 0 <= row + dr < len(maze) and 0 <= col + dc < len(maze[row]):
                        if maze[row + dr][col + dc] in ".SE":
                            graph.add_edge((row, col), (row + dr, col + dc))

    shortest_path = nx.shortest_path(graph, start, end)
    logger.debug(f"Shortest path: {shortest_path}")

    cheats = []

    cheat_targets = []
    for dr in range(-20, 21):
        max = 20 - abs(dr)
        for dc in range(-max, max + 1):
            cheat_targets.append((dr, dc))

    for step in range(len(shortest_path) - 100):
        for dr, dc in cheat_targets:
            nr, nc = shortest_path[step][0] + dr, shortest_path[step][1] + dc
            if 0 <= nr < len(maze) and 0 <= nc < len(maze[nr]) and maze[nr][nc] in ".E":
                end_point = (shortest_path[step][0] + dr, shortest_path[step][1] + dc)
                if end_point in shortest_path[step + 100 + abs(dr) + abs(dc):]:
                    cheats.append((shortest_path[step], end_point))
    logger.info(f"Cheats: {cheats}")

    total = len(cheats)

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
