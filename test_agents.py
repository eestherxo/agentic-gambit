
import chess
import pytest

from material_agent import evaluate_board, is_passed_pawn


def empty_board():
    """Create a board containing only the two kings."""
    board = chess.Board(None)

    board.set_piece_at(
        chess.E1, chess.Piece(chess.KING, chess.WHITE)
    )
    board.set_piece_at(
        chess.E8, chess.Piece(chess.KING, chess.BLACK)
    )

    return board


def test_starting_position():
    board = chess.Board()
    assert evaluate_board(board) == 0


def test_extra_white_pawn():
    board = empty_board()
    board.set_piece_at(
        chess.E2, chess.Piece(chess.PAWN, chess.WHITE)
    )

    assert evaluate_board(board) == 100


def test_extra_black_pawn():
    board = empty_board()
    board.set_piece_at(
        chess.E7, chess.Piece(chess.PAWN, chess.BLACK)
    )

    assert evaluate_board(board) == -100


def test_bishop_pair_bonus():
    board = empty_board()

    board.set_piece_at(
        chess.C1, chess.Piece(chess.BISHOP, chess.WHITE)
    )
    board.set_piece_at(
        chess.F1, chess.Piece(chess.BISHOP, chess.WHITE)
    )

    # 2 bishops = 660, bishop pair bonus = 50
    assert evaluate_board(board) == 710


def test_passed_pawn_bonus():
    board = empty_board()

    board.set_piece_at(
        chess.E7, chess.Piece(chess.PAWN, chess.WHITE)
    )

    # Pawn = 100, seventh-rank bonus = 350
    assert evaluate_board(board) == 450


def test_black_passed_pawn_bonus():
    board = empty_board()

    board.set_piece_at(
        chess.E2, chess.Piece(chess.PAWN, chess.BLACK)
    )

    # Pawn = -100, seventh-rank bonus = -350
    assert evaluate_board(board) == -450


def test_pawn_is_not_passed():
    board = empty_board()

    board.set_piece_at(
        chess.E5, chess.Piece(chess.PAWN, chess.WHITE)
    )
    board.set_piece_at(
        chess.D6, chess.Piece(chess.PAWN, chess.BLACK)
    )

    assert not is_passed_pawn(board, chess.E5)


def test_passed_pawn():
    board = empty_board()

    board.set_piece_at(
        chess.E5, chess.Piece(chess.PAWN, chess.WHITE)
    )

    assert is_passed_pawn(board, chess.E5)
