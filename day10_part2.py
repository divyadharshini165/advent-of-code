# day10_part2.py
# Fully correct solver for Advent of Code 2025 - Day 10 Part 2
# Uses Integer Linear Programming (PuLP)

import re
import pulp

def parse_input(filename):
    machines = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Extract target vector { ... }
            target = list(map(int, re.findall(r"\{([0-9,]+)\}", line)[0].split(",")))

            # Extract all button groups before it
            groups = re.findall(r"\(([0-9,]+)\)", line)
            buttons = []
            for g in groups:
                nums = list(map(int, g.split(",")))
                buttons.append(nums)

            machines.append((buttons, target))
    return machines


def solve_machine(buttons, target):
    n = len(target)
    m = len(buttons)

    # ILP problem:
    prob = pulp.LpProblem("Machine", pulp.LpMinimize)

    # Decision variables: presses[j] ≥ 0 integer
    presses = [pulp.LpVariable(f"x{j}", lowBound=0, cat=pulp.LpInteger) for j in range(m)]

    # Each counter i must sum exact increments
    for i in range(n):
        prob += (
            pulp.lpSum(presses[j] for j in range(m) if i in buttons[j]) == target[i]
        )

    # Minimize total button presses
    prob += pulp.lpSum(presses)

    # Solve
    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    if pulp.LpStatus[prob.status] != "Optimal":
        raise ValueError("ILP could not find optimal solution")

    return sum(int(presses[j].value()) for j in range(m))


def solve(filename):
    machines = parse_input(filename)
    total = 0
    for buttons, target in machines:
        total += solve_machine(buttons, target)
    return total


if __name__ == "__main__":
    print(solve("quizday10.txt"))
