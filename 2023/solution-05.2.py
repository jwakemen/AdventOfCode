# imports
import re, sys

# constants
filename = "input-05.txt"

# functions
def get_seeds(f):
    line = f.readline()
    seed_line = list(map(int, line.split(":")[1].split()))


    seeds = []
    for i in range(0, len(seed_line), 2):
        seeds.append({"start": seed_line[i], "length": seed_line[i+1]})
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

def get_seed_location(seed, mappings):
    current_mapping = "seed"
    current = seed

    while current_mapping != "location":
        current = process_mapping(mappings[current_mapping], current)
        current_mapping = mappings[current_mapping]["destination"]
    return current

def process_mapping(mapping, seed):
    seed[mapping["destination"]] = seed[mapping["source"]]

    for function in mapping["function"]:
        start = function["source"]
        end = function["source"] + function["length"]
        if seed[mapping["destination"]] < start:
            seed["skip"] = min(seed["skip"], start - seed[mapping["destination"]])

        if seed[mapping["source"]] >= start and seed[mapping["source"]] < end:
            seed[mapping["destination"]] = function["destination"] + (seed[mapping["source"]] - start)
            seed["skip"] = min(seed["skip"], end - seed[mapping["source"]])
            break
    return seed

def find_lowest_location(seeds, mappings):
    lowest = sys.maxsize
    for seed in seeds:
        s = {"seed": seed["start"], "skip": seed["length"]}
        while s["skip"] > 0:
            s = get_seed_location(s, mappings)
            if s["location"] < lowest:
                lowest = s["location"]
            s["seed"] += s["skip"]
            s["skip"] = seed["length"] - (s["seed"] - seed["start"])
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

    lowest = find_lowest_location(seed_list, mappings)
    print("done")

    # Print the answer
    print("The lowest location is {}".format(lowest))

if __name__ == "__main__":
    main()
