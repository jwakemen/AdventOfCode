# imports for day 1, solution 1
import re

# constants for day 1, solution 1
filename = "inputs/input-01.txt"

# functions for day 1, solution 1
def get_calibration(line):
    pattern = re.compile(r"\d|one|two|three|four|five|six|seven|eight|nine")
    first_match = pattern.search(line)
    next_match = first_match
    while next_match is not None:
        last_match = next_match
        next_match = pattern.search(line, next_match.pos + 1)
    first_char = decode(first_match.group())
    last_char = decode(last_match.group())
    return int(first_char + last_char)

def decode(value):
    if value == "one":
        return '1'
    elif value == "two":
        return '2'
    elif value == "three":
        return '3'
    elif value == "four":
        return '4'
    elif value == "five":
        return '5'
    elif value == "six":
        return '6'
    elif value == "seven":
        return '7'
    elif value == "eight":
        return '8'
    elif value == "nine":
        return '9'
    else:
        return value

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
