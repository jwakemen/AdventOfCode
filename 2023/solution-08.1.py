# imports
import re, math

# constants
filename = "input-08.txt"

# functions
def get_instructions(f):
    line = f.readline().strip()
    f.readline() # discard the blank line
    return line

def get_nodes(f):
    pattern = re.compile(r"(\w{3}) = \((\w{3}), (\w{3})\)")
    nodes = {}
    line = f.readline().strip()
    while line != "":
        matches = pattern.match(line)
        if matches:
            nodes[matches.group(1)] = {"L": matches.group(2), "R": matches.group(3)}

        line = f.readline().strip()
    return nodes

def process_part_one(instructions, nodes):
    node = 'AAA'
    count = 0
    while node != 'ZZZ':
        node = nodes[node][instructions[count % len(instructions)]]
        count += 1
    return count

def process_find_end(instructions, nodes, start):
    node = start
    count = 0
    while not node.endswith('Z'):
        node = nodes[node][instructions[count % len(instructions)]]
        count += 1
    return count


def process_part_two(instructions, nodes):
    counts = []

    starts = [node for node in nodes if node.endswith('A')]

    print(len(instructions))
    print(starts)
    for start in starts:
        counts.append(process_find_end(instructions, nodes, start))
    print(counts)
    print([count // len(instructions) for count in counts])
    print([count % len(instructions) for count in counts])
    return math.lcm(*counts)

def main():
    print("starting")
    # initialize variables

    with open(filename, "r") as f:
        # Do the work here
        instructions = get_instructions(f)
        nodes = get_nodes(f)
        part_one = process_part_one(instructions, nodes)
        part_two = process_part_two(instructions, nodes)

    print("done")

    # Print the answer
    print("steps for part 1: {0:5d}".format(part_one))
    print("steps for part 2: {0:5d}".format(part_two))

if __name__ == "__main__":
    main()
