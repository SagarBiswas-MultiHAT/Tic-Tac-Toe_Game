# Tic-Tac-Toe-Python

Welcome to **Tic-Tac-Toe-Python**, a clean and beginner-friendly command‑line Tic‑Tac‑Toe game written in Python. You play as `O`, the computer plays as `X`, and you can choose how smart the computer should be (easy, mid, or hard).

---

## Features

- **Interactive Gameplay**: Enter your moves via a user-friendly console interface.
- **Three AI Levels**: Easy (random), Mid (win/block), Hard (optimal play).
- **Visually Clear Board**: The board is displayed with a neat and readable design.
- **Error Handling**: Invalid or duplicate moves are handled gracefully.

---

## What’s Included

- **Human vs AI** gameplay in the terminal
- **Difficulty selection** at game start
- **Readable board rendering** with numbered positions
- **Modular code** split into game logic and CLI handling

---

## How to Play

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/Tic-Tac-Toe-Python.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Tic-Tac-Toe-Python
   ```
3. Run the game:
   ```bash
   python "tic-tac-toe v1.1.py"
   ```
4. Choose AI difficulty when prompted: `easy`, `mid`, or `hard`.
5. The computer makes the first move. On harder levels it will not always start in the center.
6. Pick your move by entering a number (1‑9) corresponding to the board position:

   ```
   +-------+-------+-------+
   |   1   |   2   |   3   |
   +-------+-------+-------+
   |   4   |   5   |   6   |
   +-------+-------+-------+
   |   7   |   8   |   9   |
   +-------+-------+-------+
   ```

---

## Rules

- Players take turns placing their symbols (`O` for you, `X` for the computer) on the board.
- The first player to align three of their symbols horizontally, vertically, or diagonally wins.
- If all spaces are filled without a winner, the game ends in a draw.

---

## Difficulty Levels

- **Easy**: Random legal moves. Great for first‑time players.
- **Mid**: Tries to win in one move or block you from winning; otherwise random.
- **Hard**: Uses optimal play (minimax). It won’t make mistakes.

---

## Example Gameplay

Here's an example of the board during gameplay:

```
+-------+-------+-------+
|   X   |       |       |
+-------+-------+-------+
|       |   O   |       |
+-------+-------+-------+
|       |       |       |
+-------+-------+-------+
```

---

## Project Structure

```
tic-tac-toe v1.1.py  # Entry point
cli.py               # Console UI and game loop
game.py              # Core game logic + AI
tests/               # Automated tests
```

---

## Learning Opportunity

This project is perfect for beginners who want to:

- Understand Python basics.
- Learn game development logic.
- Work with functions, lists, and loops.

---

## Development & Testing

- Run tests:
  ```bash
  python -m pytest
  ```

---

## Troubleshooting

- **Game doesn’t start**: Make sure you’re running the exact file name with quotes:
  ```bash
  python "tic-tac-toe v1.1.py"
  ```
- **Module not found**: Ensure you run the command from the project root.

---

## Contributions

Contributions are welcome! If you'd like to improve the AI, enhance the interface, or add new features, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

---

Enjoy the game, and may the best player win! 🎉
