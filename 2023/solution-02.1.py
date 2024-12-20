# imports

# constants
filename = "inputs/input-02.txt"

# functions
def get_game(line):
    split = line.split(":")
    raw_title = split[0]
    # raw_pulls = list(map(lambda x: x.strip(), split[1].split(";")))
    raw_pulls = list([x.strip() for x in split[1].split(";")])
    # pulls = list(map(parse_pulls, raw_pulls))
    return parse_game({
        "title": raw_title,
        "pulls": raw_pulls
    })

def parse_game(raw_game):
    number = int(raw_game["title"].strip("Game "))
    pulls = raw_game["pulls"]
    return {
        "game": number,
        "pulls": list(map(parse_pulls, pulls))
    }

def parse_pulls(raw_pulls):
    # split = list(map(lambda x: x.strip(), raw_pulls.split(",")))
    split = list([x.strip() for x in raw_pulls.split(",")])
    pull = {}
    for p in split:
        tokens = p.split(" ")
        pull[tokens[1]] = int(tokens[0])
    return pull

def is_valid(game):
    MAX_RED = 12
    MAX_GREEN = 13
    MAX_BLUE = 14

    most_red = 0
    most_green = 0
    most_blue = 0

    for pull in game["pulls"]:
        if "red" in pull:
            most_red = max(pull["red"], most_red)
        if "green" in pull:
            most_green = max(pull["green"], most_green)
        if "blue" in pull:
            most_blue = max(pull["blue"], most_blue)
    
    return most_red <= MAX_RED and most_green <= MAX_GREEN and most_blue <= MAX_BLUE

def main():
    print("starting")
    # initialize variables
    total = 0

    with open(filename, "r") as f:
        # Do the work here
        for line in f:
            line = line.strip()
            value = get_game(line)
            if is_valid(value):
                total += value["game"]
            print(line)
            print(value)

    print("done")

    # Print the answer
    print("total: {0:5d}".format(total))

if __name__ == "__main__":
    main()
