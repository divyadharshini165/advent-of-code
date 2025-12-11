from collections import defaultdict
import sys
sys.setrecursionlimit(1000000)

def parse_graph(lines):
    g = defaultdict(list)
    for line in lines:
        if ":" not in line:
            continue
        a, b = line.split(":")
        a = a.strip()
        outs = b.strip().split()
        g[a] = outs
    return g

def count_paths(g, start="you", end="out"):
    memo = {}          # memo[node] = number of paths from node to out
    visited = set()

    def dfs(node):
        if node == end:
            return 1
        if node in memo:
            return memo[node]

        visited.add(node)
        total = 0

        for nxt in g[node]:
            if nxt not in visited:
                total += dfs(nxt)

        visited.remove(node)
        memo[node] = total
        return total

    return dfs(start)

if __name__ == "__main__":
    # change filename here if needed
    INPUT_FILE = "quizday11.txt"

    with open(INPUT_FILE, "r") as f:
        lines = f.read().strip().splitlines()

    g = parse_graph(lines)
    result = count_paths(g)
    print(result)
