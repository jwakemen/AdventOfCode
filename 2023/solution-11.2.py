# imports

# constants
filename = "inputs/input-11.txt"

# functions

# main
def main():
    print("starting")
    # initialize variables
    total = 0
    galaxies = []
    columns = []
    row = 0

    with open(filename, "r") as f:
        # Do the work here
        for line in f:
            line = line.strip()
            if len(columns) == 0:
                for y in range(len(line)):
                    columns.append(0)

            for col in range(len(line)):
                if line[col] == '#':
                    columns[col] += 1
                    galaxies.append((row, col))

            row += 1
            if line.count('#') == 0:
                row += 999999
 
    for col in range(len(columns) - 1, 0, -1):
        if columns[col] == 0:
            for i in range(len(galaxies)):
                if galaxies[i][1] > col:
                    galaxies[i] = (galaxies[i][0], galaxies[i][1] + 999999)

    while len(galaxies) > 0:
        g = galaxies.pop()
        for galaxy in galaxies:
            total += abs(g[0] - galaxy[0]) + abs(g[1] - galaxy[1])

    print("done")

    # Print the answer
    print("total: {0:5d}".format(total))

if __name__ == "__main__":
    main()
