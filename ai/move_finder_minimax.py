"""Minimax strategic move finder for tic-tac-toe AI with alpha-beta pruning."""

from typing import Optional
import random
import config
from game.board import Board, make_move, available_moves
from game.rules import check_winner
from game.board_constants import WINNING_LINES, CORNERS, EDGES, CENTER


def opponent(player: int) -> int:
    """Get the opponent player.
    
    Args:
        player: PLAYER_X or PLAYER_O
        
    Returns:
        The other player
    """
    return config.PLAYER_O if player == config.PLAYER_X else config.PLAYER_X


def find_winning_move(board: Board, player: int) -> Optional[int]:
    """Find a move that wins immediately.
    
    Args:
        board: Current board state
        player: Player to find winning move for
        
    Returns:
        Position of winning move, or None if no winning move exists
    """
    for move in available_moves(board):
        test_board = make_move(board, move, player)
        if check_winner(test_board) == player:
            return move
    return None


def find_blocking_move(board: Board, player: int) -> Optional[int]:
    """Find a move that blocks opponent's immediate win.
    
    Args:
        board: Current board state
        player: Player to find blocking move for
        
    Returns:
        Position of blocking move, or None if no blocking needed
    """
    opp = opponent(player)
    for move in available_moves(board):
        test_board = make_move(board, move, opp)
        if check_winner(test_board) == opp:
            return move
    return None


def random_move(board: Board) -> int:
    """Choose a random available move.
    
    Args:
        board: Current board state
        
    Returns:
        Random available position
    """
    moves = available_moves(board)
    return random.choice(moves)


def strategic_opening_move(board: Board, player: int) -> int:
    """Choose a strategic opening move.
    
    For first move (y==0): choose from corners or center
    For second move (y==1): take center if available, otherwise corner
    
    Args:
        board: Current board state
        player: Player making the move
        
    Returns:
        Strategic opening position
    """
    moves_count = 9 - len(available_moves(board))
    
    if moves_count == 0:
        # First move: corners or center
        options = list(CORNERS) + [CENTER]
        return random.choice(options)
    elif moves_count == 1:
        # Second move: center if available, otherwise corner
        if board[CENTER] == config.EMPTY:
            return CENTER
        else:
            return random.choice(list(CORNERS))
    else:
        # Not an opening move
        return random_move(board)


def find_forced_sequence(board: Board, player: int, depth: int = 2) -> Optional[int]:
    """Find a move that creates a forced winning sequence.
    
    Simulates: player move -> opponent response -> player move -> check if winning
    This corresponds to atk2x/atk2o (depth=2) and atk22x/atk22o (depth=1)
    
    Args:
        board: Current board state
        player: Player to find sequence for
        depth: 1 for simple sequence (atk22*), 2 for full sequence (atk2*)
        
    Returns:
        First move of the sequence, or None if no sequence found
    """
    opp = opponent(player)
    
    for move1 in available_moves(board):
        board1 = make_move(board, move1, player)
        
        # Check if opponent has immediate win to block
        opp_winning = find_winning_move(board1, opp)
        
        if opp_winning is not None:
            # Opponent can win immediately, try to block
            board2 = make_move(board1, opp_winning, opp)
            
            if depth == 1:
                # atk22* style: after opponent response, check if we can still win
                if find_winning_move(board2, player) is not None:
                    return move1
            else:  # depth == 2
                # atk2* style: after opponent response, try another move
                for move2 in available_moves(board2):
                    board3 = make_move(board2, move2, player)
                    
                    # Check if opponent can win after our second move
                    opp_winning2 = find_winning_move(board3, opp)
                    if opp_winning2 is None:
                        # Opponent can't win immediately, check if we can
                        if find_winning_move(board3, player) is not None:
                            return move1
        else:
            # Opponent has no immediate win
            if depth == 1:
                # atk22* style: if opponent can't win, check if we can
                if find_winning_move(board1, player) is not None:
                    return move1
            else:  # depth == 2
                # atk2* style: try second move
                for move2 in available_moves(board1):
                    board2 = make_move(board1, move2, player)
                    
                    # Check if opponent can win
                    opp_winning2 = find_winning_move(board2, opp)
                    if opp_winning2 is None:
                        if find_winning_move(board2, player) is not None:
                            return move1
    
    return None


