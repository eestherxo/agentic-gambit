import chess

from material_agent import evaluate_board

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0 # King is invaluable, but we can assign it a value of 0 for evaluation purposes
}

def is_game_over(board):
    return board.is_game_over()

def get_legal_moves(board):
    return list(board.legal_moves)

def make_move(board, move):
    new_board = board.copy()
    new_board.push(move)
    return new_board

def chess_minimax(board, depth, alpha=float('-inf'), beta=float('inf')):
    if depth == 0 or is_game_over(board):
        return evaluate_board(board)

    if board.turn == chess.WHITE:
        max_eval = float('-inf')
        for move in order_moves(board, get_legal_moves(board)):
            new_board = make_move(board, move)
            eval = chess_minimax(new_board, depth - 1, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in order_moves(board, get_legal_moves(board)):
            new_board = make_move(board, move)
            eval = chess_minimax(new_board, depth - 1, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(board, depth):

    best_move = None
    if board.turn == chess.WHITE:
        best_eval = float('-inf')

        for move in order_moves(board, get_legal_moves(board)):

            new_board = make_move(board, move)

            evaluation = chess_minimax(new_board, depth - 1, float('-inf'), float('inf'))

            if evaluation > best_eval:
                best_eval = evaluation
                best_move = move
    else:
        best_eval = float('inf')

        for move in order_moves(board, get_legal_moves(board)):

            new_board = make_move(board, move)

            evaluation = chess_minimax(new_board, depth - 1, float('-inf'), float('inf'))

            if evaluation < best_eval:
                best_eval = evaluation
                best_move = move

    return best_move, best_eval


def order_moves(board, moves):

    def move_score(move):
        score = 0

        # Prioritize captures
        if board.is_capture(move):

            victim = board.piece_at(move.to_square)
            attacker = board.piece_at(move.from_square)

            if victim is not None and attacker is not None:
                score += 10 * PIECE_VALUES[victim.piece_type]
                score -= PIECE_VALUES[attacker.piece_type]

        # Prioritize promotions
        if move.promotion:
            score += PIECE_VALUES[move.promotion]

        # Prioritize checks
        board.push(move)
        if board.is_check():
            score += 5
        board.pop()

        return score

    return sorted(moves, key=move_score, reverse=True)


def main():

    board = chess.Board()

    print("Current board:")
    print(board)

    best_move= find_best_move(board, 4)

    print(f"Best move: {best_move}")


if __name__ == "__main__":
    main()
