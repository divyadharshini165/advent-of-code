#!/usr/bin/env python3
from bisect import bisect_left
from itertools import combinations

# -----------------------------------------------------------
# LOAD INPUT (list of red vertex coordinates in order)
# -----------------------------------------------------------
pts = []
with open("quizday9.txt") as f:
    for line in f:
        if line.strip():
            x, y = map(int, line.split(","))
            pts.append((x, y))

poly = pts[:]          # polygon in order
reds_list = list(set(pts))
n = len(pts)

print("Loaded", n, "red vertices")

# -----------------------------------------------------------
# BUILD COMPRESSED COORDINATES
# -----------------------------------------------------------
xs_set = set()
ys_set = set()

for x, y in pts:
    xs_set.add(x)
    xs_set.add(x + 1)      # tile boundary
    ys_set.add(y)
    ys_set.add(y + 1)

# also add padding around bounding box
minx = min(x for x, y in pts)
maxx = max(x for x, y in pts)
miny = min(y for x, y in pts)
maxy = max(y for x, y in pts)

xs_set.add(minx - 1)
xs_set.add(maxx + 2)
ys_set.add(miny - 1)
ys_set.add(maxy + 2)

xs = sorted(xs_set)
ys = sorted(ys_set)
nx = len(xs)
ny = len(ys)

print("Compressed size:", nx, "x", ny)

# We fill inside[] grid of size (nx-1) × (ny-1)
inside = [[0] * (ny - 1) for _ in range(nx - 1)]

# -----------------------------------------------------------
# SCANLINE FILL — DETECT INTERIOR REGIONS OF POLYGON
# -----------------------------------------------------------
def edge_intersections(yline):
    """Return sorted x-intersections of the horizontal line y=yline with polygon edges."""
    out = []
    m = len(poly)
    for i in range(m):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % m]

        if y1 == y2:        # ignore horizontal edges
            continue

        # half-open intersection
        if (y1 <= yline < y2) or (y2 <= yline < y1):
            xi = x1 + (yline - y1) * (x2 - x1) / (y2 - y1)
            out.append(xi)

    out.sort()
    return out


from bisect import bisect_left
import time

start = time.time()

for j in range(ny - 1):
    ymid = (ys[j] + ys[j + 1]) / 2.0
    xints = edge_intersections(ymid)

    # pair them into fill intervals
    for k in range(0, len(xints), 2):
        if k + 1 >= len(xints):
            break
        xa = xints[k]
        xb = xints[k + 1]

        # find candidate x-interval start
        i_left = bisect_left(xs, xa)
        if i_left > 0 and xs[i_left] > xa:
            i_left -= 1

        i = i_left
        while i < nx - 1:
            xmid = (xs[i] + xs[i + 1]) / 2.0
            if xmid <= xa:
                i += 1
                continue
            if xmid < xb:
                inside[i][j] = 1
                i += 1
            else:
                break

print("Scanline fill done in", time.time() - start, "seconds")

# -----------------------------------------------------------
# INCLUDE BOUNDARY CELLS (tile centers exactly on polygon edges)
# -----------------------------------------------------------
def point_on_segment(a, p, b):
    """Check if point p lies exactly on segment a–b."""
    (x1, y1) = a
    (x2, y2) = p
    (x3, y3) = b

    # collinearity
    if (x2 - x1) * (y3 - y1) != (y2 - y1) * (x3 - x1):
        return False

    # bounding box
    if min(x1, x3) <= x2 <= max(x1, x3) and min(y1, y3) <= y2 <= max(y1, y3):
        return True

    return False

for i in range(nx - 1):
    xmid = (xs[i] + xs[i + 1]) / 2.0
    for j in range(ny - 1):
        if inside[i][j]:
            continue
        ymid = (ys[j] + ys[j + 1]) / 2.0

        for k in range(len(poly)):
            if point_on_segment(poly[k], (xmid, ymid), poly[(k + 1) % len(poly)]):
                inside[i][j] = 1
                break

# -----------------------------------------------------------
# PREFIX SUM ARRAY FOR O(1) RECTANGLE CHECKS
# -----------------------------------------------------------
W = nx - 1
H = ny - 1

ps = [[0] * (H + 1) for _ in range(W + 1)]

for i in range(W):
    run = 0
    for j in range(H):
        run += inside[i][j]
        ps[i + 1][j + 1] = ps[i][j + 1] + run

def rect_sum(ix1, ix2, jy1, jy2):
    """Sum of inside[] in rectangular region."""
    return ps[ix2][jy2] - ps[ix1][jy2] - ps[ix2][jy1] + ps[ix1][jy1]

def ix(x): return bisect_left(xs, x)
def iy(y): return bisect_left(ys, y)

# -----------------------------------------------------------
# TEST ALL RED–RED OPPOSITE CORNER PAIRS
# -----------------------------------------------------------
best_area = 0
best_rect = None

import time
start = time.time()
count = 0

for (x1, y1), (x2, y2) in combinations(reds_list, 2):
    if x1 == x2 or y1 == y2:
        continue

    xmin, xmax = sorted([x1, x2])
    ymin, ymax = sorted([y1, y2])

    ix1 = ix(xmin)
    ix2 = ix(xmax + 1)
    jy1 = iy(ymin)
    jy2 = iy(ymax + 1)

    total = (ix2 - ix1) * (jy2 - jy1)
    s = rect_sum(ix1, ix2, jy1, jy2)

    if s == total:
        area = (xmax - xmin + 1) * (ymax - ymin + 1)
        if area > best_area:
            best_area = area
            best_rect = (xmin, ymin, xmax, ymax)

    count += 1

print("Checked pairs:", count, "in", time.time() - start, "seconds")
print("Largest rectangle area:", best_area)
print("Best rectangle corners (xmin, ymin, xmax, ymax):", best_rect)
