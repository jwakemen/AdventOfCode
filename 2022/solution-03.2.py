def priority(item):
    if ord(item) >= ord('a') and ord(item) <= ord('z'):
        return ord(item) - ord('a') + 1 
    return ord(item) - ord('A') + 27

def find_common(sack1, sack2, sack3):
    for item in sack1:
        if (item in sack2) & (item in sack3):
            return item
        
def get_group(file):
    e1 = file.readline().strip()
    if e1 == '':
        return None, None, None
    e2 = file.readline().strip()
    e3 = file.readline().strip()
    return e1, e2, e3
        
def main():
    print("starting")
    score = 0
    done = False
    with open("inputs/input-03.txt", "r") as f:
        while not done:
            elf1, elf2, elf3 = get_group(f)
            if elf1 is None:
                done = True
                break

            print("group:\n{0}\n{1}\n{2}".format(elf1, elf2, elf3))
            common = find_common(elf1, elf2, elf3)
            score += priority(common)
            print("common: {0} priority {1}\n".format(common, priority(common)))

    print("score: {0:5d}".format(score))
    print("done")

if __name__ == "__main__":
    main()
