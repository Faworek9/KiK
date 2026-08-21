"""Board representation for tic-tac-toe."""

from typing import Tuple
import config


# Type alias for board state
Board = Tuple[int, ...]


def create_empty_board() -> Board:
    """Create a new empty board."""
    return (config.EMPTY,) * 9


def is_empty(board: Board, position: int) -> bool:
    """Check if a position is empty."""
    return board[position] == config.EMPTY


def make_move(board: Board, position: int, player: int) -> Board:
    """Return a new board with the move made.
    
    Args:
        board: Current board state
        position: Position to place piece (0-8)
        player: PLAYER_X or PLAYER_O
        
    Returns:
        New board with move made
        
    Raises:
        ValueError: If position is invalid or already occupied
    """
    if position < 0 or position > 8:
        raise ValueError(f"Invalid position: {position}")
    if not is_empty(board, position):
        raise ValueError(f"Position {position} is already occupied")
    
    board_list = list(board)
    board_list[position] = player
    return tuple(board_list)


def available_moves(board: Board) -> list[int]:
    """Return list of available move positions."""
    return [i for i in range(9) if is_empty(board, i)]


def is_full(board: Board) -> bool:
    """Check if board is full."""
    return len(available_moves(board)) == 0


def copy_board(board: Board) -> Board:
    """Return a copy of the board (tuples are immutable, but for API consistency)."""
    return board


def to_state_key(board: Board) -> str:
    """Convert board to string key for Q-table storage."""
    return "".join(str(cell) for cell in board)


def from_state_key(key: str) -> Board:
    """Convert string key back to board."""
    return tuple(int(c) for c in key)


def position_to_index(x: int, y: int) -> int:
    """Convert x,y coordinates to board index.
    
    Args:
        x: Column (0-2)
        y: Row (0-2)
        
    Returns:
        Board index (0-8)
    """
    return y * 3 + x


def index_to_position(index: int) -> tuple[int, int]:
    """Convert board index to x,y coordinates.
    
    Args:
        index: Board index (0-8)
        
    Returns:
        Tuple of (x, y) coordinates
    """
    x = index % 3
    y = index // 3
    return (x, y)


def to_display_string(board: Board) -> str:
    """Convert board to human-readable string for display."""
    symbols = {config.EMPTY: ".", config.PLAYER_X: "X", config.PLAYER_O: "O"}
    rows = []
    for y in range(3):
        row = []
        for x in range(3):
            idx = position_to_index(x, y)
            row.append(symbols[board[idx]])
        rows.append(" ".join(row))
    return "\n".join(rows)
