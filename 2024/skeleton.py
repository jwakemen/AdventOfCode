# imports

# constants
filename = "inputs/input-XX.txt"

# functions

def main():
    print("starting")
    # initialize variables
    total = 0

    with open(filename, "r") as f:
        # Do the work here
        for line in f:
            line = line.strip()
            value = "TODO"
            print("line {0:45s} result {1:5}".format(line, value))

    print("done")

    # Print the answer
    print("total: {0:5d}".format(total))

if __name__ == "__main__":
    main()
