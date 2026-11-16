
import chess

from agents.positional_agent import (
    evaluate_position,
    get_positional_move,
    material_score,
    pawn_structure_score,
)


def bare_board():
    board = chess.Board(None)
    board.set_piece_at(chess.E1, chess.Piece(chess.KING, chess.WHITE))
    board.set_piece_at(chess.E8, chess.Piece(chess.KING, chess.BLACK))
    return board


def test_starting_position_scores_equally_for_both_perspectives():
    board = chess.Board()

    white_score = evaluate_position(board, chess.WHITE)
    black_score = evaluate_position(board, chess.BLACK)

    assert white_score == -black_score


def test_material_score_counts_white_advantage():
    board = bare_board()
    board.set_piece_at(chess.D4, chess.Piece(chess.QUEEN, chess.WHITE))

    assert material_score(board, chess.WHITE) == 9
    assert material_score(board, chess.BLACK) == -9



def test_advanced_passed_pawn_scores_better():
    board = bare_board()
    board.set_piece_at(chess.A4, chess.Piece(chess.PAWN, chess.WHITE))
    score_earlier = pawn_structure_score(board, chess.WHITE)

    board.remove_piece_at(chess.A4)
    board.set_piece_at(chess.A5, chess.Piece(chess.PAWN, chess.WHITE))
    score_advanced = pawn_structure_score(board, chess.WHITE)

    assert score_advanced > score_earlier


def test_agent_returns_legal_move_without_changing_board():
    board = chess.Board()
    original_position = board.fen()

    move = get_positional_move(board, depth=1)

    assert move in list(board.legal_moves)
    assert board.fen() == original_position