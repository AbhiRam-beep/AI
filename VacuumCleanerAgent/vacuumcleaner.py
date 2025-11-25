ENVIRONMENT_SIZE = 4

visited = [0] * ENVIRONMENT_SIZE 
dirty_tiles = [1] * ENVIRONMENT_SIZE 
current_pos = 0

moves = {
    0: -1,
    1: 1,
}

while sum(dirty_tiles) > 0:
    print(f"\n--- Agent is at position: {current_pos} ---")
    print(f"Dirty tiles remaining: {sum(dirty_tiles)}")
    visited[current_pos] = 1

    if dirty_tiles[current_pos] == 1:
        print(f"Action: CLEANING tile at position {current_pos}")
        dirty_tiles[current_pos] = 0
        print(f"Tile {current_pos} cleaned.")
    else:
        print(f"Tile {current_pos} is already clean.")

    if sum(dirty_tiles) == 0:
        print("\n*** GOAL ACHIEVED: All tiles are clean! ***")
        break

    next_move_index = 1
    new_pos = current_pos + moves[next_move_index]

    if 0 <= new_pos < ENVIRONMENT_SIZE:
        current_pos = new_pos
        print(f"Action: MOVED {next_move_index} (Right) to position {current_pos}")
    else:
        next_move_index = 0
        new_pos = current_pos + moves[next_move_index]

        if 0 <= new_pos < ENVIRONMENT_SIZE:
            current_pos = new_pos
            print(f"Action: MOVED {next_move_index} (Left) to position {current_pos}")
        else:
            print("ERROR: Cannot move. Agent is stuck!")
            break
