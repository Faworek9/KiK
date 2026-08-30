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

