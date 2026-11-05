import pygame
import chess

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


def main():

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")

    board = chess.Board()
    pieces = load_pieces()

    selected_sq = None
    possible_moves = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                target_sq = mouse_to_square(event.pos)
                if target_sq is None:
                    continue

                selected_piece = board.piece_at(target_sq)

                # select the current players piece and get the possible moves from that piece
                if selected_piece is not None and selected_piece.color == board.turn:
                    selected_sq = target_sq
                    possible_moves = [
                        move
                        for move in board.legal_moves
                        if move.from_square == selected_sq
                    ]
                    print(
                        f"Turn: {"White" if selected_piece.color == True else "Black"}"
                    )
                    print(f"Possible moves: {possible_moves}")
                    continue

                # Move the selected piece to the square selected from possible moves
                # Store as list, pawn promotion results in multiple 'moves'
                selected_moves = [
                    move for move in possible_moves if move.to_square == target_sq
                ]
                print(f"Selected moves: {selected_moves}")

                # Automatic queen promotion, try add options later
                if selected_moves:
                    move = next(
                        (
                            move
                            for move in selected_moves
                            if move.promotion == chess.QUEEN
                        ),
                        selected_moves[0],
                    )
                    board.push(move)
                    selected_sq = None
                    possible_moves = []

        draw_board(screen)
        draw_piece_highlight(screen, selected_sq)
        draw_pieces(screen, board, pieces)
        draw_move_dots(screen, possible_moves)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
