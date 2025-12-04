def load_grid(filename):
    with open(filename, "r") as f:
        return [list(line.strip()) for line in f if line.strip()]


def count_neighbors(r, c, grid):
    rows = len(grid)
    cols = len(grid[0])

    directions = [
        (-1,-1), (-1,0), (-1,1),
        (0,-1),         (0,1),
        (1,-1),  (1,0), (1,1)
    ]

    count = 0
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            if grid[nr][nc] == '@':
                count += 1
    return count


def simulate_removal(grid):
    rows = len(grid)
    cols = len(grid[0])
    total_removed = 0

    while True:
        removable = []

        # Find all removable rolls
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '@':
                    if count_neighbors(r, c, grid) < 4:
                        removable.append((r, c))

        if not removable:
            break  # stop when no accessible rolls left

        # Remove all at once
        for r, c in removable:
            grid[r][c] = '.'

        total_removed += len(removable)

    return total_removed


if __name__ == "__main__":
    grid = load_grid("quizday4.txt")
    answer = simulate_removal(grid)
    print("Total rolls removed:", answer)
