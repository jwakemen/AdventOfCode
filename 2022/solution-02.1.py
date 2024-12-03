def selection_score(selection):
    if selection in ['A', 'B', 'C']:
        return ord(selection) - (ord('A') - 1)
    return ord(selection) - ord('W')

def result_score(throw):
    opp = selection_score(throw[0])
    my = selection_score(throw[2])

    if opp == my:
         return 3
    elif (opp + 1) % 3 == my % 3:
        return 6
    else:
        return 0


def main():
    print("starting")
    score = 0
    with open("inputs/input-02.txt", "r") as f:
        for line in f:
            print("line: {0} = {1} + {2}".format(line[:3], result_score(line), selection_score(line[2])))
            score += result_score(line) + selection_score(line[2])
    print("score: {0:5d}".format(score))
    print("done")

if __name__ == "__main__":
    main()

    