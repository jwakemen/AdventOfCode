# imports

# constants
filename = "inputs/input-04.txt"

# functions
def pre_process(f):
    cards = []
    for line in f:
        raw = line.strip().split(":")
        raw_card = raw[0].strip().split()
        card = int(raw_card[1])
        raw_numbers = raw[1].strip().split("|")
        raw_winners = raw_numbers[0].strip().split()
        raw_tries = raw_numbers[1].strip().split()
        winners = [int(x) for x in raw_winners]
        tries = [int(x) for x in raw_tries]
        cards.append({
            "card": card,
            "winners": winners,
            "tries": tries
        })
    return cards

def process(cards):
    points = 0
    for card in cards:
        count = 0
        for number in card["tries"]:
            if number in card["winners"]:
                count += 1
        
        if count >= 1:
            points += 2 ** (count - 1)
    return points

def main():
    print("starting")
    # initialize variables

    with open(filename, "r") as f:
        # Do the work here
        cards = pre_process(f)
    
    total = process(cards)
    print("done")

    # Print the answer
    print("total: {0:5d}".format(total))

if __name__ == "__main__":
    main()
