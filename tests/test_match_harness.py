import chess

from agents.material_agent import get_material_move
from agents.positional_agent import get_positional_move


GAME_COUNT = 6
SEARCH_DEPTH = 2
TOTAL_MOVE_LIMIT = 300


def play_game(player) -> tuple[str, str]:
    board = chess.Board()
    opponent = not player
    agents = {
        player: ("Positional", get_positional_move),
        opponent: ("Material", get_material_move),
    }

    while not board.is_game_over(claim_draw=True) and board.ply() < TOTAL_MOVE_LIMIT:
        agent_name, choose_move = agents[board.turn]
        move = choose_move(board, depth=SEARCH_DEPTH)

        if move is None or move not in board.legal_moves:
            raise RuntimeError(
                f"{agent_name} returned an invalid move in position {board.fen()}"
            )

        board.push(move)

    if board.ply() >= TOTAL_MOVE_LIMIT and not board.is_game_over(claim_draw=True):
        return "Draw", "Ply limit reached"

    outcome = board.outcome(claim_draw=True)
    if outcome is None or outcome.winner is None:
        return "Draw", board.result(claim_draw=True)

    winner_name = agents[outcome.winner][0]
    return winner_name, board.result(claim_draw=True)


def test_run_match(game_count: int = GAME_COUNT) -> None:
    if game_count < 1:
        raise ValueError("Game count must be at least 1")

    wins = {"Positional": 0, "Material": 0, "Draw": 0}

    for game_number in range(game_count):
        player_color = chess.WHITE if game_number % 2 == 0 else chess.BLACK
        player_color_name = (
            "White" if player_color == chess.WHITE else "Black"
        )
        opponent_color_name = "Black" if player_color_name == "White" else "White"

        winner, result = play_game(player_color)
        wins[winner] += 1
        print(
            f"\n***********************************\n"
            f"Game {game_number + 1}: {result}\n"
            f"Positional played {player_color_name}\n"
            f"Material played {opponent_color_name}\n"
            f"winner: {winner}\n"
            f"***********************************"
        )

    print("\nMatch totals:")
    for agent_name, wins_count in wins.items():
        print(f"{agent_name}: {wins_count}")


