import math
from itertools import combinations

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
# Compute all pair distances (squared)
# -------------------------
pairs = []

for i in range(n):
    x1, y1, z1 = coords[i]
    for j in range(i+1, n):
        x2, y2, z2 = coords[j]
        dx = x1 - x2
        dy = y1 - y2
        dz = z1 - z2
        dist2 = dx*dx + dy*dy + dz*dz
        pairs.append((dist2, i, j))

# Sort by distance
pairs.sort(key=lambda x: x[0])

# -------------------------
# Connect until everything is in one circuit
# -------------------------
dsu = DSU(n)
remaining_components = n

last_a = last_b = None

for dist, a, b in pairs:
    if dsu.union(a, b):
        remaining_components -= 1
        last_a, last_b = a, b
        
        if remaining_components == 1:
            break

# Extract X coordinates of last connected pair
x1 = coords[last_a][0]
x2 = coords[last_b][0]

print("Last connection X coords:", x1, x2)
print("Answer:", x1 * x2)
