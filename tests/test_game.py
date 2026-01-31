import game

from game import (
    COMPUTER_SYMBOL,
    EMPTY,
    PLAYER_SYMBOL,
    apply_move,
    choose_ai_move,
    draw_move,
    is_draw,
    make_list_of_free_fields,
    new_board,
    victory_for,
)


def test_make_list_of_free_fields_initial():
    board = new_board()
    free_fields = make_list_of_free_fields(board)
    assert len(free_fields) == 9


def test_victory_for_row():
    board = new_board()
    board[0] = [PLAYER_SYMBOL, PLAYER_SYMBOL, PLAYER_SYMBOL]
    assert victory_for(board, PLAYER_SYMBOL)


def test_victory_for_column():
    board = new_board()
    for i in range(3):
        board[i][1] = COMPUTER_SYMBOL
    assert victory_for(board, COMPUTER_SYMBOL)


def test_victory_for_diagonal():
    board = new_board()
    for i in range(3):
        board[i][i] = PLAYER_SYMBOL
    assert victory_for(board, PLAYER_SYMBOL)


def test_easy_ai_move_places_symbol():
    board = new_board()
    apply_move(board, (1, 1), PLAYER_SYMBOL)
    position = choose_ai_move(board, "easy")
    assert position is not None
    row, col = position
    assert board[row][col] == COMPUTER_SYMBOL
    assert board[row][col] != EMPTY


def test_mid_ai_blocks_immediate_win():
    board = new_board()
    board[0] = [PLAYER_SYMBOL, PLAYER_SYMBOL, EMPTY]
    position = choose_ai_move(board, "mid")
    assert position == (0, 2)


def test_hard_ai_wins_when_available():
    board = new_board()
    board[1] = [COMPUTER_SYMBOL, COMPUTER_SYMBOL, EMPTY]
    position = choose_ai_move(board, "hard")
    assert position == (1, 2)


def test_draw_move_uses_easy_ai(monkeypatch):
    board = new_board()
    monkeypatch.setattr(game, "choice", lambda free_fields: free_fields[0])
    position = draw_move(board)
    assert position == (0, 0)
    assert board[0][0] == COMPUTER_SYMBOL


def test_is_draw_full_board():
    board = [
        [PLAYER_SYMBOL, COMPUTER_SYMBOL, PLAYER_SYMBOL],
        [COMPUTER_SYMBOL, PLAYER_SYMBOL, COMPUTER_SYMBOL],
        [COMPUTER_SYMBOL, PLAYER_SYMBOL, COMPUTER_SYMBOL],
    ]
    assert is_draw(board)


def test_hard_ai_blocks_immediate_loss(monkeypatch):
    board = new_board()
    board[0] = [PLAYER_SYMBOL, PLAYER_SYMBOL, EMPTY]
    monkeypatch.setattr(game, "choice", lambda free_fields: free_fields[0])
    position = choose_ai_move(board, "hard")
    assert position == (0, 2)


def test_choose_ai_move_on_full_board_returns_none():
    board = [
        [PLAYER_SYMBOL, COMPUTER_SYMBOL, PLAYER_SYMBOL],
        [COMPUTER_SYMBOL, PLAYER_SYMBOL, COMPUTER_SYMBOL],
        [COMPUTER_SYMBOL, PLAYER_SYMBOL, COMPUTER_SYMBOL],
    ]
    assert choose_ai_move(board, "easy") is None


def test_mid_ai_uses_winning_move_when_available():
    board = new_board()
    board[2] = [COMPUTER_SYMBOL, COMPUTER_SYMBOL, EMPTY]
    position = choose_ai_move(board, "mid")
    assert position == (2, 2)


def test_mid_ai_picks_random_when_no_win_or_block(monkeypatch):
    board = new_board()
    board[0][0] = PLAYER_SYMBOL
    board[0][1] = COMPUTER_SYMBOL
    monkeypatch.setattr(game, "choice", lambda free_fields: free_fields[0])
    position = choose_ai_move(board, "mid")
    assert position == (0, 2)


def test_hard_ai_accounts_for_multiple_best_moves(monkeypatch):
    board = new_board()
    monkeypatch.setattr(game, "_minimax", lambda *_args, **_kwargs: 0)
    monkeypatch.setattr(game, "choice", lambda free_fields: free_fields[0])
    position = choose_ai_move(board, "hard")
    assert position is not None
