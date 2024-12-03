def selection_value(selection):
    return ord(selection) - ord('A')

def result_score(throw):
    opp = selection_value(throw[0])
    strat = throw[2]

    if strat == 'X':
        return ((opp - 1) % 3) + 1 + 0
    elif strat == 'Y':
        return (opp % 3) + 1 + 3
    else:
        return ((opp + 1) % 3) + 1 + 6

def main():
    print("starting")
    score = 0
    with open("inputs/input-02.txt", "r") as f:
        for line in f:
            score += result_score(line)
            print("line: {0} = {1}".format(line[:3], result_score(line)))

    print("score: {0:5d}".format(score))
    print("done")

if __name__ == "__main__":
    main()
