# imports
import re

# constants
filename = "inputs/input-03.txt"

# functions
def pre_process(f):
    schematic = []
    max = 0

    for line in f:
        result = "." + line.strip() + "."
        if len(result) > max:
            max = len(result)
        schematic.append(result)
    
    border = "." * max
    schematic.insert(0, border)
    schematic.append(border)
    
    return schematic

def process(schematic):
    gear_pattern = re.compile(r"\*")
    nums_pattern = re.compile(r"\d+")
    ratios = []

    for i in range(len(schematic)):
        for m in gear_pattern.finditer(schematic[i]):
            candidates = []

            for x in range(i-1, i+2):
                for num_match in nums_pattern.finditer(schematic[x]):
                    if num_match.start() <= m.end() and num_match.end() >= m.start():
                        candidates.append(num_match.group())

            if len(candidates) == 2:
                ratios.append(int(candidates[0]) * int(candidates[1]))

    return sum(ratios)

def main():
    print("starting")
    # initialize variables
    schematic = []
    
    with open(filename, "r") as f:
        # Do the work here
        schematic = pre_process(f)

    result = process(schematic)

    print("done")

    # Print the answer
    print("result: {0:5d}".format(result))

if __name__ == "__main__":
    main()
