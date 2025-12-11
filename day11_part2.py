from collections import defaultdict
import sys

sys.setrecursionlimit(10**7)

INPUT_FILE = "quizday11.txt"

def parse_graph(lines):
    graph = defaultdict(list)
    for line in lines:
        if ":" not in line:
            continue
        a, b = line.split(":")
        a = a.strip()
        outs = b.strip().split()
        graph[a] = outs
    return graph


# Count paths from svr -> out that visit BOTH dac and fft
def count_paths_with_constraints(graph):
    memo = {}   # memo[(node, has_dac, has_fft)] = count

    def dfs(node, has_dac, has_fft):
        key = (node, has_dac, has_fft)
        if key in memo:
            return memo[key]

        # Reached target
        if node == "out":
            memo[key] = 1 if (has_dac and has_fft) else 0
            return memo[key]

        total = 0
        for nxt in graph.get(node, []):
            total += dfs(
                nxt,
                has_dac or (nxt == "dac"),
                has_fft or (nxt == "fft")
            )

        memo[key] = total
        return total

    return dfs("svr", False, False)


def main():
    with open(INPUT_FILE, "r") as f:
        lines = f.read().strip().splitlines()

    graph = parse_graph(lines)
    result = count_paths_with_constraints(graph)
    print(result)


if __name__ == "__main__":
    main()
