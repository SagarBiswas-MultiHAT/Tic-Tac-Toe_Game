from __future__ import annotations

from typing import Callable

from game import (
    Board,
    COMPUTER_SYMBOL,
    EMPTY,
    PLAYER_SYMBOL,
    apply_move,
    choose_ai_move,
    is_draw,
    new_board,
    victory_for,
)


def display_board(board: Board, printer: Callable[[str], None] = print) -> None:
    printer("+-------" * 3 + "+")
    for row in board:
        printer("|       " * 3 + "|")
        printer("".join(f"|   {cell}   " for cell in row) + "|")
        printer("|       " * 3 + "|")
        printer("+-------" * 3 + "+")


def prompt_move(input_fn: Callable[[str], str]) -> int:
    while True:
        try:
            move = int(input_fn("\nEnter your move (1-9): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if 1 <= move <= 9:
            return move

        print("Invalid move. Enter a number between 1 and 9.")


def enter_move(board: Board, input_fn: Callable[[str], str] = input) -> None:
    while True:
        move = prompt_move(input_fn)
        row, col = divmod(move - 1, 3)
        if board[row][col] == EMPTY:
            apply_move(board, (row, col), PLAYER_SYMBOL)
            return
        print("Field already occupied. Try again.")


def print_instructions() -> None:
    print("\n..:: This is the game of Tic-Tac-Toe. You play 'O' and I play 'X'.\n")
    print(
        """ \t\t+-------+-------+-------+
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
"""
    )
    print("System will make the first move. Just enter the number of the field you want to occupy.\n")
    print("\n==> Let's start!\n")


def prompt_difficulty(input_fn: Callable[[str], str]) -> str:
    options = {"easy", "mid", "hard"}
    while True:
        choice = input_fn("Choose AI level (easy, mid, hard): ").strip().lower()
        if choice in options:
            return choice
        print("Invalid choice. Please enter easy, mid, or hard.")


def run_game(input_fn: Callable[[str], str] = input) -> None:
    print_instructions()

    difficulty = prompt_difficulty(input_fn)

    board = new_board()
    choose_ai_move(board, difficulty)
    human_turn = True

    while True:
        display_board(board)

        if human_turn:
            enter_move(board, input_fn)
            if victory_for(board, PLAYER_SYMBOL):
                display_board(board)
                print("\n..:: Congratulations! You won!\n")
                return
        else:
            choose_ai_move(board, difficulty)
            if victory_for(board, COMPUTER_SYMBOL):
                display_board(board)
                print("\n:( Sorry, I won!\n")
                return

        if is_draw(board):
            display_board(board)
            print("\n:) It's a draw!\n")
            return

        human_turn = not human_turn


def main() -> None:
    run_game()


if __name__ == "__main__":
    main()
