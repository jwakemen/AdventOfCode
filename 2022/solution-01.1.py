def next_elf(file):
    total = 0
    line = file.readline()
    while (line != "\n") & (line != ""):
        total += int(line)
        line = file.readline()
    return total

def main():
    print("starting")
    most_calories = 0
    with open("input-01.txt", "r") as f:
        this_elf = next_elf(f)
        while this_elf != 0:
            if this_elf > most_calories:
                most_calories = this_elf
            print('elf {0:5d}'.format(this_elf))
            this_elf = next_elf(f)
    print("done")
    print("most calories: {0:5d}".format(most_calories))

if __name__ == "__main__":
    main()
