def solve_day6_part2(path):
    # Read input
    with open(path) as f:
        lines = [line.rstrip('\n') for line in f]

    # Remove trailing empty lines
    while lines and lines[-1].strip() == '':
        lines.pop()

    ops_line = lines[-1]                 # bottom operator row
    num_lines = lines[:-1]               # everything above operators
    width = len(ops_line)

    # Pad rows so they all have same width
    num_lines = [row.ljust(width) for row in num_lines]
    height = len(num_lines)

    # --- Identify separator columns (all spaces) ---
    sep = [all(row[c] == ' ' for row in num_lines) for c in range(width)]

    # --- Find contiguous non-separator column ranges (the problems) ---
    segments = []
    c = 0
    while c < width:
        if not sep[c]:
            start = c
            while c < width and not sep[c]:
                c += 1
            segments.append((start, c))  # [start, end)
        else:
            c += 1

    # --- Helper: read a single column as a number (top->bottom digits) ---
    def read_column_number(col):
        digits = []
        for r in range(height):
            ch = num_lines[r][col]
            if ch.isdigit():
                digits.append(ch)
        if not digits:
            return None
        return int("".join(digits))

    total = 0

    # --- For each problem ---
    for start, end in segments:

        # Find operator in this segment
        op = None
        for col in range(start, end):
            if ops_line[col] in "+*":
                op = ops_line[col]
                break
        if op is None:
            continue

        # === PART 2 CHANGE: read numbers right-to-left by column ===
        numbers = []
        for col in range(end - 1, start - 1, -1):
            n = read_column_number(col)
            if n is not None:
                numbers.append(n)

        # Compute the problem value
        if op == "+":
            value = sum(numbers)
        else:
            value = 1
            for n in numbers:
                value *= n

        total += value

    return total


# Example usage:
print(solve_day6_part2("quizday6.txt"))
