# imports

# constants
filename = "inputs/input-10.txt"

# functions
def read_data(f):
    data = []
    for line in f:
        data.append(line.strip())
    return data

def find_start(data):
    for x in range(len(data)):
        y = data[x].find("S")
        if y >= 0:
            return (x, y)
        
def process(data, start):
    count = 1
    # find inital steps
    steps = []
    if start[0] > 0 and (data[start[0]-1][start[1]] == "|" or data[start[0]-1][start[1]] == "7" or data[start[0]-1][start[1]] == "F"):
        steps.append((start[0]-1, start[1], "N"))
    if start[0] < len(data) - 1 and (data[start[0]+1][start[1]] == "|" or data[start[0]+1][start[1]] == "J" or data[start[0]+1][start[1]] == "L"):
        steps.append((start[0]+1, start[1], "S"))
    if start[1] > 0 and (data[start[0]][start[1]-1] == "-" or data[start[0]][start[1]-1] == "L" or data[start[0]][start[1]-1] == "F"):
        steps.append((start[0], start[1]-1, "W"))
    if start[1] < len(data[0]) - 1 and (data[start[0]][start[1]+1] == "-" or data[start[0]][start[1]+1] == "J" or data[start[0]][start[1]+1] == "7"):
        steps.append((start[0], start[1]+1, "E"))

    print(steps)
    while not (steps[0][0] == steps[1][0] and steps[0][1] == steps[1][1]):
        steps[0] = next_step(data, *steps[0])
        steps[1] = next_step(data, *steps[1])
        count += 1
        print(steps)
    return count

def next_step(data, x, y, direction):
    if data[x][y] == "|":
        if direction == "N":
            return (x-1, y, "N")
        elif direction == "S":
            return (x+1, y, "S")
        else:
            print("error")
    elif data[x][y] == "-":
        if direction == "W":
            return (x, y-1, "W")
        elif direction == "E":
            return (x, y+1, "E")
        else:
            print("error")
    elif data[x][y] == "L":
        if direction == "S":
            return (x, y+1, "E")
        elif direction == "W":
            return (x-1, y, "N")
        else:
            print("error")
    elif data[x][y] == "J":
        if direction == "S":
            return (x, y-1, "W")
        elif direction == "E":
            return (x-1, y, "N")
        else:
            print("error")
    elif data[x][y] == "7":
        if direction == "N":
            return (x, y-1, "W")
        elif direction == "E":
            return (x+1, y, "S")
        else:
            print("error")
    elif data[x][y] == "F":
        if direction == "N":
            return (x, y+1, "E")
        elif direction == "W":
            return (x+1, y, "S")


def main():
    print("starting")
    # initialize variables
    total = 0

    with open(filename, "r") as f:
        # Do the work here
        data = read_data(f)

    start = find_start(data)
    print(start)

    total = process(data, start)

    print("done")

    # Print the answer
    print("total: {0:5d}".format(total))

    print(u"\u2550\u2551\u2554\u2557\u255A\u255D\u2591")

if __name__ == "__main__":
    main()
