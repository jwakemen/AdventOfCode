def get_assignments(line):
    a = line.strip().split(",")
    return a

def overlap(a, b):
    a_start, a_end = map(int, a.split("-"))
    b_start, b_end = map(int, b.split("-"))
    print(a_start, a_end, b_start, b_end)
    print((a_start <= b_start and b_start <= a_end) or (a_start <= b_end and b_end <= a_end) or (b_start <= a_start and a_start <= b_end) or (b_start <= a_end and a_end <= b_end))
    if (a_start <= b_start and b_start <= a_end) or (a_start <= b_end and b_end <= a_end) or (b_start <= a_start and a_start <= b_end) or (b_start <= a_end and a_end <= b_end):
        return 1
    return 0

def main():
    print("starting")
    score = 0
    done = False
    with open("inputs/input-04.txt", "r") as f:
        for line in f:
            print(line.strip())
            assignments = get_assignments(line)
            score += overlap(*assignments)

    print("score: {0:5d}".format(score))
    print("done")

if __name__ == "__main__":
    main()
