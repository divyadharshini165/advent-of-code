import math
from itertools import combinations
from collections import defaultdict

# -------------------------
# Union-Find / Disjoint Set
# -------------------------
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True

# -------------------------
# Load coordinates
# -------------------------
coords = []
with open("quizday8.txt") as f:
    for line in f:
        x, y, z = map(int, line.strip().split(","))
        coords.append((x, y, z))

n = len(coords)

# -------------------------
# Compute all pair distances
# -------------------------
pairs = []

for i in range(n):
    x1, y1, z1 = coords[i]
    for j in range(i+1, n):
        x2, y2, z2 = coords[j]
        dx = x1 - x2
        dy = y1 - y2
        dz = z1 - z2
        dist2 = dx*dx + dy*dy + dz*dz  # squared distance is enough
        pairs.append((dist2, i, j))

# Sort by distance — smallest first
pairs.sort(key=lambda x: x[0])

# -------------------------
# Connect 1000 closest pairs
# -------------------------
dsu = DSU(n)

for d, a, b in pairs[:1000]:
    dsu.union(a, b)

# -------------------------
# Count sizes of circuits
# -------------------------
comp_sizes = defaultdict(int)
for i in range(n):
    root = dsu.find(i)
    comp_sizes[root] += 1

sizes = sorted(comp_sizes.values(), reverse=True)

# Product of 3 largest
ans = sizes[0] * sizes[1] * sizes[2]

print("Answer:", ans)
