# Advent of Code 2025 - Day 9 Part 1
# Largest rectangle using two red tiles as opposite corners (inclusive area)

def parse_input(path):
    pts = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            x, y = map(int, line.split(","))
            pts.append((x, y))
    return pts


def largest_rectangle(points):
    best = 0
    n = len(points)
    
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]

            # Inclusive tile count
            area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)

            if area > best:
                best = area

    return best


if __name__ == "__main__":
    points = parse_input("quizday9.txt")
    result = largest_rectangle(points)
    print(result)
