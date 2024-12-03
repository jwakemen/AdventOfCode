import re


def load_line(line, stacks):
    for i in range(len(line)):
        if line[i] != " ":
            stacks[i].insert(0, line[i])

def process(line, stacks):
    count, source, dest = map(int, re.match(r"move (\d+) from (\d+) to (\d+)", line).group(1, 2, 3))
    
    moving = stacks[source-1][-count:]
    del stacks[source-1][-count:]
    for c in moving:
        stacks[dest-1].append(c)
    
def main():
    print("starting")
    stacks = [[],[],[],[],[],[],[],[],[]]
    with open("inputs/input-05.txt", "r") as f:
        line = f.readline().strip()
        while line != "":
            input = ""
            for c in range(1, len(line), 4):
                input += line[c]

            load_line(input, stacks)
            line = f.readline().strip()
        line = f.readline().strip()
        while line != "":
            process(line, stacks)
            line = f.readline().strip()

    for s in stacks:
        print(s[-1], end="")
    print()

    print("done")

if __name__ == "__main__":
    main()
