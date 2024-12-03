def find_packet(line):
    for i in range(len(line)-3):
        slice = line[i:i+4]
        if slice[0] not in slice[1:] and slice[1] not in slice[2:] and slice[2] not in slice[3:]:
            return i + 4

def find_message(packet):
    def check(start):
        return slice[start] not in slice[start+1:]

    for i in range(len(packet)-13):
        slice = packet[i:i+14]
        mapping = [check(i) for i in range(len(slice))]
        if all(mapping):
            return i + 14

def main():
    print("starting")
    with open("inputs/input-06.txt", "r") as f:
        line = f.readline().strip()
        packet = find_packet(line)
        message = find_message(line[packet:])
        print(packet, message)

    print(packet+message)

    print("done")

if __name__ == "__main__":
    main()
