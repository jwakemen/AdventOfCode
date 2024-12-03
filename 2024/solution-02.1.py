# imports
import numpy as np

# constants
filename = "inputs/input-02.txt"

# functions
def check_safe(values):
    # check if the values are increacing or decreasing
    if values[0] < values[1]:
        return check_increasing(values)
    elif values[0] > values[1]:
        return check_increasing(np.flip(values, axis=0))
    else:
        return False

def check_increasing(values):
    for i in range(1, len(values)):
        if values[i] - values[i-1] <= 0 or values[i] - values[i-1] > 3:
            return False
    return True

def main():
    print("starting")
    # initialize variables
    total = 0

    with open(filename, "r") as f:
        # Do the work here
        for line in f:
            line = line.strip()
            value = np.array(line.split(), dtype=int)
            print("line {0:45s}".format(line))
            result = check_safe(value)
            print("result {0:5}".format(result))
            print

            total += result

    print("done")

    # Print the answer
    print("total: {0:5d}".format(total))

if __name__ == "__main__":
    main()