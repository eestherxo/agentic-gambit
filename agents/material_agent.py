import chess
from search import find_best_move
CENTER_SQUARES = [
    chess.D4, chess.E4,
    chess.D5, chess.E5
]
PIECE_VALUES = {
       chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 0  # King is invaluable, but we can assign it a value of 0 for evaluation purposes
    }
BISHOP_PAIR_BONUS = 50

# Bonus for a passed pawn based on how close it is to promotion.
# Index represents the pawn's rank from its starting side.
PASSED_PAWN_BONUS = {
    3: 40,
    4: 70,
    5: 120,
    6: 200,
    7: 350
}
def evaluate_board(board, player):
    """Evaluates the board and returns a score based on material balance."""
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -100000
        return 100000

    if board.is_game_over():
        return 0
    

    score = 0

    # 1. Material evaluation.
    for piece in board.piece_map().values():
        value = PIECE_VALUES[piece.piece_type]

        if piece.color == chess.WHITE:
            score += value
        else:
            score -= value

    # 2. Bishop pair bonus.
    white_bishops = len(board.pieces(chess.BISHOP, chess.WHITE))
    black_bishops = len(board.pieces(chess.BISHOP, chess.BLACK))

    if white_bishops >= 2:
        score += BISHOP_PAIR_BONUS

    if black_bishops >= 2:
        score -= BISHOP_PAIR_BONUS

    # 3. Passed-pawn bonus.
    for color in [chess.WHITE, chess.BLACK]:

        pawns = board.pieces(chess.PAWN, color)

        for square in pawns:

            if not is_passed_pawn(board, square):
                continue

            rank = chess.square_rank(square)

            # Convert to the pawn's perspective.
            if color == chess.WHITE:
                relative_rank = rank + 1
            else:
                relative_rank = 8 - rank

            bonus = PASSED_PAWN_BONUS.get(relative_rank, 0)

            if color == chess.WHITE:
                score += bonus
            else:
                score -= bonus

    return score if player == chess.WHITE else -score

def is_passed_pawn(board, square):
    piece = board.piece_at(square)

    if piece is None or piece.piece_type != chess.PAWN:
        return False

    color = piece.color
    file = chess.square_file(square)
    rank = chess.square_rank(square)

    # Check the three files in front of the pawn.
    for enemy_square in board.pieces(chess.PAWN, not color):
        enemy_file = chess.square_file(enemy_square)
        enemy_rank = chess.square_rank(enemy_square)

        # Only opposing pawns on the same or adjacent files matter.
        if abs(enemy_file - file) > 1:
            continue

        # White pawns move towards rank 7.
        if color == chess.WHITE and enemy_rank > rank:
            return False

        # Black pawns move towards rank 0.
        if color == chess.BLACK and enemy_rank < rank:
            return False

    return True

def get_material_move(board, depth = 2):
    return find_best_move(board, depth, evaluate_board)