# Chess Engine

This is a simple chess engine that allows you to play against an AI.

## Prerequisites

- Python 3.x
- pipenv

## Installation

1.  **Install Python:** If you don't have Python installed, you can download it from [python.org](https://www.python.org/downloads/).

2.  **Install pipenv:** If you don't have pipenv installed, open your terminal or command prompt and run:

    ```bash
    pip install pipenv
    ```

3.  **Install dependencies:** Navigate to the project directory and run:

    ```bash
    pipenv install
    ```

## How to Play

1.  **Run the script:** Open your terminal or command prompt, navigate to the project directory, and run the following command:

    ```bash
    pipenv run python chess-engine.py
    ```

2.  **Make your move:** You will be playing as White. Enter your moves in standard algebraic notation (e.g., `e4`, `Nf3`, `O-O`, `exd5`, `e8=Q`).

3.  **Quit the game:** To quit the game at any time, simply type `quit` and press Enter.

## How it Works

The AI uses the minimax algorithm with alpha-beta pruning to determine the best move. It evaluates the board based on material balance and basic positional bonuses.