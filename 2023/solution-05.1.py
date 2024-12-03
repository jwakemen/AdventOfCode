# imports
import re

# constants
filename = "inputs/input-05.txt"

# functions
def get_seeds(f):
    line = f.readline()
    seeds = list([{"seed": x} for x in list(map(int, line.split(":")[1].split()))])

    # read in the blank line
    f.readline()
    return seeds

def get_mapping(f):
    mapping = {}
    pattern = re.compile(r"(\w+)-to-(\w+).*")

    map_string = f.readline()
    if not map_string:
        return None
    
    groups = pattern.match(map_string).groups()
    mapping["source"] = groups[0]
    mapping["destination"] = groups[1]
    mapping["function"] = []

    line = f.readline().strip()
    while line:
        code = list(map(int, line.split()))
        mapping["function"].append({"source": code[1], "destination": code[0], "length": code[2]})
        line = f.readline().strip()
    return mapping

def process_mapping(mapping, seeds):
    for seed in seeds:
        seed[mapping["destination"]] = seed[mapping["source"]]

        for function in mapping["function"]:
            start = function["source"]
            end = function["source"] + function["length"]

            if seed[mapping["source"]] >= start and seed[mapping["source"]] < end:
                seed[mapping["destination"]] = function["destination"] + (seed[mapping["source"]] - start)
                break
    return seeds

def find_lowest_location(seeds):
    lowest = seeds[0]["location"]
    for seed in seeds:
        if seed["location"] < lowest:
            lowest = seed["location"]
    return lowest

def main():
    print("starting")
    # initialize variables
    total = 0
    mappings = {}

    with open(filename, "r") as f:
        # Do the work here
        seed_list = get_seeds(f)

        mapping = get_mapping(f)
        while mapping:
            mappings[mapping["source"]] = mapping
            mapping = get_mapping(f)

    current_map = "seed"
    while current_map != "location":
        seed_list = process_mapping(mappings[current_map], seed_list)
        current_map = mappings[current_map]["destination"]

    lowest = find_lowest_location(seed_list)
    print("done")

    # Print the answer
    print("The lowest location is {}".format(lowest))

if __name__ == "__main__":
    main()
