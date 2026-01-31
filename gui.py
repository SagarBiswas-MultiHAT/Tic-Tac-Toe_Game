from __future__ import annotations

import tkinter as tk
from random import choice
from tkinter import ttk

from game import (
    COMPUTER_SYMBOL,
    PLAYER_SYMBOL,
    choose_ai_move,
    is_draw,
    new_board,
    victory_for,
)


class TicTacToeGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.resizable(False, False)
        self.root.configure(bg="#0f172a")

        self.board = new_board()
        self.human_turn = True
        self.match_index = 0
        self.total_matches = 3
        self.starter_symbol = PLAYER_SYMBOL
        self.human_wins = 0
        self.computer_wins = 0
        self.draws = 0
        self.series_active = False

        self.status_var = tk.StringVar(value="Choose settings and start a series.")
        self.difficulty_var = tk.StringVar(value="mid")
        self.total_matches_var = tk.IntVar(value=3)
        self.score_var = tk.StringVar(value="You 0 • Computer 0 • Draws 0")

        self._style_ui()
        self._build_ui()
        self.start_series()

    def _style_ui(self) -> None:
        style = ttk.Style(self.root)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        style.configure("App.TFrame", background="#0f172a")
        style.configure("Card.TFrame", background="#111827", relief="flat")
        style.configure("Header.TLabel", background="#0f172a", foreground="#f8fafc")
        style.configure(
            "Subtle.TLabel",
            background="#0f172a",
            foreground="#94a3b8",
        )
        style.configure(
            "Status.TLabel",
            background="#111827",
            foreground="#e2e8f0",
            padding=10,
        )
        style.configure(
            "Score.TLabel",
            background="#111827",
            foreground="#cbd5f5",
            padding=8,
        )
        style.configure(
            "Primary.TButton",
            background="#6366f1",
            foreground="white",
            padding=(12, 6),
        )
        style.map(
            "Primary.TButton",
            background=[("active", "#4f46e5")],
        )
        style.configure(
            "Secondary.TButton",
            background="#1f2937",
            foreground="white",
            padding=(10, 6),
        )
        style.map(
            "Secondary.TButton",
            background=[("active", "#334155")],
        )
        style.configure(
            "Cell.TButton",
            background="#1f2937",
            font=("Segoe UI", 18, "bold"),
            padding=(8, 6),
        )
        style.map(
            "Cell.TButton",
            background=[("active", "#334155")],
        )
        style.configure("CellEmpty.TButton", foreground="#f8fafc")
        style.configure("CellO.TButton", foreground="#22c55e")
        style.configure("CellX.TButton", foreground="#f97316")

    def _build_ui(self) -> None:
        header = ttk.Frame(self.root, padding=(20, 18), style="App.TFrame")
        header.pack(fill="x")

        ttk.Label(
            header,
            text="Tic-Tac-Toe",
            font=("Segoe UI", 20, "bold"),
            style="Header.TLabel",
        ).pack(anchor="w")
        ttk.Label(
            header,
            text="You are O. Computer is X. First move alternates each match.",
            style="Subtle.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        content = ttk.Frame(self.root, padding=(20, 10, 20, 20), style="App.TFrame")
        content.pack(fill="both", expand=True)

        left_card = ttk.Frame(content, padding=16, style="Card.TFrame")
        left_card.grid(row=0, column=0, sticky="n", padx=(0, 16))

        ttk.Label(left_card, text="Series Settings", font=("Segoe UI", 12, "bold"), style="Status.TLabel").pack(
            fill="x", pady=(0, 12)
        )

        ttk.Label(left_card, text="AI Level", style="Status.TLabel").pack(anchor="w")
        ttk.OptionMenu(left_card, self.difficulty_var, "mid", "easy", "mid", "hard").pack(
            fill="x", pady=(6, 12)
        )

        ttk.Label(left_card, text="Matches", style="Status.TLabel").pack(anchor="w")
        ttk.Spinbox(left_card, from_=1, to=25, textvariable=self.total_matches_var, width=6).pack(
            anchor="w", pady=(6, 12)
        )

        ttk.Button(left_card, text="Start Series", command=self.start_series, style="Primary.TButton").pack(
            fill="x", pady=(4, 8)
        )
        self.next_match_button = ttk.Button(
            left_card, text="Next Match", command=self.start_match, state="disabled", style="Secondary.TButton"
        )
        self.next_match_button.pack(fill="x")

        self.score_label = ttk.Label(
            left_card, textvariable=self.score_var, style="Score.TLabel", anchor="center"
        )
        self.score_label.pack(fill="x", pady=(16, 0))

        center_card = ttk.Frame(content, padding=20, style="Card.TFrame")
        center_card.grid(row=0, column=1, sticky="n")

        self.status_label = ttk.Label(
            center_card, textvariable=self.status_var, style="Status.TLabel", anchor="center"
        )
        self.status_label.pack(fill="x", pady=(0, 12))

        board_frame = ttk.Frame(center_card, padding=8, style="Card.TFrame")
        board_frame.pack()

        self.buttons: list[list[ttk.Button]] = []
        for row in range(3):
            button_row: list[ttk.Button] = []
            for col in range(3):
                button = ttk.Button(
                    board_frame,
                    text=" ",
                    width=7,
                    style="Cell.TButton",
                    command=lambda r=row, c=col: self.on_cell_click(r, c),
                )
                button.grid(row=row, column=col, padx=8, pady=8, ipadx=10, ipady=10)
                button_row.append(button)
            self.buttons.append(button_row)

        content.columnconfigure(1, weight=1)

    def start_series(self) -> None:
        self.total_matches = max(1, int(self.total_matches_var.get()))
        self.match_index = 0
        self.human_wins = 0
        self.computer_wins = 0
        self.draws = 0
        self.series_active = True
        self.starter_symbol = choice([PLAYER_SYMBOL, COMPUTER_SYMBOL])
        self._update_scoreboard()
        self.start_match()

    def start_match(self) -> None:
        if not self.series_active:
            return

        if self.match_index >= self.total_matches:
            self._finalize_series()
            return

        self.match_index += 1
        self.board = new_board()
        self.human_turn = self.starter_symbol == PLAYER_SYMBOL
        self._render_board()
        self._disable_board(False)
        self.next_match_button.config(state="disabled")

        starter_text = "You" if self.human_turn else "Computer"
        self.status_var.set(
            f"Match {self.match_index}/{self.total_matches} — {starter_text} starts."
        )

        if not self.human_turn:
            self._disable_board(True)
            self.root.after(200, self.computer_move)

    def _render_board(self) -> None:
        for row in range(3):
            for col in range(3):
                symbol = self.board[row][col]
                button = self.buttons[row][col]
                button.config(text=symbol)
                if symbol == PLAYER_SYMBOL:
                    button.config(style="CellO.TButton")
                elif symbol == COMPUTER_SYMBOL:
                    button.config(style="CellX.TButton")
                else:
                    button.config(style="CellEmpty.TButton")

    def _disable_board(self, disabled: bool) -> None:
        state = "disabled" if disabled else "normal"
        for row in self.buttons:
            for button in row:
                button.config(state=state)

    def on_cell_click(self, row: int, col: int) -> None:
        if not self.human_turn or self.board[row][col] != " ":
            return

        self.board[row][col] = PLAYER_SYMBOL
        self._render_board()

        if victory_for(self.board, PLAYER_SYMBOL):
            self._finish_match(winner=PLAYER_SYMBOL)
            return

        if is_draw(self.board):
            self._finish_match(winner=None)
            return

        self.human_turn = False
        self.status_var.set("Computer is thinking...")
        self._disable_board(True)
        self.root.after(200, self.computer_move)

    def computer_move(self) -> None:
        if victory_for(self.board, PLAYER_SYMBOL) or is_draw(self.board):
            return

        level = self.difficulty_var.get()
        choose_ai_move(self.board, level)
        self._render_board()

        if victory_for(self.board, COMPUTER_SYMBOL):
            self._finish_match(winner=COMPUTER_SYMBOL)
            return

        if is_draw(self.board):
            self._finish_match(winner=None)
            return

        self.human_turn = True
        self.status_var.set("Your turn.")
        self._disable_board(False)

    def _finish_match(self, winner: str | None) -> None:
        if winner == PLAYER_SYMBOL:
            self.human_wins += 1
            self.status_var.set("You win this match! 🎉")
        elif winner == COMPUTER_SYMBOL:
            self.computer_wins += 1
            self.status_var.set("Computer wins this match.")
        else:
            self.draws += 1
            self.status_var.set("This match is a draw.")

        self._update_scoreboard()
        self._disable_board(True)

        if self.match_index >= self.total_matches:
            self._finalize_series()
            return

        self.next_match_button.config(state="normal")
        self.starter_symbol = (
            PLAYER_SYMBOL if self.starter_symbol == COMPUTER_SYMBOL else COMPUTER_SYMBOL
        )

    def _finalize_series(self) -> None:
        self.series_active = False
        if self.human_wins > self.computer_wins:
            result = "You win the series!"
        elif self.computer_wins > self.human_wins:
            result = "Computer wins the series."
        else:
            result = "The series ends in a draw."
        self.status_var.set(result)
        self.next_match_button.config(state="disabled")

    def _update_scoreboard(self) -> None:
        self.score_var.set(
            f"You {self.human_wins} • Computer {self.computer_wins} • Draws {self.draws}"
        )


def main() -> None:
    root = tk.Tk()
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")
    TicTacToeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
