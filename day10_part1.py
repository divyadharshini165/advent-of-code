import re

INPUT_PATH = "quizday10.txt"   # ← put your puzzle input file here


def parse_line(line):
    # Extract pattern, button groups (ignore joltage)
    pat = re.search(r'\[([.#]+)\]', line).group(1)
    buttons = re.findall(r'\(([^)]*)\)', line)

    btn_lists = []
    for b in buttons:
        b = b.strip()
        if b == "":
            btn_lists.append([])
        else:
            btn_lists.append([int(x) for x in b.split(',') if x != ""])
    return pat, btn_lists


def min_presses_for_machine(pat, btn_lists):
    m = len(pat)
    n = len(btn_lists)

    # Build matrix rows as bitmasks
    row_masks = []
    rhs = []
    for i, ch in enumerate(pat):
        mask = 0
        for j, btn in enumerate(btn_lists):
            if i in btn:
                mask |= (1 << j)
        row_masks.append(mask)
        rhs.append(1 if ch == '#' else 0)

    # Gaussian elimination on GF(2)
    row_masks = list(row_masks)
    rhs = list(rhs)
    pivot_row_for_col = [-1] * n

    r = 0
    for c in range(n):
        sel = None
        for i in range(r, m):
            if (row_masks[i] >> c) & 1:
                sel = i
                break
        if sel is None:
            continue

        # Swap to put pivot in row r
        row_masks[r], row_masks[sel] = row_masks[sel], row_masks[r]
        rhs[r], rhs[sel] = rhs[sel], rhs[r]
        pivot_row_for_col[c] = r

        # Eliminate everywhere else
        for i in range(m):
            if i != r and ((row_masks[i] >> c) & 1):
                row_masks[i] ^= row_masks[r]
                rhs[i] ^= rhs[r]

        r += 1
        if r == m:
            break

    # Check impossible rows
    for i in range(m):
        if row_masks[i] == 0 and rhs[i] == 1:
            return None

    # Free vars
    free_cols = [c for c in range(n) if pivot_row_for_col[c] == -1]
    k = len(free_cols)

    def build_solution(free_bits):
        x = [0] * n
        for idx, c in enumerate(free_cols):
            x[c] = (free_bits >> idx) & 1

        for c in reversed(range(n)):
            rrow = pivot_row_for_col[c]
            if rrow == -1:
                continue

            mask = row_masks[rrow] & ~(1 << c)
            parity = 0
            for j in range(n):
                if (mask >> j) & 1:
                    parity ^= x[j]

            x[c] = rhs[rrow] ^ parity

        return x

    best_weight = None

    for bits in range(1 << k):
        sol = build_solution(bits)
        w = sum(sol)
        if best_weight is None or w < best_weight:
            best_weight = w

    return best_weight if best_weight is not None else 0


def main():
    total = 0
    with open(INPUT_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            pat, btns = parse_line(line)
            mp = min_presses_for_machine(pat, btns)
            total += mp

    print("ANSWER:", total)


if __name__ == "__main__":
    main()
