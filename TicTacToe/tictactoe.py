HUMAN = 'X'
AI ='O'
EMPTY = ' '
WIN =[[0,1,2],[3,4,5],[6,7,8],[0,4,8],[2,4,6],[0,3,6],[1,4,7],[2,5,8]]

def checkWin(b):
    for w in WIN:
        if b[w[0]] != EMPTY and b[w[0]] == b[w[1]] == b[w[2]]:
            return b[w[0]]
    return None

def minimax(b,ai_turn):
    winner = checkWin(b)
    if winner == HUMAN : return -1
    if winner == AI : return 1
    if EMPTY not in b : return 0 
    if ai_turn:
        best = -float('inf')
        for i in range(9):
            if b[i] == EMPTY:
                b[i] = AI 
                best = max(best,minimax(b,False))
                b[i]=EMPTY 
        return best 
    else:
        best=float('inf')
        for i in range(9):
            if b[i] == EMPTY:
                b[i] = HUMAN 
                best = min(best,minimax(b,True))
                b[i]=EMPTY 
        return best 

def ai_move(b):
    move=-1
    score=-float('inf')
    for i in range(9):
        if b[i] == EMPTY:
            b[i] = AI 
            best = minimax(b,False)
            b[i]=EMPTY
            if best > score:
                score = best
                move = i 
    return move

def print_board(b):
    print("\n")
    for i in range(3):
        print(" | ".join(b[i*3:(i+1)*3]))
        if i < 2:
            print("---------")
    print("\n")

def main():
    board = [EMPTY] * 9
    print("Welcome to Tic-Tac-Toe!")
    print("You are 'X', AI is 'O'.")
    print("Enter your move (0-8):")
    print("0 | 1 | 2\n3 | 4 | 5\n6 | 7 | 8")

    turn = input("Do you want to go first? (y/n): ").lower()
    human_turn = True if turn == 'y' else False

    while True:
        print_board(board)
        winner = checkWin(board)
        if winner:
            print(f"{winner} wins!")
            break
        if EMPTY not in board:
            print("It's a draw!")
            break

        if human_turn:
            try:
                move = int(input("Enter your move (0-8): "))
                if board[move] != EMPTY:
                    print("Invalid move. Try again.")
                    continue
                board[move] = HUMAN
            except (ValueError, IndexError):
                print("Invalid input. Try a number from 0 to 8.")
                continue
        else:
            print("AI is thinking...")
            move = ai_move(board)
            board[move] = AI

        human_turn = not human_turn

if __name__ == "__main__":
    main()
