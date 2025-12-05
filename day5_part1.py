def count_fresh_ids(filename):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")

    ranges = []
    ids = []
    reading_ranges = True

    for line in lines:
        if line.strip() == "":
            reading_ranges = False
            continue

        if reading_ranges:
            a, b = map(int, line.split("-"))
            ranges.append((a, b))
        else:
            ids.append(int(line))

    fresh_count = 0
    for x in ids:
        for a, b in ranges:
            if a <= x <= b:
                fresh_count += 1
                break

    return fresh_count


if __name__ == "__main__":
    # Change this to your input filename
    input_file = "quizday5.txt"

    result = count_fresh_ids(input_file)
    print("Day 5 Part 1 Answer:", result)
