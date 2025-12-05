def count_all_fresh_ids(filename):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")

    # Read only fresh ranges (before the blank line)
    ranges = []
    for line in lines:
        if line.strip() == "":
            break
        a, b = map(int, line.split("-"))
        ranges.append((a, b))

    # Sort ranges by start
    ranges.sort()

    # Merge intervals
    merged = []
    for a, b in ranges:
        if not merged or a > merged[-1][1] + 1:
            merged.append([a, b])
        else:
            merged[-1][1] = max(merged[-1][1], b)

    # Count total number of integers covered
    total = 0
    for a, b in merged:
        total += (b - a + 1)

    return total


if __name__ == "__main__":
    input_file = "quizday5.txt"
    result = count_all_fresh_ids(input_file)
    print("Day 5 Part 2 Answer:", result)
