# imports

# constants
filename = "inputs/input-09.txt"

# functions
def parse_line(line):
    return list(map(int, line.split()))

def find_next(sequence):
    diffs = [y - x for x, y in zip(sequence, sequence[1:])]
    if all([x == 0 for x in diffs]):
        return sequence[-1]

    return sequence[-1] + find_next(diffs)

def find_prev(sequence):
    diffs = [y - x for x, y in zip(sequence, sequence[1:])]
    if all([x == 0 for x in diffs]):
        return sequence[0]

    return sequence[0] - find_prev(diffs)

def main():
    print("starting")
    # initialize variables
    next_total = 0
    prev_total = 0
    data = []

    with open(filename, "r") as f:
        # Do the work here
        for line in f:
            data.append(parse_line(line))

    for line in data:
        next_total += find_next(line)
        prev_total += find_prev(line)

    print("done")

    # Print the answer
    print("next total: {0:10d} | prev total {1:10d}".format(next_total, prev_total))

if __name__ == "__main__":
    main()
