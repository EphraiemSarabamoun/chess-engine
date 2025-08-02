import chess
import chess.pgn
import random
import sys

# Simple evaluation function: material balance + basic positional bonuses
def evaluate_board(board):
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -float('inf')  # Black wins
        else:
            return float('inf')   # White wins
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    # Material values
    piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }

    # Positional bonuses (very basic, center control for pawns and knights)
    pawn_table = [
        0,  0,  0,  0,  0,  0,  0,  0,
        5, 10, 10, -20, -20, 10, 10,  5,
        5, -5, -10,  0,  0, -10, -5,  5,
        0,  0,  0, 20, 20,  0,  0,  0,
        5,  5, 10, 25, 25, 10,  5,  5,
        10, 10, 20, 30, 30, 20, 10, 10,
        50, 50, 50, 50, 50, 50, 50, 50,
        0,  0,  0,  0,  0,  0,  0,  0
    ]

    knight_table = [
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20,   0,   5,   5,   0, -20, -40,
        -30,   5,  10,  15,  15,  10,   5, -30,
        -30,   0,  15,  20,  20,  15,   0, -30,
        -30,   5,  15,  20,  20,  15,   5, -30,
        -30,   0,  10,  15,  15,  10,   0, -30,
        -40, -20,   0,   0,   0,   0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50
    ]

    eval = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = piece_values[piece.piece_type]
            if piece.color == chess.BLACK:
                value = -value
            eval += value

            # Add positional bonuses
            if piece.piece_type == chess.PAWN:
                pos_bonus = pawn_table[square if piece.color == chess.WHITE else chess.square_mirror(square)]
                eval += pos_bonus if piece.color == chess.WHITE else -pos_bonus
            elif piece.piece_type == chess.KNIGHT:
                pos_bonus = knight_table[square if piece.color == chess.WHITE else chess.square_mirror(square)]
                eval += pos_bonus if piece.color == chess.WHITE else -pos_bonus

    # Mobility bonus: number of legal moves
    eval += len(list(board.legal_moves)) * 0.1 if board.turn == chess.WHITE else -len(list(board.legal_moves)) * 0.1

    return eval

# Minimax with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Get best move for the AI (assuming AI is black)
def get_best_move(board, depth=3):
    best_move = None
    best_value = float('inf') if board.turn == chess.BLACK else -float('inf')
    alpha = -float('inf')
    beta = float('inf')
    maximizing = board.turn == chess.WHITE

    # Sort moves by simple heuristic (captures first)
    def move_heuristic(move):
        if board.is_capture(move):
            return -1  # Prioritize captures
        return 0

    moves = sorted(board.legal_moves, key=move_heuristic)

    for move in moves:
        board.push(move)
        board_value = minimax(board, depth - 1, alpha, beta, not maximizing)
        board.pop()

        if maximizing:
            if board_value > best_value:
                best_value = board_value
                best_move = move
            alpha = max(alpha, board_value)
        else:
            if board_value < best_value:
                best_value = board_value
                best_move = move
            beta = min(beta, board_value)

        if beta <= alpha:
            break

    return best_move

# Main game loop
def play_chess(ai_color=chess.BLACK, depth=3):
    board = chess.Board()
    print("Welcome to Grok's Chess Engine! You play as White, AI as Black.")
    print("Enter moves in algebraic notation (e.g., e4, Nf3, O-O, exd5, e8=Q). Type 'quit' to exit.")
    print(board)

    while not board.is_game_over():
        if board.turn == chess.WHITE:  # User's turn
            while True:
                user_input = input("Your move: ").strip()
                if user_input.lower() == 'quit':
                    sys.exit(0)
                try:
                    # Parse algebraic notation
                    move = board.parse_san(user_input)
                    if move in board.legal_moves:
                        board.push(move)
                        break
                    else:
                        print("Illegal move. Try again.")
                except ValueError:
                    print("Invalid algebraic notation. Examples: e4, Nf3, O-O, exd5, e8=Q. Try again.")
        else:  # AI's turn
            print("AI thinking...")
            move = get_best_move(board, depth)
            if move:
                # Convert AI's move to algebraic notation for output
                san_move = board.san(move)
                print(f"AI moves: {san_move}")
                board.push(move)
            else:
                print("No move found (this shouldn't happen).")

        print(board)
        print(f"FEN: {board.fen()}")

    print("Game over.")
    print(board.result())

if __name__ == "__main__":
    play_chess(depth=3)