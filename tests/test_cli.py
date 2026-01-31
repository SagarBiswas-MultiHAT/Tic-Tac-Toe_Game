import cli
from game import COMPUTER_SYMBOL, PLAYER_SYMBOL, make_list_of_free_fields, new_board


def _input_sequence(values):
    iterator = iter(values)
    return lambda _prompt="": next(iterator)


def test_prompt_move_accepts_valid_number():
    input_fn = _input_sequence(["a", "10", "5"])
    assert cli.prompt_move(input_fn) == 5


def test_prompt_difficulty_accepts_valid_choice():
    input_fn = _input_sequence(["foo", "Hard"])
    assert cli.prompt_difficulty(input_fn) == "hard"


def test_enter_move_places_symbol():
    board = new_board()
    input_fn = _input_sequence(["1"])
    cli.enter_move(board, input_fn)
    assert board[0][0] == PLAYER_SYMBOL


def test_run_game_human_win(monkeypatch):
    def fake_choose_ai_move(board, _level):
        if board[1][1] == " ":
            board[1][1] = COMPUTER_SYMBOL
            return (1, 1)
        free = make_list_of_free_fields(board)
        row, col = free[0]
        board[row][col] = COMPUTER_SYMBOL
        return (row, col)

    def fake_victory_for(board, symbol):
        return symbol == PLAYER_SYMBOL and board[0][0] == PLAYER_SYMBOL

    monkeypatch.setattr(cli, "choose_ai_move", fake_choose_ai_move)
    monkeypatch.setattr(cli, "victory_for", fake_victory_for)
    monkeypatch.setattr(cli, "choice", lambda _seq: PLAYER_SYMBOL)

    input_fn = _input_sequence(["easy", "1", "1"])
    cli.run_game(input_fn)
