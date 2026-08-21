"""Rules and win checking for tic-tac-toe."""

from typing import Optional
import config
from game.board import Board


def check_winner(board: Board) -> Optional[int]:
    """Check if there is a winner.
    
    Args:
        board: Current board state
        
    Returns:
        PLAYER_X if X wins, PLAYER_O if O wins, None if no winner yet
    """
    for line in config.WINNING_LINES:
        values = [board[pos] for pos in line]
        if values[0] != config.EMPTY and values[0] == values[1] == values[2]:
            return values[0]
    return None


def is_game_over(board: Board) -> bool:
    """Check if the game is over (winner or full board).
    
    Args:
        board: Current board state
        
    Returns:
        True if game is over, False otherwise
    """
    if check_winner(board) is not None:
        return True
    
    from game.board import is_full
    return is_full(board)


def get_game_result(board: Board) -> Optional[int]:
    """Get the game result.
    
    Args:
        board: Current board state
        
    Returns:
        PLAYER_X if X wins, PLAYER_O if O wins, 0 if draw, None if game not over
    """
    winner = check_winner(board)
    if winner is not None:
        return winner
    
    from game.board import is_full
    if is_full(board):
        return 0  # Draw
    
    return None  # Game not over
