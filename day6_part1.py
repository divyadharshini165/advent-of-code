def solve_day6_part1(path):
    # Read input
    with open(path) as f:
        lines = [line.rstrip('\n') for line in f]

    # Remove trailing blank lines
    while lines and lines[-1].strip() == '':
        lines.pop()

    ops_line = lines[-1]
    number_lines = lines[:-1]
    width = len(ops_line)

    # Pad number rows
    number_lines = [row.ljust(width) for row in number_lines]

    # Identify separator columns (all spaces)
    sep = [all(row[c] == ' ' for row in number_lines) for c in range(width)]

    # Find non-separator column groups (problems)
    segments = []
    c = 0
    while c < width:
        if not sep[c]:
            start = c
            while c < width and not sep[c]:
                c += 1
            segments.append((start, c))
        else:
            c += 1

    def extract_numbers(start, end):
        nums = []
        for row in number_lines:
            s = row[start:end].strip()
            if s:
                digits = ''.join(ch for ch in s if ch.isdigit())
                if digits:
                    nums.append(int(digits))
        return nums

    total = 0

    for start, end in segments:
        # Find op
        op = None
        for i in range(start, end):
            if ops_line[i] in '+*':
                op = ops_line[i]
                break
        if op is None:
            continue

        nums = extract_numbers(start, end)

        if op == '+':
            val = sum(nums)
        else:
            val = 1
            for n in nums:
                val *= n

        total += val

    return total


print(solve_day6_part1("quizday6.txt"))
