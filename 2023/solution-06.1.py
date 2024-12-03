# imports

# constants
filename = "inputs/input-06.txt"

# functions
def process_times(times, distances):
    winnings = []
    for i in range(len(times)):
        winnings.append(wins(times[i], distances[i]))
    return winnings

def wins(time, distance):
    count = 0
    for i in range(time+1):
        if i * (time - i) > distance:
            count += 1
    return count

def main():
    print("starting")
    # initialize variables
    total = 0

    input = []
    with open(filename, "r") as f:
        # Do the work here
        for line in f:
            line = line.strip()
            str_vals = line.split(":")[1].split()
            values = [int(x) for x in str_vals]
            input.append(values)

    winnings = process_times(input[0], input[1])

    total = 1
    for i in winnings:
        total *= i
    print("done")

    # Print the answer
    print("total: {0:5d}".format(total))

if __name__ == "__main__":
    main()
