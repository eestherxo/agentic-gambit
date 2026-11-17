import pygame
import chess
from agents.positional_agent import get_positional_move
from agents.material_agent import get_material_move

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

AGENTS = {
    "Positional": get_positional_move,
    "Material": get_material_move,
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


def choose_setup(screen):
    font = pygame.font.SysFont(None, 34)
    buttons = [
        (pygame.Rect(170, 190, 300, 60), "Play Agent 1"), # positional agent 
        (pygame.Rect(170, 280, 300, 60), "Play Agent 2"), # material agent 
        (pygame.Rect(170, 370, 300, 60), "Agent 1 vs Agent 2"),
    ]

    while True:
        screen.fill((235, 235, 225))
        title = font.render("Choose a game mode", True, (30, 30, 30))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 110)))

        for rect, label in buttons:
            pygame.draw.rect(screen, (118, 150, 86), rect, border_radius=8)
            text = font.render(label, True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=rect.center))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for index, (rect, _) in enumerate(buttons):
                    if rect.collidepoint(event.pos):
                        if index == 0:
                            return ("human_vs_agent", get_positional_move, None, None)
                        if index == 1:
                            return ("human_vs_agent", get_material_move, None, None)
                        return (
                            "agent_vs_agent",
                            None,
                            get_positional_move,
                            get_material_move,
                            
                        )

def agent_for_turn(mode, board, human_color, chosen_agent,
                   white_agent, black_agent):
    if mode == "human_vs_agent":
        return chosen_agent if board.turn != human_color else None

    if mode == "agent_vs_agent":
        return white_agent if board.turn == chess.WHITE else black_agent

    return None

def show_game_over(screen, board, pieces):
    outcome = board.outcome(claim_draw=True)

    if outcome is None or outcome.winner is None:
        message = "Draw"
    else:
        winner = "White" if outcome.winner == chess.WHITE else "Black"
        message = f"{winner} Won"

    font = pygame.font.SysFont(None, 48)
    button_font = pygame.font.SysFont(None, 32)
    menu_button = pygame.Rect(170, 365, 300, 60)

    clock = pygame.time.Clock()

    while True:
        # Keep the final board visible behind the dialog.
        draw_board(screen)
        draw_pieces(screen, board, pieces)

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        title = font.render(message, True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 275)))

        pygame.draw.rect(screen, (118, 150, 86), menu_button, border_radius=8)
        label = button_font.render("Restart", True, (255, 255, 255))
        screen.blit(label, label.get_rect(center=menu_button.center))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and menu_button.collidepoint(event.pos)
            ):
                return True

        clock.tick(30)


def play_game(screen, setup, pieces):
    board = chess.Board()
    mode, chosen_agent, white_agent, black_agent = setup
    human_color = chess.WHITE

    clock = pygame.time.Clock()
    ai_delay_ms = 500
    next_ai_move_at = pygame.time.get_ticks() + ai_delay_ms
    selected_sq = None
    possible_moves = []

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and mode == "human_vs_agent"
                and board.turn == human_color
            ):
                target_sq = mouse_to_square(event.pos)
                selected_piece = board.piece_at(target_sq)

                if selected_piece is not None and selected_piece.color == human_color:
                    selected_sq = target_sq

                    possible_moves = [
                        move for move in board.legal_moves
                        if move.from_square == selected_sq
                    ]
                else:
                    selected_moves = [
                        move for move in possible_moves
                        if move.to_square == target_sq
                    ]

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
                        next_ai_move_at = pygame.time.get_ticks() + ai_delay_ms

        agent = agent_for_turn(
            mode, board, human_color, chosen_agent, white_agent, black_agent
        )
        now = pygame.time.get_ticks()

        if (
            agent is not None
            and not board.is_game_over()
            and now >= next_ai_move_at
        ):
            move = agent(board, depth=3)
            if move is not None:
                board.push(move)

            selected_sq = None
            possible_moves = []
            next_ai_move_at = pygame.time.get_ticks() + ai_delay_ms

        # Draw everything.
        draw_board(screen)
        draw_piece_highlight(screen, selected_sq)
        draw_pieces(screen, board, pieces)
        draw_move_dots(screen, possible_moves)

        if board.is_game_over(claim_draw=True):
            return show_game_over(screen, board, pieces)

        pygame.display.flip()
        clock.tick(60)

    return False



def main():

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Agentic Gambit")
    pieces = load_pieces()

    while True:
        setup = choose_setup(screen)
        if setup is None:
            break

        if not play_game(screen, setup, pieces):
            break


if __name__ == "__main__":
    main()
