# imports

# constants
filename = "input-07.txt"

# functions

def hand_type(hand):
    h = {}
    for card in hand:
        h[card] = h.get(card, 0) + 1

    if len(h) == 1:
        return 7
    elif len(h) == 2:
        if 4 in h.values():
            return 6
        else:
            return 5
    elif len(h) == 3:
        if 3 in h.values():
            return 4
        else:
            return 3
    elif len(h) == 4:
        return 2
    else:
        return 1

def card_value(card):
    if card == "T":
        return 10
    elif card == "J":
        return 11
    elif card == "Q":
        return 12
    elif card == "K":
        return 13
    elif card == "A":
        return 14
    else:
        return int(card)
    
def hand_value(hand):
    value = hand_type(hand)
    for card in hand:
        value = (value * 16) + card_value(card)
    return value

def parse_hand(hand):
    h, b = hand.split()
    return {"hand": h, "bid": int(b), "value": hand_value(h)}

def main():
    print("starting")
    # initialize variables
    total = 0
    hands = []

    with open(filename, "r") as f:
        # Do the work here
        for line in f:
            line = line.strip()
            value = parse_hand(line)
            hands.append(value)

    sorted_hands = sorted(hands, key=lambda x: x["value"])
    for i in range(len(sorted_hands)):
        print("rank: {0:5d} bid: {1:5d} hand: {2:5s} value: {3:5x}".format(i + 1, sorted_hands[i]["bid"], sorted_hands[i]["hand"], sorted_hands[i]["value"]))
        total += (i + 1) * sorted_hands[i]["bid"]
    print("done")

    # Print the answer
    print("total: {0:5d}".format(total))

if __name__ == "__main__":
    main()
