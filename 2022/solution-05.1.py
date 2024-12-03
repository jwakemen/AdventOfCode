import re


def load_line(line, stacks):
    for i in range(len(line)):
        if line[i] != " ":
            stacks[i].insert(0, line[i])

def process(line, stacks):
    count, source, dest = re.match(r"move (\d+) from (\d+) to (\d+)", line).group(1, 2, 3)
    print (count, source, dest)
    for i in range(int(count)):
        stacks[int(dest)-1].append(stacks[int(source)-1].pop())

def main():
    print("starting")
    stacks = [[],[],[],[],[],[],[],[],[]]
    with open("inputs/input-05.txt", "r") as f:
        line = f.readline().strip()
        while line != "":
            print(line)
            input = ""
            for c in range(1, len(line), 4):
                input += line[c]

            load_line(input, stacks)
            line = f.readline().strip()
        line = f.readline().strip()
        while line != "":
            print(line)
            process(line, stacks)
            line = f.readline().strip()

    for s in stacks:
        print(s[-1], end="")
    print()

    print("done")

if __name__ == "__main__":
    main()
