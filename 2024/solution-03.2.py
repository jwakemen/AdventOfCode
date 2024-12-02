# imports
import re

# constants
filename = "inputs/input-03.txt"

# functions
def find_matches(line):
    # find the matches in the line
    regex = re.compile(r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)")
    matches = regex.findall(line)
    return matches

def calculate(matches):
    enabled = True
    acc = 0
    for m in matches:
        match m:
            case "do()":
                enabled = True
            case "don't()":
                enabled = False
            case _:
                if enabled:
                    l,r = re.match(r"mul\((\d{1,3}),(\d{1,3})\)", m).groups()
                    acc += int(l) * int(r)
    return acc

def main():
    print("starting")
    # initialize variables
    total = 0
    lines = ""

    with open(filename, "r") as f:
        # Read the input file
        for line in f:
            lines += line

    values = find_matches(lines)
    total += calculate(values)
    print("done")

    # Print the answer
    print("total: {0:5d}".format(total))

if __name__ == "__main__":
    main()
