import chess

MATE_SCORE = 1_000_000

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

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



def chess_minimax(board, depth, utility_function, player,  alpha=float("-inf"), beta=float("inf")):

    if board.is_checkmate():
        return -MATE_SCORE if board.turn == player else MATE_SCORE

    if board.is_game_over(claim_draw=True):
        return 0

    if depth == 0: 
        return utility_function(board, player)

    if board.turn == player:
        max_eval = float("-inf")

        moves = order_moves(board, list(board.legal_moves))
        for move in moves:
            board.push(move)
            eval = chess_minimax(board, depth - 1, utility_function, player, alpha, beta)
            board.pop()

            max_eval = max(max_eval, eval)
            alpha = max(alpha, max_eval)
            if alpha >= beta:
                break

        return max_eval
    
    else:
        min_eval = float("inf")

        moves = order_moves(board, list(board.legal_moves))
        for move in moves:
            board.push(move)
            eval = chess_minimax(board, depth - 1, utility_function, player, alpha, beta)
            board.pop()

            min_eval = min(min_eval, eval)
            beta = min(beta, min_eval)
            if alpha >= beta:
                break

        return min_eval


def find_best_move(board, depth, utility_function):

    player = board.turn 
    best_move = None 
    max_eval = float("-inf")
    alpha = float("-inf")
    beta = float("inf")

    moves = order_moves(board, list(board.legal_moves))
    for move in moves:
        board.push(move)
        eval = chess_minimax(board, depth - 1, utility_function, player, alpha, beta)
        board.pop()

        if eval > max_eval:
            max_eval = eval
            best_move = move

        alpha = max(alpha, max_eval)

    return best_move  

