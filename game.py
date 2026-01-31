from __future__ import annotations

from random import choice

EMPTY = " "
PLAYER_SYMBOL = "O"
COMPUTER_SYMBOL = "X"
Board = list[list[str]]
Position = tuple[int, int]


def new_board() -> Board:
    return [[EMPTY for _ in range(3)] for _ in range(3)]


def make_list_of_free_fields(board: Board) -> list[Position]:
    return [(row, col) for row in range(3) for col in range(3) if board[row][col] == EMPTY]


def victory_for(board: Board, symbol: str) -> bool:
    for i in range(3):
        if all(board[i][j] == symbol for j in range(3)):
            return True
        if all(board[j][i] == symbol for j in range(3)):
            return True

    if all(board[i][i] == symbol for i in range(3)):
        return True
    if all(board[i][2 - i] == symbol for i in range(3)):
        return True

    return False


def apply_move(board: Board, position: Position, symbol: str) -> None:
    row, col = position
    board[row][col] = symbol


def draw_move(board: Board) -> Position | None:
    return choose_ai_move(board, level="easy")


def _find_winning_move(board: Board, symbol: str) -> Position | None:
    for position in make_list_of_free_fields(board):
        row, col = position
        board[row][col] = symbol
        try:
            if victory_for(board, symbol):
                return position
        finally:
            board[row][col] = EMPTY
    return None


def _minimax(board: Board, maximizing: bool) -> int:
    if victory_for(board, COMPUTER_SYMBOL):
        return 1
    if victory_for(board, PLAYER_SYMBOL):
        return -1
    if is_draw(board):
        return 0

    if maximizing:
        best_score = -2
        for position in make_list_of_free_fields(board):
            row, col = position
            board[row][col] = COMPUTER_SYMBOL
            score = _minimax(board, maximizing=False)
            board[row][col] = EMPTY
            best_score = max(best_score, score)
        return best_score

    best_score = 2
    for position in make_list_of_free_fields(board):
        row, col = position
        board[row][col] = PLAYER_SYMBOL
        score = _minimax(board, maximizing=True)
        board[row][col] = EMPTY
        best_score = min(best_score, score)
    return best_score


def choose_ai_move(board: Board, level: str) -> Position | None:
    free_fields = make_list_of_free_fields(board)
    if not free_fields:
        return None

    normalized = level.strip().lower()

    if normalized == "easy":
        position = choice(free_fields)
        apply_move(board, position, COMPUTER_SYMBOL)
        return position

    if normalized == "mid":
        winning_move = _find_winning_move(board, COMPUTER_SYMBOL)
        if winning_move is not None:
            apply_move(board, winning_move, COMPUTER_SYMBOL)
            return winning_move

        blocking_move = _find_winning_move(board, PLAYER_SYMBOL)
        if blocking_move is not None:
            apply_move(board, blocking_move, COMPUTER_SYMBOL)
            return blocking_move

        position = choice(free_fields)
        apply_move(board, position, COMPUTER_SYMBOL)
        return position

    best_score = -2
    best_moves: list[Position] = []
    for position in free_fields:
        row, col = position
        board[row][col] = COMPUTER_SYMBOL
        score = _minimax(board, maximizing=False)
        board[row][col] = EMPTY
        if score > best_score:
            best_score = score
            best_moves = [position]
        elif score == best_score:
            best_moves.append(position)

    position = choice(best_moves)
    apply_move(board, position, COMPUTER_SYMBOL)
    return position


def is_draw(board: Board) -> bool:
    return not make_list_of_free_fields(board)
