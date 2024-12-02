# imports
import numpy as np

# constants
filename = "inputs/input-01.txt"

# functions

def main():
    print("starting")
    # initialize variables
    total = 0

    # read the data
    data = np.loadtxt(filename, dtype=int)
    print("done reading")

    # loop through the data
    (lefts, rights) = np.unstack(data, axis=1)
    
    # sort the lefts and rights
    lefts.sort()
    rights.sort()
    
    for i in range(len(lefts)):
        total += abs(lefts[i] - rights[i])
    
    print("done")

    # Print the answer
    print("total: {0:5d}".format(total))

if __name__ == "__main__":
    main()
