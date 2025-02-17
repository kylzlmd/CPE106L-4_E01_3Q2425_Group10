# tictactoe.py

def print_board (board): 
    for row in board:
        print(" | ".join(row)) 
        print("-" * 9)

def check_win (board, player):
    win_condition = [player, player, player] 
    for row in board:
        if row == win_condition:
            return True
    for col in range(3):
        if [board[row][col] for row in range(3)] == win_condition: 
            return True
    if [board[i][i] for i in range(3)] == win_condition: 
        return True
    if [board[i][2-i] for i in range(3)] == win_condition: 
        return True
    return False

def tic_tac_toe(): 
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ['X', '0']
    turn = 0

    while True: 
        print_board(board)
        player = players[turn % 2]
        print(f"Player {player}'s turn.")

        while True:
            try:
                row = int(input("Enter row (0-2): "))
                col = int(input("Enter column (0-2): ")) 
                if board[row][col] == " ":
                    board[row][col] = player
                    break
                else:
                    print("That spot is taken! Try again.")
            except (ValueError, IndexError):
                print("Invalid input! Please enter numbers between 0 and 2.")
            
        if check_win (board, player):
            print_board (board)
            print(f"Player {player} wins!")
            break
        elif all(board[row][col] != " " for row in range(3) for col in range(3)):
            print_board(board)
            print("It's a tie!")
            break

        turn += 1

if __name__ == "__main__":
    tic_tac_toe()


