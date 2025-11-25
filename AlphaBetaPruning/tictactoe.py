import math

def print_board(b):
    for r in range(3):
        print(" | ".join(b[r]))
    print()

def empty_cells(b):
    return [(i,j) for i in range(3) for j in range(3) if b[i][j] == "_"]

def check_win(b):
    lines = [
        [b[0][0], b[0][1], b[0][2]],
        [b[1][0], b[1][1], b[1][2]],
        [b[2][0], b[2][1], b[2][2]],
        [b[0][0], b[1][0], b[2][0]],
        [b[0][1], b[1][1], b[2][1]],
        [b[0][2], b[1][2], b[2][2]],
        [b[0][0], b[1][1], b[2][2]],
        [b[0][2], b[1][1], b[2][0]]
    ]
    for line in lines:
        if line == ["X","X","X"]:
            return "X"
        if line == ["O","O","O"]:
            return "O"
    return None

def minimax(b, depth, alpha, beta, is_max):
    r = check_win(b)
    if r == "O": return 1
    if r == "X": return -1
    if not empty_cells(b): return 0
    if is_max:
        best = -math.inf
        for i,j in empty_cells(b):
            b[i][j] = "O"
            val = minimax(b, depth+1, alpha, beta, False)
            b[i][j] = "_"
            best = max(best, val)
            alpha = max(alpha, best)
            if beta <= alpha: break
        return best
    else:
        best = math.inf
        for i,j in empty_cells(b):
            b[i][j] = "X"
            val = minimax(b, depth+1, alpha, beta, True)
            b[i][j] = "_"
            best = min(best, val)
            beta = min(beta, best)
            if beta <= alpha: break
        return best

def best_move(b):
    best = -math.inf
    move = None
    for i,j in empty_cells(b):
        b[i][j] = "O"
        val = minimax(b, 0, -math.inf, math.inf, False)
        b[i][j] = "_"
        if val > best:
            best = val
            move = (i,j)
    return move

board = [["_"]*3 for _ in range(3)]
turn = "X"

print("Board cells: 0-8 as follows:")
print("0 | 1 | 2\n3 | 4 | 5\n6 | 7 | 8\n")

while True:
    print_board(board)
    if check_win(board) == "X":
        print("Human wins")
        break
    if check_win(board) == "O":
        print("AI wins")
        break
    if not empty_cells(board):
        print("Draw")
        break

    if turn == "X":
        move = int(input("Enter cell 0-8: "))
        r, c = divmod(move, 3)
        if board[r][c] == "_":
            board[r][c] = "X"
            turn = "O"
    else:
        r,c = best_move(board)
        board[r][c] = "O"
        turn = "X"
