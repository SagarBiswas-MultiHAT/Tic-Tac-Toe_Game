from random import randrange

# Constants for board symbols
EMPTY = " "
PLAYER_SYMBOL = "O"
COMPUTER_SYMBOL = "X"


def display_board(board):
    """Displays the current state of the board."""
    print("+-------" * 3 + "+")
    for row in board:
        print("|       " * 3 + "|")
        for cell in row:
            print(f"|   {cell}   ", end="")
        print("|")
        print("|       " * 3 + "|")
        print("+-------" * 3 + "+")


def enter_move(board):
    """Allows the player to make their move."""
    while True:
        try:
            move = int(input("\nEnter your move (1-9): "))
            if 1 <= move <= 9:
                row, col = divmod(move - 1, 3)
                if board[row][col] == EMPTY:
                    board[row][col] = PLAYER_SYMBOL
                    break
                else:
                    print("Field already occupied. Try again.")
            else:
                print("Invalid move. Enter a number between 1 and 9.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def make_list_of_free_fields(board):
    """Returns a list of all free positions on the board."""
    return [(row, col) for row in range(3) for col in range(3) if board[row][col] == EMPTY]


def victory_for(board, symbol):
    """Checks if the given symbol has won."""
    # Check rows and columns
    for i in range(3):
        if all(board[i][j] == symbol for j in range(3)) or all(board[j][i] == symbol for j in range(3)):
            return True

    # Check diagonals
    if all(board[i][i] == symbol for i in range(3)) or all(board[i][2 - i] == symbol for i in range(3)):
        return True

    return False


def draw_move(board):
    """Makes a random move for the computer."""
    free_fields = make_list_of_free_fields(board)
    if free_fields:
        row, col = free_fields[randrange(len(free_fields))]
        board[row][col] = COMPUTER_SYMBOL

print ("\n..:: This is the game of Tic-Tac-Toe. You play 'O' and I play 'X'.\n")
print (
''' \t\t+-------+-------+-------+
    \t\t|       |       |       |
    \t\t|   1   |   2   |   3   |
    \t\t|       |       |       |
    \t\t+-------+-------+-------+
    \t\t|       |       |       |
    \t\t|   4   |   5   |   6   |
    \t\t|       |       |       |
    \t\t+-------+-------+-------+
    \t\t|       |       |       |
    \t\t|   7   |   8   |   9   |
    \t\t|       |       |       |
    \t\t+-------+-------+-------+
''')
print("System will make the first move. Just enter the number of the field you want to occupy.\n")

print("\n==> Let's start!\n")

# Initialize the board
board = [[EMPTY for _ in range(3)] for _ in range(3)]
board[1][1] = COMPUTER_SYMBOL  # Computer starts with the center square

human_turn = True  # Start with the human player's turn

# Main game loop
while True:
    display_board(board)

    if human_turn:
        enter_move(board)
        if victory_for(board, PLAYER_SYMBOL):
            display_board(board)
            print("\n..:: Congratulations! You won!\n")
            break
    else:
        draw_move(board)
        if victory_for(board, COMPUTER_SYMBOL):
            display_board(board)
            print("\n:( Sorry, I won!\n")
            break

    if not make_list_of_free_fields(board):
        display_board(board)
        print("\n:) It's a draw!\n")
        break

    human_turn = not human_turn
