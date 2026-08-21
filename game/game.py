"""Game engine for tic-tac-toe."""

from typing import Optional, Callable
from dataclasses import dataclass, field
import config
from game.board import Board, create_empty_board, make_move, available_moves, to_state_key
from game.rules import check_winner, is_game_over, get_game_result


@dataclass
class GameHistory:
    """History of moves in a game."""
    moves: list[int] = field(default_factory=list)  # Move positions
    states: list[str] = field(default_factory=list)  # Board states before each move


@dataclass
class GameResult:
    """Result of a game."""
    winner: Optional[int] = None  # PLAYER_X, PLAYER_O, or None (draw)
    is_draw: bool = False
    is_finished: bool = False


class Game:
    """Game engine for a single tic-tac-toe game."""
    
    def __init__(self, player_x: Callable[[Board], int], player_o: Callable[[Board], int]):
        """Initialize a new game.
        
        Args:
            player_x: Function that takes board and returns move for X
            player_o: Function that takes board and returns move for O
        """
        self.player_x = player_x
        self.player_o = player_o
        self.board: Board = create_empty_board()
        self.current_player = config.PLAYER_X
        self.history = GameHistory()
        self.result = GameResult()
        self.move_count = 0
    
    def reset(self):
        """Reset the game to initial state."""
        self.board = create_empty_board()
        self.current_player = config.PLAYER_X
        self.history = GameHistory()
        self.result = GameResult()
        self.move_count = 0
    
    def play_move(self, move: int) -> bool:
        """Play a move for the current player.
        
        Args:
            move: Position to play (0-8)
            
        Returns:
            True if move was successful, False otherwise
        """
        if self.result.is_finished:
            return False
        
        if move not in available_moves(self.board):
            return False
        
        # Record state before move
        state_key = to_state_key(self.board)
        self.history.states.append(state_key)
        self.history.moves.append(move)
        
        # Make the move
        self.board = make_move(self.board, move, self.current_player)
        self.move_count += 1
        
        # Check for winner
        winner = check_winner(self.board)
        if winner is not None:
            self.result.winner = winner
            self.result.is_finished = True
            return True
        
        # Check for draw
        if is_game_over(self.board):
            self.result.is_draw = True
            self.result.is_finished = True
            return True
        
        # Switch player
        self.current_player = config.PLAYER_O if self.current_player == config.PLAYER_X else config.PLAYER_X
        return True
    
    def play(self) -> GameResult:
        """Play a complete game with both players.
        
        Returns:
            Game result
        """
        self.reset()
        
        while not self.result.is_finished:
            if self.current_player == config.PLAYER_X:
                move = self.player_x(self.board)
            else:
                move = self.player_o(self.board)
            
            if not self.play_move(move):
                # Invalid move, game ends
                self.result.is_finished = True
                break
        
        return self.result
    
    def get_board(self) -> Board:
        """Get current board state."""
        return self.board
    
    def get_current_player(self) -> int:
        """Get current player."""
        return self.current_player
    
    def is_finished(self) -> bool:
        """Check if game is finished."""
        return self.result.is_finished
    
    def get_history(self) -> GameHistory:
        """Get game history."""
        return self.history
    
    def get_move_count(self) -> int:
        """Get number of moves played."""
        return self.move_count
