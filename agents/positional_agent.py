import chess 
from search import find_best_move, PIECE_VALUES

"""
my positional chess strategy prioritizes the following:
    center control (ability to attack center squares)
    piece activity (mobility and development of pieces)
    pawn structure (pawn positions and how they influence each other)
"""



CENTER_SQUARES = (
    chess.D4,
    chess.E4,
    chess.D5,
    chess.E5,

)

PIECE_ACTIVITY_WEIGHTS = {
    chess.KNIGHT: 1.5,
    chess.BISHOP: 1.5,
    chess.ROOK: 1.0,
    chess.QUEEN: 0.5,
}

MINOR_PIECE_SQAURES = {
    chess.WHITE: {chess.B1, chess.G1, chess.C1, chess.F1},
    chess.BLACK: {chess.B8, chess.G8, chess.C8, chess.F8},
}

DEVELOPMENT_BONUS = 1.0

DOUBLED_PAWN_PENALTY = 0.5
ISOLATED_PAWN_PENALTY = 0.5
PASSED_PAWN_BONUS = 1.5

MATERIAL_WEIGHT = 0.5


def material_score(board, color):
    score = 0
    for piece in board.piece_map().values():
        value = PIECE_VALUES[piece.piece_type]
        score += value if piece.color == color else -value
    return score


def piece_activity(board, colour) -> float:

    mobility_score = 0
    development_score = 0

    for square, piece in board.piece_map().items():
        if piece.color != colour or piece.piece_type not in PIECE_ACTIVITY_WEIGHTS:
            continue

        # Piece Mobility 
        attackable_sqs = sum(
            1
            for target in board.attacks(square) # can sacrifice king safety  
            if board.color_at(target) != colour
        )

        mobility_score += (
            PIECE_ACTIVITY_WEIGHTS[piece.piece_type] * attackable_sqs / 8
        )

        # Minor Piece Development
        if (
            piece.piece_type in (chess.KNIGHT, chess.BISHOP)
            and square not in MINOR_PIECE_SQAURES[colour]
        ):
            development_score += DEVELOPMENT_BONUS

    return mobility_score + development_score


def pawn_structure_score(board, color) -> float:

    pawns = list(board.pieces(chess.PAWN, color))
    enemy_pawns = list(board.pieces(chess.PAWN, not color))

    pawn_score = 0.0

    # Doubled Pawns 
    pawns_per_col = [0] * 8
    for square in pawns:
        pawns_per_col[chess.square_file(square)] += 1

    extra_pawns_per_col = [max(0, count - 1) for count in pawns_per_col]
    pawn_score -= sum(extra_pawns_per_col) * DOUBLED_PAWN_PENALTY

    # Isolated Pawns 
    pawn_cols = {chess.square_file(square) for square in pawns}

    for square in pawns:
        col_index = chess.square_file(square)
        if (col_index - 1 not in pawn_cols) and (col_index + 1 not in pawns):
            pawn_score -= ISOLATED_PAWN_PENALTY

        # Passed Pawns 
        row = chess.square_rank(square)
        is_passed = True 

        for enemy in enemy_pawns:
            enemy_col = chess.square_file(enemy)
            enemy_row = chess.square_rank(enemy)

            if abs(enemy_col - col_index) <= 1:
                if color == chess.WHITE and enemy_row > row:
                    is_passed = False
                    break

                if color == chess.BLACK and enemy_row < row:
                    is_passed = False
                    break

        if is_passed:
            if color == chess.WHITE:
                advance = row - 1
            else:
                advance =  6 - row

            advance = max(0, min(advance, 5))
            pawn_score += PASSED_PAWN_BONUS * advance / 5

    return pawn_score



def evaluate_position(board, player: chess.Color) -> float:

    # CENTER CONTROL 
    white_control = sum(
        board.is_attacked_by(chess.WHITE, square)
        for square in CENTER_SQUARES
    )

    black_control = sum(
        board.is_attacked_by(chess.BLACK, square)
        for square in CENTER_SQUARES
    )

    white_score = white_control - black_control

    # PIECE ACTIVITY 
    white_score += (
        piece_activity(board, chess.WHITE) - piece_activity(board, chess.BLACK)
        )

    # PAWN STRUCTURE 
    white_score += (
    pawn_structure_score(board, chess.WHITE)
    - pawn_structure_score(board, chess.BLACK)
    )

    # MATERIAL BASELINE
    white_score += MATERIAL_WEIGHT * material_score(board, chess.WHITE)

    if player == chess.WHITE:
        return white_score
    return -white_score



def get_positional_move(board, depth = 2):
    return find_best_move(board, depth, evaluate_position)