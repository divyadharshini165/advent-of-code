def max_joltage_for_line(line: str) -> int:
    digits = [int(c) for c in line.strip()]
    n = len(digits)
    best = 0

    # suffix max approach: max digit to the right for each position
    suffix_max = [0] * n
    suffix_max[-1] = digits[-1]

    for i in range(n - 2, -1, -1):
        suffix_max[i] = max(digits[i], suffix_max[i + 1])

    for i in range(n - 1):
        candidate = digits[i] * 10 + suffix_max[i + 1]
        best = max(best, candidate)

    return best


def main():
    filename = "quizday3.txt"
    total = 0

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                total += max_joltage_for_line(line)

    print("Total Output Joltage =", total)


if __name__ == "__main__":
    main()
