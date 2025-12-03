def max_12_digit_joltage(line: str) -> int:
    digits = list(line.strip())
    n = len(digits)
    k = 12

    stack = []

    for i, d in enumerate(digits):
        # Remove smaller digits if we can still form 12 digits later
        while stack and stack[-1] < d and len(stack) + (n - i) > k:
            stack.pop()

        # Add digit if we still need more digits
        if len(stack) < k:
            stack.append(d)

    return int("".join(stack))


def main():
    filename = "quizday3.txt"
    total = 0

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                total += max_12_digit_joltage(line)

    print("Total Output Joltage (Part 2) =", total)


if __name__ == "__main__":
    main()
