import pygame
import chess
from search import find_best_move
WIDTH = 640
HEIGHT = 640
DIMENSIONS = 8
SQ_SIZE = HEIGHT // DIMENSIONS

# board colors
LIGHT = "#eeeed2"
DARK = "#769656"


piece_names = {
    "K": "wK",
    "Q": "wQ",
    "R": "wR",
    "B": "wB",
    "N": "wN",
    "P": "wP",
    "k": "bK",
    "q": "bQ",
    "r": "bR",
    "b": "bB",
    "n": "bN",
    "p": "bP",
}


def load_pieces():

    pieces = {}

    for symbol, filename in piece_names.items():

        image = pygame.image.load(f"pieces/{filename}.png").convert_alpha()
        pieces[symbol] = pygame.transform.smoothscale(image, (SQ_SIZE, SQ_SIZE))

    return pieces


def draw_board(screen):

    for row in range(8):
        for col in range(8):
            color = LIGHT if (row + col) % 2 == 0 else DARK

            pygame.draw.rect(
                screen, color, (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            )


def draw_pieces(screen, board, pieces):

    for row in range(8):
        for col in range(8):
            square = chess.square(col, 7 - row)
            piece = board.piece_at(square)

            if piece is not None:
                symbol = piece.symbol()

                # display image onto the window at specified location
                screen.blit(pieces[symbol], (col * SQ_SIZE, row * SQ_SIZE))


def mouse_to_square(position):
    """Translates the position of a mouse click into a square"""

    x, y = position

    sq_col = x // SQ_SIZE
    game_row = y // SQ_SIZE
    sq_row = 7 - game_row

    square = chess.square(sq_col, sq_row)
    return square


def draw_piece_highlight(screen, selected_sq):
    if selected_sq is None:
        return

    col = chess.square_file(selected_sq)
    row = 7 - chess.square_rank(selected_sq)
    rect = pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)

    overlay = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
    overlay.fill((255, 220, 0, 90))
    screen.blit(overlay, rect)


def draw_move_dots(screen, possible_moves):

    destinations = {move.to_square for move in possible_moves}

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    for square in destinations:
        col = chess.square_file(square)
        row = 7 - chess.square_rank(square)
        center = (col * SQ_SIZE + SQ_SIZE // 2, row * SQ_SIZE + SQ_SIZE // 2)

        pygame.draw.circle(overlay, (30, 30, 30, 110), center, SQ_SIZE // 8)

    screen.blit(overlay, (0, 0))

AI_COLOR = chess.BLACK
SEARCH_DEPTH = 3


def make_ai_move(board):
    if board.is_game_over():
        return

    best_move, evaluation = find_best_move(board, SEARCH_DEPTH)

    if best_move is not None:
        board.push(best_move)

        print(f"AI played: {best_move}")
        print(f"Evaluation: {evaluation}")

def draw_status(screen, board, font):

    if board.is_checkmate():
        winner = "White" if board.turn == chess.BLACK else "Black"
        message = f"Checkmate! {winner} wins"

    elif board.is_game_over():
        message = f"Game over: {board.result()}"

    elif board.is_check():
        message = f"{'White' if board.turn else 'Black'} is in check"

    else:
        message = f"{'White' if board.turn else 'Black'} to move"

    text = font.render(message, True, (255, 255, 255))

    screen.blit(text, (10, 10))


def main():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess - Material Agent")

    board = chess.Board()
    pieces = load_pieces()

    font = pygame.font.SysFont("Arial", 22, bold=True)

    selected_sq = None
    possible_moves = []

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                # Only allow human moves when it is White's turn.
                if board.turn == AI_COLOR:
                    continue

                if board.is_game_over():
                    continue

                target_sq = mouse_to_square(event.pos)

                if target_sq is None:
                    continue

                selected_piece = board.piece_at(target_sq)

                # Select a White piece.
                if (
                    selected_piece is not None
                    and selected_piece.color == chess.WHITE
                ):

                    selected_sq = target_sq

                    possible_moves = [
                        move
                        for move in board.legal_moves
                        if move.from_square == selected_sq
                    ]

                    print("Possible moves:", possible_moves)

                    continue

                # Find moves to the selected destination.
                selected_moves = [
                    move
                    for move in possible_moves
                    if move.to_square == target_sq
                ]

                if selected_moves:

                    # Automatically promote to a queen for now.
                    move = next(
                        (
                            move
                            for move in selected_moves
                            if move.promotion == chess.QUEEN
                        ),
                        selected_moves[0]
                    )

                    # Apply the human move.
                    board.push(move)

                    selected_sq = None
                    possible_moves = []

                    print("Human played:", move)

                    # Let the AI respond.
                    if not board.is_game_over():
                        make_ai_move(board)

                else:
                    # Clear selection if the destination is invalid.
                    selected_sq = None
                    possible_moves = []

        # Draw everything.
        draw_board(screen)
        draw_piece_highlight(screen, selected_sq)
        draw_pieces(screen, board, pieces)
        draw_move_dots(screen, possible_moves)
        draw_status(screen, board, font)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
