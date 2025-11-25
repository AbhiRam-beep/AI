import random
import math

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

def simulated_annealing(n, max_steps=1000, t_start=10.0, alpha=0.95):
    state = [random.randint(0,n-1) for _ in range(n)]
    t = t_start
    step = 0

    print(f"Step {step}: conflicts = {conflicts(state)}")
    print_grid(state)

    for step in range(1, max_steps+1):
        current_conflicts = conflicts(state)
        if current_conflicts == 0:
            print("Solution found!")
            return state

        col = random.randint(0,n-1)
        row = random.randint(0,n-1)
        if row == state[col]:
            continue
        new_state = state[:]
        new_state[col] = row
        new_conflicts = conflicts(new_state)

        delta = new_conflicts - current_conflicts
        if delta < 0 or random.random() < math.exp(-delta/t):
            state = new_state

        t *= alpha

        print(f"Step {step}: conflicts = {conflicts(state)}")
        print_grid(state)

    print("No solution found within step limit.")
    return None

simulated_annealing(4)
