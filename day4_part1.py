# Day 4 Part 1 - Printing Department

def load_grid(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file.readlines()]

def count_accessible_rolls(grid):
    rows = len(grid)
    cols = len(grid[0])
    accessible = 0

    # Directions for 8 neighbors
    directions = [
        (-1,-1), (-1,0), (-1,1),
        (0,-1),         (0,1),
        (1,-1),  (1,0), (1,1)
    ]

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                neighbors = 0

                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if grid[nr][nc] == '@':
                            neighbors += 1

                if neighbors < 4:
                    accessible += 1

    return accessible


if __name__ == "__main__":
    grid = load_grid("quizday4.txt")
    result = count_accessible_rolls(grid)
    print("Accessible rolls:", result)
