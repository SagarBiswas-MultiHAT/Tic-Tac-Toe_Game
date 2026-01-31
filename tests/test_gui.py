import pytest


tk = pytest.importorskip("tkinter")

from gui import TicTacToeGUI


def test_gui_initialization(monkeypatch):
    root = tk.Tk()
    root.withdraw()
    monkeypatch.setattr(root, "after", lambda _delay, _func=None: None)

    gui = TicTacToeGUI(root)
    assert gui.difficulty_var.get() in {"easy", "mid", "hard"}
    assert gui.total_matches_var.get() >= 1

    root.destroy()


def test_gui_human_win(monkeypatch):
    root = tk.Tk()
    root.withdraw()
    monkeypatch.setattr(root, "after", lambda _delay, _func=None: None)

    gui = TicTacToeGUI(root)
    gui.series_active = True
    gui.match_index = 0
    gui.total_matches = 1
    gui.starter_symbol = "O"
    gui.start_match()
    gui.board[0][0] = "O"
    gui.board[0][1] = "O"
    gui.human_turn = True
    gui.on_cell_click(0, 2)

    assert gui.status_var.get().startswith("You win")

    root.destroy()


def test_gui_computer_win(monkeypatch):
    root = tk.Tk()
    root.withdraw()
    monkeypatch.setattr(root, "after", lambda _delay, _func=None: None)

    gui = TicTacToeGUI(root)
    gui.series_active = True
    gui.match_index = 0
    gui.total_matches = 1
    gui.starter_symbol = "X"
    gui.start_match()

    def fake_choose_ai_move(board, _level):
        board[1][0] = "X"
        board[1][1] = "X"
        board[1][2] = "X"
        return (1, 2)

    monkeypatch.setattr("gui.choose_ai_move", fake_choose_ai_move)

    gui.computer_move()
    assert gui.status_var.get().startswith("Computer wins")

    root.destroy()
