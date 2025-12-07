#!/usr/bin/env python3
from collections import deque
import os

def load_input():
    # Auto-load quizday7.txt from the same directory as this script
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "quizday7.txt")

    with open(path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    width = max(len(r) for r in lines)
    return [r.ljust(width, " ") for r in lines]

def solve(grid):
    H = len(grid)
    W = len(grid[0])

    # find S
    start = None
    for r in range(H):
        c = grid[r].find("S")
        if c != -1:
            start = (r, c)
            break
    if start is None:
        raise ValueError("Start 'S' not found")

    beams = set([start])
    splits = 0

    # simulate until no beams remain
    while beams:
        next_beams = set()
        for (r, c) in beams:
            nr = r + 1
            if nr >= H:
                continue

            cell_below = grid[nr][c]

            if cell_below == "^":
                splits += 1
                if c - 1 >= 0:
                    next_beams.add((nr, c - 1))
                if c + 1 < W:
                    next_beams.add((nr, c + 1))
            else:
                next_beams.add((nr, c))

        beams = next_beams

    return splits


if __name__ == "__main__":
    grid = load_input()
    ans = solve(grid)
    print(ans)
