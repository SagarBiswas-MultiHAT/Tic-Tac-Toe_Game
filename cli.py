from __future__ import annotations

from random import choice
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
    print("\n==> Let's start!\n")


def prompt_difficulty(input_fn: Callable[[str], str]) -> str:
    options = {"easy", "mid", "hard"}
    while True:
        choice = input_fn("Choose AI level (easy, mid, hard): ").strip().lower()
        if choice in options:
            return choice
        print("Invalid choice. Please enter easy, mid, or hard.")


def prompt_total_matches(input_fn: Callable[[str], str]) -> int:
    while True:
        try:
            total = int(input_fn("Total matches (e.g., 3, 5, 7): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if total >= 1:
            return total

        print("Please enter a number greater than 0.")


def play_match(
    difficulty: str,
    starter: str,
    input_fn: Callable[[str], str],
) -> str | None:
    board = new_board()
    human_turn = starter == PLAYER_SYMBOL

    if starter == COMPUTER_SYMBOL:
        choose_ai_move(board, difficulty)
        human_turn = True

    while True:
        display_board(board)

        if human_turn:
            enter_move(board, input_fn)
            if victory_for(board, PLAYER_SYMBOL):
                display_board(board)
                print("\n..:: Congratulations! You won this match!\n")
                return PLAYER_SYMBOL
        else:
            choose_ai_move(board, difficulty)
            if victory_for(board, COMPUTER_SYMBOL):
                display_board(board)
                print("\n:( Sorry, I won this match!\n")
                return COMPUTER_SYMBOL

        if is_draw(board):
            display_board(board)
            print("\n:) This match is a draw!\n")
            return None

        human_turn = not human_turn


def run_game(input_fn: Callable[[str], str] = input) -> None:
    print_instructions()

    difficulty = prompt_difficulty(input_fn)
    total_matches = prompt_total_matches(input_fn)
    first_starter = choice([PLAYER_SYMBOL, COMPUTER_SYMBOL])
    first_starter_text = "You (O)" if first_starter == PLAYER_SYMBOL else "Computer (X)"
    print(
        "Randomly chosen starter for Match 1: "
        f"{first_starter_text}\n"
    )

    human_wins = 0
    computer_wins = 0
    draws = 0
    current_starter = first_starter

    for match in range(1, total_matches + 1):
        print(f"--- Match {match}/{total_matches} ---")
        winner = play_match(difficulty, current_starter, input_fn)
        if winner == PLAYER_SYMBOL:
            human_wins += 1
        elif winner == COMPUTER_SYMBOL:
            computer_wins += 1
        else:
            draws += 1

        current_starter = (
            PLAYER_SYMBOL if current_starter == COMPUTER_SYMBOL else COMPUTER_SYMBOL
        )

    print("\n=== Final Results ===")
    print(f"You (O): {human_wins}")
    print(f"Computer (X): {computer_wins}")
    print(f"Draws: {draws}\n")

    if human_wins > computer_wins:
        print("..:: You win the series! Great job! ::..\n")
    elif computer_wins > human_wins:
        print("..:: Computer wins the series. Try again! ::..\n")
    else:
        print("..:: The series is a draw! ::..\n")


def main() -> None:
    run_game()


if __name__ == "__main__":
    main()
