# Agentic Gambit

A mini chess game a using Pygame graphical interface and two Python chess agents:

- Positional agent
- Material agent

The agents use Minimax with Alpha-Beta pruning. The GUI supports human-vs-agent
and agent-vs-agent games.


## Requirements

- python 3.12
- pygame 2.6.1
- chess 1.11.2

Install the dependencies from this directory:

```bash
python -m pip install -r requirements.txt
```

## Run the game

From the project directory:

Windows:

```bash
python chess_visual.py
```

macOS / Linux:

```bash
python3 chess_visual.py
```


## Select Game Mode

When the game opens, select one of the menu buttons:

- **Play Agent 1**: Play as White against the positional agent as Black.
- **Play Agent 2**: Play as White against the material agent as Black.
- **Agent 1 vs Agent 2**: The positional agent plays White against the material agent as Black.


When a game ends, the result popup reports the winner's color or a draw. Choose
**Restart** to return to the game-mode menu, or close the window to exit.




*AI tools were used to assist with debugging and reviewing code.*