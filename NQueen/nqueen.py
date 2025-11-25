import random

def conflicts(state):
    n = len(state)
    c = 0
    for i in range(n):
        for j in range(i+1, n):
            if state[i] == state[j] or abs(state[i]-state[j]) == j-i:
                c += 1
    return c

def print_grid(state):
    n = len(state)
    for r in range(n):
        row = ""
        for c in range(n):
            row += "Q " if state[c] == r else ". "
        print(row)
    print()

def hill_climb(n):
    state = [random.randint(0,n-1) for _ in range(n)]
    step = 0
    print(f"Step {step}: conflicts = {conflicts(state)}")
    print_grid(state)

    while True:
        current_conflicts = conflicts(state)
        if current_conflicts == 0:
            print("Solution found!")
            return state

        neighbors = []
        for col in range(n):
            for row in range(n):
                if row != state[col]:
                    new_state = state[:]
                    new_state[col] = row
                    neighbors.append(new_state)

        neighbor = min(neighbors, key=conflicts)
        neighbor_conflicts = conflicts(neighbor)

        if neighbor_conflicts >= current_conflicts:
            print("No solution found (local maximum).")
            return None

        state = neighbor
        step += 1
        print(f"Step {step}: conflicts = {neighbor_conflicts}")
        print_grid(state)

hill_climb(4)
