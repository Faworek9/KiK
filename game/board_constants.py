"""Board position constants for tic-tac-toe game logic."""

from typing import Final

# Winning lines (indices 0-8)
WINNING_LINES: Final[tuple[tuple[int, ...], ...]] = (
    (0, 1, 2),  # top row
    (3, 4, 5),  # middle row
    (6, 7, 8),  # bottom row
    (0, 3, 6),  # left column
    (1, 4, 7),  # middle column
    (2, 5, 8),  # right column
    (0, 4, 8),  # diagonal
    (2, 4, 6),  # anti-diagonal
)

# Corner positions
CORNERS: Final[tuple[int, ...]] = (0, 2, 6, 8)

# Edge positions (non-corner, non-center)
EDGES: Final[tuple[int, ...]] = (1, 3, 5, 7)

# Center position
CENTER: Final[int] = 4
