def priority(item):
    if ord(item) >= ord('a') and ord(item) <= ord('z'):
        return ord(item) - ord('a') + 1 
    return ord(item) - ord('A') + 27

def find_error(sack):
    m = len(sack) // 2
    print("sack {0} = midpoint {1}".format(sack, m))

    c1 = sack[:m]
    c2 = sack[m:]

    for item in c1:
        if item in c2:
            return item
        
def main():
    print("starting")
    score = 0
    with open("inputs/input-03.txt", "r") as f:
        for line in f:
            score += priority(find_error(line.strip()))
            print("line: {0} = {1}".format(line.strip(), priority(find_error(line.strip()))))

    print("score: {0:5d}".format(score))
    print("done")

if __name__ == "__main__":
    main()
