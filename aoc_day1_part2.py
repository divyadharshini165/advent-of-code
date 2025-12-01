def parse_input(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]


def count_zero_passes(position, direction, distance):
    if direction == "R":
        return (position + distance) // 100
    else:  # "L"
        if position == 0:
            return distance // 100
        elif position <= distance:
            return (distance - position) // 100 + 1
        else:
            return 0


def solve_part_two(filename):
    instructions = parse_input(filename)
    position = 50
    total_zeros = 0

    for inst in instructions:
        direction = inst[0]
        distance = int(inst[1:])

        total_zeros += count_zero_passes(position, direction, distance)

        if direction == "R":
            position = (position + distance) % 100
        else:
            position = (position - distance) % 100

    return total_zeros


if __name__ == "__main__":
    filename = "quiz2.txt"   # keeps your original input file
    answer = solve_part_two(filename)
    print("Part Two Password:", answer)
