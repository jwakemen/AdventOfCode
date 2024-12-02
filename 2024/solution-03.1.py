# imports
import re

# constants
filename = "inputs/input-03.txt"

# functions
def find_matches(line):
    # find the matches in the line
    regex = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    matches = regex.findall(line)
    return matches

def calculate(pairs):
    acc = 0
    for pair in pairs:
        acc += int(pair[0]) * int(pair[1])
    return acc

def main():
    print("starting")
    # initialize variables
    total = 0

    with open(filename, "r") as f:
        # Do the work here
        for line in f:
            # line = line.strip()
            values = find_matches(line)
            total += calculate(values)
    print("done")

    # Print the answer
    print("total: {0:5d}".format(total))

if __name__ == "__main__":
    main()
