# Contributing

Thanks for your interest in improving Tic‑Tac‑Toe‑Python! Contributions are welcome.

## Quick Start

1. Fork the repo and create a feature branch.
2. Install dev tools:
   ```bash
   python -m pip install -e .[dev]
   ```
3. Run checks:
   ```bash
   ruff check .
   black --check .
   mypy .
   pytest
   ```

## Guidelines

- Keep changes focused and readable.
- Add or update tests when behavior changes.
- Maintain the CLI and GUI user experience.

## Submitting

Open a pull request with a clear description of the changes and why they help.
