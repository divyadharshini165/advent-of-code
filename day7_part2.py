#!/usr/bin/env python3
import os
from collections import defaultdict

def load_input():
    # Automatically read quizday7.txt from same directory
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "quizday7.txt")

    with open(path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    width = max(len(r) for r in lines)
    return [r.ljust(width, " ") for r in lines]


def solve(grid):
    H = len(grid)
    W = len(grid[0])

    # Find S
    start_r = start_c = None
    for r in range(H):
        c = grid[r].find("S")
        if c != -1:
            start_r, start_c = r, c
            break

    if start_r is None:
        raise ValueError("Start 'S' not found")

    # beams[col] = number of timelines entering this row at column col
    beams = defaultdict(int)
    beams[start_c] = 1

    # Process rows below S
    for r in range(start_r + 1, H):
        current = dict(beams)

        # Process same-row splitting until stable
        while True:
            next_beams = defaultdict(int)
            changed = False

            for col, count in current.items():
                if col < 0 or col >= W:
                    continue  # out of bounds horizontally

                cell = grid[r][col]

                if cell == "^":
                    # Split count timelines into left + right
                    if col - 1 >= 0:
                        next_beams[col - 1] += count
                    if col + 1 < W:
                        next_beams[col + 1] += count
                    changed = True
                else:
                    # Timeline continues downward
                    next_beams[col] += count

            if not changed:
                beams = next_beams
                break

            current = next_beams

    # All timelines that reach the row after the last line are final
    return sum(beams.values())


if __name__ == "__main__":
    grid = load_input()
    result = solve(grid)
    print(result)
