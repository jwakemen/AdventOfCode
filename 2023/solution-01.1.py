# imports for day 1, solution 1
import re

# constants for day 1, solution 1
filename = "input-01.txt"

# functions for day 1, solution 1
def get_calibration(line):
    pattern = re.compile(r"\d")
    matches = pattern.findall(line)
    first_char = matches[0]
    last_char = matches[-1]
    return int(first_char + last_char)

def main():
    print("starting")
    # initialize variables
    total = 0

    with open(filename, "r") as f:
        # Do the work here
        for line in f:
            line = line.strip()
            value = get_calibration(line)
            print("line {0:45s} result {1:5d}".format(line, value))
            total += value
    print("done")

    # Print the answer
    print("total: {0:5d}".format(total))

if __name__ == "__main__":
    main()
