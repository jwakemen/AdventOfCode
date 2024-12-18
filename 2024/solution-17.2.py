# imports
import logging
import colorlog
import argparse
import sys
import re

# constants
day = 17
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

# machine state
machine = {"A": 0, "B": 0, "C": 0, "I": 0, "M": [], "O": []}

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

def run_program():
    logger.debug(f"Starting program  - machine: {machine}")
    logger.debug(f"Instructions: {machine['M']} - Length: {len(machine['M'])}")
    while machine["I"] < len(machine["M"]):
        logger.debug(f"Before running operation - machine: {machine}")
        instr = machine["M"][machine["I"]]
        oper = machine["M"][machine["I"] + 1]
        logger.debug(f"Instruction: {instr} - Operand: {oper}")
        match instr:
            case 0:
                adv(oper)
            case 1:
                bxl(oper)
            case 2:
                bst(oper)
            case 3:
                jnz(oper)
            case 4:
                bxc(oper)
            case 5:
                out(oper)
            case 6:
                bdv(oper)
            case 7:
                cdv(oper)
            case _:
                ValueError("Invalid instruction")
        logger.debug(f"After running operation - machine: {machine}")

def combo_oper(oper):
    match oper:
        case 1 | 2 | 3:
            return oper
        case 4:
            return machine["A"]
        case 5:
            return machine["B"]
        case 6:
            return machine["C"]
        case 7:
            return -1
        
def adv(oper):
    logger.debug(f"adv: {oper}")
    machine["A"] = int(machine["A"] // pow(2, combo_oper(oper)))
    machine["I"] += 2

def bxl(oper):
    logger.debug(f"bxl: {oper}")
    machine["B"] = machine["B"] ^ oper
    machine["I"] += 2

def bst(oper):
    logger.debug(f"bst: {oper}")
    machine["B"] = combo_oper(oper) % 8
    machine["I"] += 2

def jnz(oper):
    logger.debug(f"jnz: {oper}")
    if machine["A"] != 0:
        machine["I"] = oper
    else:
        machine["I"] += 2

def bxc(oper):
    logger.debug(f"bxc: {oper}")
    machine["B"] = machine["B"] ^ machine["C"]
    machine["I"] += 2

def out(oper):
    logger.debug(f"out: {oper}")
    machine["O"].append(combo_oper(oper) % 8)
    machine["I"] += 2

def bdv(oper):
    logger.debug(f"bdv: {oper}")
    machine["B"] = machine["A"] // pow(2, combo_oper(oper))
    machine["I"] += 2

def cdv(oper):
    logger.debug(f"cdv: {oper}")
    machine["C"] = machine["A"] // pow(2, combo_oper(oper))
    machine["I"] += 2

# main function
def main():
    # setup
    args = get_args()
    logger = setup_logger(args)

    regex_a = re.compile(r"Register A: (\d+)$")
    regex_b = re.compile(r"Register B: (\d+)$")
    regex_c = re.compile(r"Register C: (\d+)$")
    regex_m = re.compile(r"Program: (.*$)")

    logger.info("Starting")
    # machine = {"A": 0, "B": 0, "C": 0, "I": 0, "M": [], "O": []}
    
    # open the input file
    with open(infile, "r") as f:
        # Read the input file
        for line in f:
            line = line.strip()
            if regex_a.match(line):
                machine["A"] = int(regex_a.match(line).group(1))
            elif regex_b.match(line):
                machine["B"] = int(regex_b.match(line).group(1))
            elif regex_c.match(line):
                machine["C"] = int(regex_c.match(line).group(1))
            elif regex_m.match(line):
                machine["M"] = [int(x) for x in regex_m.match(line).group(1).split(",")]

    logger.info(f"input: {machine}")

    i = 0
    pos = -1
    # run the program
    while machine["O"] != machine["M"] and i < pow(8, 16):
        machine["A"] = i
        machine["B"] = 0
        machine["C"] = 0
        machine["I"] = 0
        machine["O"] = []
        run_program()
        logger.info(f"i: {i} - output: {machine['O']}")
        output = ",".join([str(x) for x in machine["O"]])
        if machine["O"] == machine["M"][pos:] and machine["O"] != machine["M"]:
            i <<= 3
            pos -= 1
        else:
            i += 1

    solution = i - 1
    # finish up and log the total
    logger.info("Complete")
    logger.info(f"Solution {solution} Output: {output}")

    # write the output
    final_output = f"{aoc_name} - solution: {solution} output: {output}\n"
    sys.stdout.write(final_output)
    with open(outfile, "w") as f:
        f.write(final_output)

if __name__ == "__main__":
    main()
