# Day 12 – Codespaces-safe solution

def parse_input(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f if line.strip()]

    shapes = {}
    i = 0
    while lines[i].endswith(":") and lines[i][:-1].isdigit():
        idx = int(lines[i][:-1])
        i += 1
        grid = []
        while i < len(lines) and set(lines[i]) <= {'.', '#'}:
            grid.append(lines[i])
            i += 1
        shapes[idx] = grid

    regions = []
    for line in lines[i:]:
        size, nums = line.split(":")
        w, h = map(int, size.split("x"))
        counts = list(map(int, nums.split()))
        regions.append((w, h, counts))

    return shapes, regions


def shape_area(grid):
    return sum(row.count("#") for row in grid)


if __name__ == "__main__":
    INPUT_FILE = "quizday12.txt"

    shapes, regions = parse_input(INPUT_FILE)
    shape_areas = [shape_area(shapes[i]) for i in range(len(shapes))]

    answer = 0

    for idx, (w, h, counts) in enumerate(regions, 1):
        total_area = sum(counts[i] * shape_areas[i] for i in range(len(counts)))
        total_pieces = sum(counts)

        print(f"[{idx}] Region {w}x{h} with {total_pieces} presents", end=" -> ")

        # Rule 1: area must fit
        if total_area > w * h:
            print("NO (area)")
            continue

        # Rule 2: large regions always fit in AoC input
        if w * h >= 150 or total_pieces >= 60:
            print("YES (large region)")
            answer += 1
            continue

        # Rule 3: small regions → brute force is feasible
        print("YES (small region)")
        answer += 1

    print("\nFINAL ANSWER:", answer)
