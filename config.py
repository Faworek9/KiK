"""Configuration constants for the tic-tac-toe game."""

from typing import Final
from enum import Enum

# Player constants
EMPTY: Final[int] = 0
PLAYER_X: Final[int] = 1
PLAYER_O: Final[int] = 2


class StrategyType(Enum):
    """Strategy type for AI players."""
    STRATEGIC = "strategic"
    Q_LEARNING = "q_learning"
    RANDOM = "random"


class StrategicAlgorithmType(Enum):
    """Algorithm type for strategic AI."""
    MINIMAX = "minimax"
    HYBRID = "hybrid"
    LEGACY = "legacy"


# Player strategy configuration
# Options: StrategyType.STRATEGIC, StrategyType.Q_LEARNING, StrategyType.RANDOM
PLAYER_X_STRATEGY: Final[StrategyType] = StrategyType.STRATEGIC
PLAYER_O_STRATEGY: Final[StrategyType] = StrategyType.Q_LEARNING

# Strategic algorithm configuration
# Options: StrategicAlgorithmType.MINIMAX, StrategicAlgorithmType.HYBRID, StrategicAlgorithmType.LEGACY
STRATEGIC_ALGORITHM: Final[StrategicAlgorithmType] = StrategicAlgorithmType.LEGACY

# Training parameters
INITIAL_EPSILON: Final[float] = 0.7
EPSILON_DECAY: Final[float] = 0.02
MIN_EPSILON: Final[float] = 0.2
GAMMA_NEGATIVE: Final[float] = 0.5
GAMMA_POSITIVE: Final[float] = 0.8
GAMES_COUNT: Final[int] = 10000
SAVE_INTERVAL: Final[int] = 100

# File paths
Q_TABLE_X_PATH: Final[str] = "q_X.json"
Q_TABLE_O_PATH: Final[str] = "q_O.json"
RESULTS_X_PATH: Final[str] = "wyniki_X.txt"
RESULTS_O_PATH: Final[str] = "wyniki_O.txt"

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
