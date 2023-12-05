# imports

# constants
filename = "input-04.txt"

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
            "tries": tries,
            "count": 1
        })
    return cards

def process(cards):
    for card in cards:
        count = 0
        for number in card["tries"]:
            if number in card["winners"]:
                count += 1
        
        for i in range(count):
            cards[card["card"] + i]["count"] += card["count"]
    return cards

def main():
    print("starting")
    # initialize variables

    with open(filename, "r") as f:
        # Do the work here
        cards = pre_process(f)
    
    cards = process(cards)

    total = sum(map(lambda c: c["count"], cards))
    
    print("done")

    # Print the answer
    print("total: {0:5d}".format(total))

if __name__ == "__main__":
    main()
