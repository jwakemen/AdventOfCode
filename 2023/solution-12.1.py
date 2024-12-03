# imports

# constants
filename = "inputs/input-12.txt"

# functions
def count_springs(line):
    springs, counts = line.split(" ")
    springs = list(springs)
    counts = list(map(int, counts.split(",")))

    print(springs, "-", counts)
    print(len(springs))
    print(sum(counts) + len(counts) - 1)

    slack = len(springs) - sum(counts) - len(counts) + 1
    print(slack)

    if slack == 0:
        return 1

    # if 

    return 0

def main():
    print("starting")
    # initialize variables
    total = 0

    data = []

    with open(filename, "r") as f:
        # Do the work here
        for line in f:
            data.append(line.strip())

    # print(data)
    for line in data[:1]:
        total += count_springs(line)

    print("done")

    # Print the answer
    print("total: {0:5d}".format(total))

if __name__ == "__main__":
    main()
