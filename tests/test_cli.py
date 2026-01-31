import cli
from game import (
    COMPUTER_SYMBOL,
    PLAYER_SYMBOL,
    apply_move,
    make_list_of_free_fields,
    new_board,
)


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


def test_enter_move_retries_on_occupied_field():
    board = new_board()
    board[0][0] = PLAYER_SYMBOL
    input_fn = _input_sequence(["1", "2"])
    cli.enter_move(board, input_fn)
    assert board[0][1] == PLAYER_SYMBOL


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


def test_display_board_structure():
    board = new_board()
    board[0][0] = PLAYER_SYMBOL
    lines: list[str] = []
    cli.display_board(board, printer=lines.append)
    output = "\n".join(lines)
    assert "+-------+-------+-------+" in lines[0]
    assert PLAYER_SYMBOL in output


def test_prompt_total_matches_requires_positive():
    input_fn = _input_sequence(["foo", "0", "-5", "2"])
    assert cli.prompt_total_matches(input_fn) == 2


def test_print_instructions_outputs_diagram(capsys):
    cli.print_instructions()
    captured = capsys.readouterr()
    assert "Let's start" in captured.out
    assert "+-------+-------+-------+" in captured.out


def test_play_match_computer_win(monkeypatch):
    board = new_board()
    monkeypatch.setattr(cli, "new_board", lambda: board)

    def fake_enter_move(board_arg, _input_fn):
        apply_move(board_arg, (0, 0), PLAYER_SYMBOL)

    monkeypatch.setattr(cli, "enter_move", fake_enter_move)

    def fake_choose_ai_move(board_arg, _level):
        board_arg[1][0] = COMPUTER_SYMBOL
        board_arg[1][1] = COMPUTER_SYMBOL
        board_arg[1][2] = COMPUTER_SYMBOL
        return (1, 2)

    monkeypatch.setattr(cli, "choose_ai_move", fake_choose_ai_move)

    winner = cli.play_match("hard", PLAYER_SYMBOL, lambda _prompt: "1")
    assert winner == COMPUTER_SYMBOL


def test_play_match_draw(monkeypatch):
    board = new_board()
    monkeypatch.setattr(cli, "new_board", lambda: board)

    def fake_enter_move(board_arg, _input_fn):
        apply_move(board_arg, (0, 0), PLAYER_SYMBOL)

    monkeypatch.setattr(cli, "enter_move", fake_enter_move)
    monkeypatch.setattr(cli, "choose_ai_move", lambda *_: None)
    monkeypatch.setattr(cli, "is_draw", lambda _board: True)

    result = cli.play_match("mid", PLAYER_SYMBOL, lambda _prompt: "1")
    assert result is None


def test_play_match_starts_with_computer(monkeypatch):
    board = new_board()
    board[0][1] = PLAYER_SYMBOL
    board[0][2] = PLAYER_SYMBOL
    monkeypatch.setattr(cli, "new_board", lambda: board)
    monkeypatch.setattr(cli, "display_board", lambda *_: None)

    def fake_enter_move(board_arg, _input_fn):
        apply_move(board_arg, (0, 0), PLAYER_SYMBOL)

    def fake_choose_ai_move(board_arg, _level):
        apply_move(board_arg, (1, 0), COMPUTER_SYMBOL)
        return (1, 0)

    monkeypatch.setattr(cli, "enter_move", fake_enter_move)
    monkeypatch.setattr(cli, "choose_ai_move", fake_choose_ai_move)

    winner = cli.play_match("hard", COMPUTER_SYMBOL, lambda _prompt: "1")
    assert winner == PLAYER_SYMBOL


def test_run_game_series_results(monkeypatch, capsys):
    winners = iter([PLAYER_SYMBOL, COMPUTER_SYMBOL, None])

    def fake_play_match(_difficulty, _starter, _input_fn):
        return next(winners)

    monkeypatch.setattr(cli, "play_match", fake_play_match)
    monkeypatch.setattr(cli, "choice", lambda _seq: PLAYER_SYMBOL)

    input_fn = _input_sequence(["mid", "3"])
    cli.run_game(input_fn)

    captured = capsys.readouterr()
    assert "You (O): 1" in captured.out
    assert "Computer (X): 1" in captured.out
    assert "Draws: 1" in captured.out


def test_run_game_series_human_win(monkeypatch, capsys):
    winners = iter([PLAYER_SYMBOL, PLAYER_SYMBOL])

    monkeypatch.setattr(cli, "play_match", lambda *_: next(winners))
    monkeypatch.setattr(cli, "choice", lambda _seq: PLAYER_SYMBOL)
    input_fn = _input_sequence(["mid", "2"])

    cli.run_game(input_fn)
    captured = capsys.readouterr()
    assert "You win the series" in captured.out


def test_run_game_series_computer_win(monkeypatch, capsys):
    winners = iter([COMPUTER_SYMBOL, COMPUTER_SYMBOL])

    monkeypatch.setattr(cli, "play_match", lambda *_: next(winners))
    monkeypatch.setattr(cli, "choice", lambda _seq: COMPUTER_SYMBOL)
    input_fn = _input_sequence(["hard", "2"])

    cli.run_game(input_fn)
    captured = capsys.readouterr()
    assert "Computer wins the series" in captured.out
