# imports
import re

# constants
filename = "inputs/input-03.txt"

# functions
def pre_process(line):
    result = "." + line.strip() + "."
    return result, len(result)

def process(schematic, line):
    pattern = re.compile(r"\d+")
    unwanteds = '.0123456789'
    part_numbers = []
    for m in pattern.finditer(schematic[line]):
        box_top = schematic[line-1][m.start() - 1:m.end() + 1]
        box_mid = schematic[line][m.start() - 1:m.end() + 1]
        box_bot = schematic[line+1][m.start() - 1:m.end() + 1]

        if len(box_top.strip(unwanteds)) != 0 or len(box_mid.strip(unwanteds)) != 0 or len(box_bot.strip(unwanteds)) != 0:
            part_numbers.append(int(m.group(0)))

    return part_numbers

def main():
    print("starting")
    # initialize variables
    total = 0
    schematic = []
    
    with open(filename, "r") as f:
        # Do the work here
        max = 0
        for line in f:
            pl, ln = pre_process(line)
            schematic.append(pl)
            if ln > max:
                max = ln
        border = "." * max
        schematic.insert(0, border)
        schematic.append(border)

    for i in range(len(schematic)):
        total += sum(process(schematic, i))

    print("done")

    # Print the answer
    print("total: {0:5d}".format(total))

if __name__ == "__main__":
    main()
