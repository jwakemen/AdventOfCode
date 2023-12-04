def next_elf(file):
    total = 0
    line = file.readline()
    while (line != "\n") & (line != ""):
        total += int(line)
        line = file.readline()
    return total

def main():
    print("starting")
    top_three = [0, 0, 0]
    with open("input-01.txt", "r") as f:
        this_elf = next_elf(f)
        while this_elf != 0:
            if this_elf > top_three[0]:
                top_three[2] = top_three[1]
                top_three[1] = top_three[0]
                top_three[0] = this_elf
            elif this_elf > top_three[1]:
                top_three[2] = top_three[1]
                top_three[1] = this_elf
            elif this_elf > top_three[2]:
                top_three[2] = this_elf
            this_elf = next_elf(f)
    print("done")
    print("most calories: {0:5d} {1:5d} {2:5d}".format(top_three[0], top_three[1], top_three[2]))
    print("total: {0:5d}".format(top_three[0] + top_three[1] + top_three[2]))

if __name__ == "__main__":
    main()