def find_defensive_sequence(board: Board, player: int, complex_defense: bool = False) -> Optional[int]:
    """Find a defensive move against opponent's forced sequences.
    
    Corresponds to obr2x/obr2o (simple) and obr22x/obr22o (complex)
    
    Args:
        board: Current board state
        player: Player to find defensive move for
        complex_defense: If True, use more complex defense logic (obr22*)
        
    Returns:
        Defensive move position, or None if no defense needed
    """
    opp = opponent(player)
    
    # Check if opponent has a forced sequence
    opp_sequence = find_forced_sequence(board, opp, depth=1)
    
    if opp_sequence is not None:
        # Opponent has a sequence, block it
        for move in available_moves(board):
            test_board = make_move(board, move, player)
            
            # After our move, check if opponent still has sequence
            if complex_defense:
                # obr22* style: more complex check
                opp_sequence_after = find_forced_sequence(test_board, opp, depth=2)
                opp_winning_after = find_winning_move(test_board, opp)
                
                # Block if opponent can't win or doesn't have sequence
                if opp_winning_after is None and opp_sequence_after is None:
                    return move
            else:
                # obr2* style: simple check
                opp_sequence_after = find_forced_sequence(test_board, opp, depth=1)
                
                if opp_sequence_after is None:
                    return move
    
    return None


class StrategicMoveFinder:
    """Main strategic move finder using perfect-play minimax."""
    
    def __init__(self, player: int):
        """Initialize move finder for a player.
        
        Args:
            player: PLAYER_X or PLAYER_O
        """
        self.player = player

    def _evaluate_terminal(self, board: Board, maximizing_player: int, depth: int) -> Optional[int]:
        """Evaluate terminal board state from maximizing player's perspective."""
        winner = check_winner(board)
        if winner == maximizing_player:
            return 10 - depth
        if winner == opponent(maximizing_player):
            return depth - 10
        if not available_moves(board):
            return 0
        return None

    def _minimax(
        self,
        board: Board,
        current_player: int,
        maximizing_player: int,
        depth: int,
        alpha: int,
        beta: int,
    ) -> int:
        """Return minimax score for a board state."""
        terminal_score = self._evaluate_terminal(board, maximizing_player, depth)
        if terminal_score is not None:
            return terminal_score

        moves = self._ordered_moves(board)

        if current_player == maximizing_player:
            best_score = -100
            for move in moves:
                next_board = make_move(board, move, current_player)
                score = self._minimax(
                    next_board,
                    opponent(current_player),
                    maximizing_player,
                    depth + 1,
                    alpha,
                    beta,
                )
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score

        best_score = 100
        for move in moves:
            next_board = make_move(board, move, current_player)
            score = self._minimax(
                next_board,
                opponent(current_player),
                maximizing_player,
                depth + 1,
                alpha,
                beta,
            )
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score

    def _ordered_moves(self, board: Board) -> list[int]:
        """Order moves to keep decisions deterministic among equally good outcomes."""
        move_priority = [CENTER, *CORNERS, *EDGES]
        moves = available_moves(board)
        return [move for move in move_priority if move in moves]
    
    def choose_move(self, board: Board) -> int:
        """Choose the optimal move using minimax with alpha-beta pruning."""
        moves = self._ordered_moves(board)
        if not moves:
            raise ValueError("No available moves for strategic AI")

        best_move = moves[0]
        best_score = -100

        for move in moves:
            next_board = make_move(board, move, self.player)
            score = self._minimax(
                next_board,
                opponent(self.player),
                self.player,
                depth=1,
                alpha=-100,
                beta=100,
            )

            if score > best_score:
                best_score = score
                best_move = move

        return best_move
