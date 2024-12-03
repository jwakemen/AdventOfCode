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
        
def make_loop_map(data, start):
    count = 1
    map = [["." for y in range(len(data[x]))] for x in range(len(data))]
    map[start[0]][start[1]] = "S"

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

    map[steps[0][0]][steps[0][1]] = translate(data[steps[0][0]][steps[0][1]])
    map[steps[1][0]][steps[1][1]] = translate(data[steps[1][0]][steps[1][1]])

    while not (steps[0][0] == steps[1][0] and steps[0][1] == steps[1][1]):
        steps[0] = next_step(data, *steps[0])
        map[steps[0][0]][steps[0][1]] = translate(data[steps[0][0]][steps[0][1]])

        steps[1] = next_step(data, *steps[1])
        map[steps[1][0]][steps[1][1]] = translate(data[steps[1][0]][steps[1][1]])

        count += 1

    # for line in map:
    #     print("".join(line))
    
    return map

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

def translate(c):
    if c == "|":
        return u"\u2551"
    elif c == "-":
        return u"\u2550"
    elif c == "L":
        return u"\u255A"
    elif c == "J":
        return u"\u255D"
    elif c == "7":
        return u"\u2557"
    elif c == "F":
        return u"\u2554"
    else:
        return c
    
def expand_map(map):
    expanded = []
    for line in map:
        l1 = []
        l2 = []
        l3 = []
        for c in line:
            l1.append(" ")
            if c == u"\u2551" or c == u"\u255A" or c == u"\u255D":
                l1.append(u"\u2551")
            elif c == "S":
                l1.append("S")
            else:
                l1.append(" ")
            l1.append(" ")

            if c == u"\u2550" or c == u"\u255D" or c == u"\u2557":
                l2.append(u"\u2550")
            elif c == "S":
                l2.append("S")
            else:
                l2.append(" ")
            l2.append(c)
            if c == u"\u2550" or c == u"\u255A" or c == u"\u2554":
                l2.append(u"\u2550")
            elif c == "S":
                l2.append("S")
            else:
                l2.append(" ")

            l3.append(" ")
            if c == u"\u2551" or c == u"\u2554" or c == u"\u2557":
                l3.append(u"\u2551")
            elif c == "S":
                l3.append("S")
            else:
                l3.append(" ")
            l3.append(" ")

        expanded.append(l1)
        expanded.append(l2)
        expanded.append(l3)

    expanded = make_border(expanded)
    return expanded

def make_border(map):
    for y in range(len(map[0])):
        map[0][y] = u"\u2591"
    for x in range(1, len(map) - 1):
        map[x][0] = u"\u2591"
        map[x][-1] = u"\u2591"
    for y in range(len(map[-1])):
        map[-1][y] = u"\u2591"

    return map

def top_down_pass(map):
    changed = False
    for x in range(len(map)):
        for y in range(len(map[x])):
            if map[x][y] == " " or map[x][y] == ".":
                if check_neighbours(map, x, y):
                    map[x][y] = u"\u2591"
                    changed = True

    return map, changed

def bottom_up_pass(map):
    changed = False
    for x in range(len(map) -1, 0, -1):
        for y in range(len(map[x]) - 1, 0, -1):
            if map[x][y] == " " or map[x][y] == ".":
                if check_neighbours(map, x, y):
                    map[x][y] = u"\u2591"
                    changed = True

    return map, changed

def check_neighbours(map, x, y):
    if x > 0 and map[x-1][y] == u"\u2591":
        return True
    if x < len(map) - 1 and map[x+1][y] == u"\u2591":
        return True
    if y > 0 and map[x][y-1] == u"\u2591":
        return True
    if y < len(map[x]) - 1 and map[x][y+1] == u"\u2591":
        return True

    return False

def main():
    print("starting")
    # initialize variables
    total = 0

    with open(filename, "r") as f:
        # Do the work here
        data = read_data(f)

    start = find_start(data)
    print(start)

    map = make_loop_map(data, start)
    # for line in map:
    #     print("".join(line))

    map = expand_map(map)
    changed = True

    while changed:
        map, c1 = top_down_pass(map)
        map, c2 = bottom_up_pass(map)
        changed = c1 or c2

    for line in map:
        print("".join(line))

    total = sum([line.count(".") for line in map])

    print("done")

    # Print the answer
    print("total: {0:5d}".format(total))

if __name__ == "__main__":
    main()
