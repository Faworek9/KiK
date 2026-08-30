"""Hybrid strategic move finder combining heuristic priority hierarchy with tactical evaluation."""

from typing import Optional, Tuple
import random
import config
from game.board import Board, make_move, available_moves
from game.rules import check_winner
from game.board_constants import WINNING_LINES, CORNERS, EDGES, CENTER


def opponent(player: int) -> int:
    """Get the opponent player."""
    return config.PLAYER_O if player == config.PLAYER_X else config.PLAYER_X


def count_threats(board: Board, player: int) -> list[int]:
    """Return every empty square that completes a line for a player."""
    threats: list[int] = []
    for line in WINNING_LINES:
        values = [board[pos] for pos in line]
        if values.count(player) == 2 and values.count(config.EMPTY) == 1:
            for pos in line:
                if board[pos] == config.EMPTY and pos not in threats:
                    threats.append(pos)
                    break
    return threats


def find_winning_moves(board: Board, player: int) -> list[int]:
    """Return all immediate winning moves for a player."""
    wins: list[int] = []
    for move in available_moves(board):
        test_board = make_move(board, move, player)
        if check_winner(test_board) == player:
            wins.append(move)
    return wins


def find_winning_move(board: Board, player: int) -> Optional[int]:
    """Find immediate winning move for player.
    
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
    """Find move that blocks opponent's immediate win or multi-threat.
    
    Args:
        board: Current board state
        player: Player to find blocking move for
        
    Returns:
        Position of blocking move, or None if no block needed
    """
    opp = opponent(player)
    opp_winning = find_winning_moves(board, opp)
    if opp_winning:
        return opp_winning[0]

    opp_threats = count_threats(board, opp)
    if not opp_threats:
        return None

    best_move = opp_threats[0]
    best_score = -1
    for move in opp_threats:
        test_board = make_move(board, move, player)
        score = 0
        if find_winning_move(test_board, player) is not None:
            score += 100
        if len(count_threats(test_board, opp)) == 0:
            score += 25
        if move == CENTER:
            score += 5
        elif move in CORNERS:
            score += 3
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


def find_forced_sequence(board: Board, player: int, depth: int = 2) -> Optional[int]:
    """Find a move that creates a forced winning sequence.
    
    Simulates: player move -> opponent response -> player move -> check if winning
    depth=1: simplified sequence (player -> opponent -> player wins)
    depth=2: full sequence (player -> opponent -> player -> opponent -> player wins)
    
    Args:
        board: Current board state
        player: Player to find sequence for
        depth: 1 for simplified, 2 for full sequence
        
    Returns:
        First move of sequence, or None if no sequence found
    """
    opp = opponent(player)
    
    for move1 in available_moves(board):
        board1 = make_move(board, move1, player)
        
        # Check if this move creates a winning opportunity
        winning_lines = 0
        for line in WINNING_LINES:
            values = [board1[pos] for pos in line]
            if values.count(player) == 2 and values.count(config.EMPTY) == 1:
                winning_lines += 1
        
        # If we create multiple winning lines, it's a fork - take it
        if winning_lines >= 2:
            return move1
        
        # Check if opponent has immediate win to block
        opp_winning = find_winning_move(board1, opp)
        
        if opp_winning is not None:
            # Opponent can win immediately, try to block
            board2 = make_move(board1, opp_winning, opp)
            
            if depth == 1:
                # Simplified: after opponent response, check if we can still win
                if find_winning_move(board2, player) is not None:
                    return move1
            else:  # depth == 2
                # Full: try another move after opponent response
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
                # Simplified: if opponent can't win, check if we can
                if find_winning_move(board1, player) is not None:
                    return move1
            else:  # depth == 2
                # Full: try second move
                for move2 in available_moves(board1):
                    board2 = make_move(board1, move2, player)
                    
                    # Check if opponent can win
                    opp_winning2 = find_winning_move(board2, opp)
                    if opp_winning2 is None:
                        if find_winning_move(board2, player) is not None:
                            return move1
    
    return None


def find_defensive_move(board: Board, player: int, complex_defense: bool = False) -> Optional[int]:
    """Find defensive move against opponent's forced sequences.
    
    Args:
        board: Current board state
        player: Player to find defensive move for
        complex_defense: If True, use more complex defense logic
        
    Returns:
        Defensive move position, or None if no defense needed
    """
    opp = opponent(player)

    opp_sequence = find_forced_sequence(board, opp, depth=1 if not complex_defense else 2)
    if opp_sequence is not None:
        for move in available_moves(board):
            test_board = make_move(board, move, player)
            if complex_defense:
                opp_seq_after = find_forced_sequence(test_board, opp, depth=2)
                opp_win_after = find_winning_move(test_board, opp)
                if opp_win_after is None and opp_seq_after is None:
                    return move
            else:
                opp_seq_after = find_forced_sequence(test_board, opp, depth=1)
                if opp_seq_after is None:
                    return move

    opp_threats = count_threats(board, opp)
    if opp_threats:
        for move in available_moves(board):
            test_board = make_move(board, move, player)
            if len(count_threats(test_board, opp)) == 0:
                return move

    return None


def find_fork_prevention(board: Board, player: int) -> Optional[int]:
    """Find move that prevents opponent from creating a fork or simple threats.
    
    A fork is when opponent has two ways to win.
    Also handles simple linear threats that aren't immediate wins.
    
    Args:
        board: Current board state
        player: Player to find fork prevention for
        
    Returns:
        Move that prevents fork or threat, or None if no threat
    """
    opp = opponent(player)
    opp_threats = count_threats(board, opp)

    if len(opp_threats) >= 2:
        return opp_threats[0]

    for opp_move in available_moves(board):
        test_board = make_move(board, opp_move, opp)
        if len(count_threats(test_board, opp)) >= 2:
            for move in available_moves(board):
                if move == opp_move:
                    continue
                block_board = make_move(board, move, player)
                if len(count_threats(block_board, opp)) < 2:
                    return move

    return None


def _tactical_evaluation(board: Board, player: int, current_player: int, depth: int) -> int:
    """Evaluate a board from the tactical perspective of a player.
    
    The legacy heuristic remains in place, but the final move selection now
    does a deeper tactical risk evaluation to avoid fork traps and forced losses.
    """
    winner = check_winner(board)
    if winner == player:
        return 100 - depth
    if winner == opponent(player):
        return depth - 100
    if not available_moves(board):
        return 0

    if depth == 0:
        score = 0
        score += 20 * len(count_threats(board, player))
        score -= 25 * len(count_threats(board, opponent(player)))
        score += 5 * len(find_winning_moves(board, player))
        score -= 10 * len(find_winning_moves(board, opponent(player)))
        if board[CENTER] == player:
            score += 3
        elif board[CENTER] == opponent(player):
            score -= 3
        return score

    best_value = -10**9 if current_player == player else 10**9

    for move in available_moves(board):
        test_board = make_move(board, move, current_player)
        if check_winner(test_board) == current_player:
            value = 100 - depth if current_player == player else depth - 100
        else:
            value = _tactical_evaluation(
                test_board,
                player,
                opponent(current_player),
                depth - 1,
            )

        if current_player == player:
            best_value = max(best_value, value)
        else:
            best_value = min(best_value, value)

    return best_value


def find_tactical_move(board: Board, player: int) -> Optional[int]:
    """Score all legal moves by tactical safety and opportunity."""
    best_move = None
    best_score = -10**9

    for move in available_moves(board):
        test_board = make_move(board, move, player)
        if check_winner(test_board) == player:
            return move

        score = _tactical_evaluation(
            test_board,
            player,
            opponent(player),
            depth=8,
        )

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def find_center_control(board: Board, player: int) -> Optional[int]:
    """Find strategic center control move.
    
    Args:
        board: Current board state
        player: Player to find move for
        
    Returns:
        Center if available, otherwise None
    """
    if board[CENTER] == config.EMPTY:
        return CENTER
    return None


def find_strategic_pattern(board: Board, player: int) -> Optional[int]:
    """Find move based on strategic patterns.
    
    Args:
        board: Current board state
        player: Player to find move for
        
    Returns:
        Strategic pattern move, or None if no pattern applies
    """
    opp = opponent(player)
    moves = available_moves(board)
    
    # Strategic pattern: if we have center and opponent has corner, play opposite corner
    if board[CENTER] == player:
        for i in CORNERS:
            if board[i] == opp:
                opposite = 8 - i
                if opposite in moves:
                    return opposite
    
    # Strategic pattern: if opponent has center, play corner to create diagonal threat
    if board[CENTER] == opp:
        for corner in CORNERS:
            if corner in moves:
                return corner
    
    return None


def find_best_positional_move(board: Board, player: int) -> Optional[int]:
    """Find best move based on positional heuristics.
    
    Args:
        board: Current board state
        player: Player to find move for
        
    Returns:
        Best positional move
    """
    opp = opponent(player)
    moves = available_moves(board)
    
    # Score each move based on positional value
    best_move = None
    best_score = -100
    
    for move in moves:
        score = 0
        
        # Position priority: center > corners > edges
        if move == CENTER:
            score += 5
        elif move in CORNERS:
            score += 3
        else:  # edges
            score += 1
        
        # Check if this move creates a winning opportunity
        test_board = make_move(board, move, player)
        winning_lines = 0
        for line in WINNING_LINES:
            values = [test_board[pos] for pos in line]
            if values.count(player) == 2 and values.count(config.EMPTY) == 1:
                winning_lines += 1
        score += winning_lines * 3  # Increased weight for offensive opportunities
        
        # Check if this move creates a fork (multiple winning lines)
        if winning_lines >= 2:
            score += 20  # Very high priority for forks
        
        # Check if this move blocks opponent
        opp_winning = find_winning_move(board, opp)
        if opp_winning is not None and move == opp_winning:
            score += 10  # High priority to block
        
        # Check if this move prevents opponent from creating winning lines
        test_board_opp = make_move(board, move, player)
        opp_winning_lines = 0
        for line in WINNING_LINES:
            values = [test_board_opp[pos] for pos in line]
            if values.count(opp) == 2 and values.count(config.EMPTY) == 1:
                opp_winning_lines += 1
        score -= opp_winning_lines  # Prefer moves that reduce opponent's opportunities
        
        # Bonus for moves that create potential winning lines
        potential_lines = 0
        for line in WINNING_LINES:
            values = [test_board[pos] for pos in line]
            if values.count(player) == 1 and values.count(config.EMPTY) == 2:
                potential_lines += 1
        score += potential_lines  # Prefer moves that create future opportunities
        
        if score > best_score:
            best_score = score
            best_move = move
    
    return best_move


def find_offensive_fork(board: Board, player: int) -> Optional[int]:
    """Find move that creates an offensive fork (multiple winning threats).
    
    Args:
        board: Current board state
        player: Player to find offensive fork for
        
    Returns:
        Move that creates fork, or None if no fork opportunity
    """
    moves = available_moves(board)
    
    for move in moves:
        test_board = make_move(board, move, player)
        
        # Count how many winning lines this move creates
        winning_lines = 0
        for line in WINNING_LINES:
            values = [test_board[pos] for pos in line]
            if values.count(player) == 2 and values.count(config.EMPTY) == 1:
                winning_lines += 1
        
        # If this creates 2 or more winning lines, it's a fork
        if winning_lines >= 2:
            return move
    
    return None


def strategic_opening_move(board: Board, player: int) -> int:
    """Choose strategic opening move (deterministic).
    
    Args:
        board: Current board state
        player: Player making the move
        
    Returns:
        Strategic opening position
    """
    moves_count = 9 - len(available_moves(board))
    
    if moves_count == 0:
        # First move: always center (optimal)
        return CENTER
    elif moves_count == 1:
        # Second move: center if available, otherwise corner opposite to opponent
        if board[CENTER] == config.EMPTY:
            return CENTER
        else:
            # Find opponent's first move and play opposite corner
            opp = opponent(player)
            for i in range(9):
                if board[i] == opp:
                    if i in CORNERS:
                        # Play opposite corner
                        opposite = 8 - i  # 0->8, 2->6, 6->2, 8->0
                        if board[opposite] == config.EMPTY:
                            return opposite
                    # If opponent played edge, play any corner
                    for corner in CORNERS:
                        if board[corner] == config.EMPTY:
                            return corner
    elif moves_count == 2:
        # Third move: strategic patterns
        opp = opponent(player)

        opp_winning = find_winning_move(board, opp)
        if opp_winning is not None:
            return opp_winning

        opp_threats = count_threats(board, opp)
        if opp_threats:
            return opp_threats[0]

        if board[CENTER] == player:
            for i in CORNERS:
                if board[i] == opp:
                    opposite = 8 - i
                    if board[opposite] == config.EMPTY:
                        return opposite

        if board[CENTER] == opp:
            for corner in CORNERS:
                if board[corner] == config.EMPTY:
                    return corner

    return available_moves(board)[0]


class HybridStrategicMoveFinder:
    """Hybrid strategic move finder combining heuristic priority hierarchy with tactical evaluation."""
    
    def __init__(self, player: int):
        """Initialize move finder for a player.
        
        Args:
            player: PLAYER_X or PLAYER_O
        """
        self.player = player
    
    def choose_move(self, board: Board) -> int:
        """Choose optimal move using heuristic priority hierarchy.
        
        Priority hierarchy:
        1. Immediate win
        2. Block opponent's immediate win
        3. Create simplified winning sequence
        4. Create full winning sequence
        5. Block opponent's simplified sequence
        6. Block opponent's full sequence
        7. Prevent opponent fork
        8. Control center
        9. Random move (fallback)
        
        Args:
            board: Current board state
            
        Returns:
            Chosen move position (0-8)
        """
        moves = available_moves(board)
        if not moves:
            raise ValueError("No available moves")
        
        # Opening moves
        move = strategic_opening_move(board, self.player)
        if len(moves) >= 8:  # First or second move
            return move
        
        # Priority hierarchy
        move = self._find_strategic_move(board)
        if move is not None:
            return move
        
        # Fallback to random move
        return random.choice(moves)
    
    def _find_strategic_move(self, board: Board) -> Optional[int]:
        """Find strategic move using priority hierarchy.
        
        Args:
            board: Current board state
            
        Returns:
            Move position or None
        """
        # Priority 1: Immediate win
        move = find_winning_move(board, self.player)
        if move is not None:
            return move
        
        # Priority 2: Block opponent's immediate win
        move = find_blocking_move(board, self.player)
        if move is not None:
            return move
        
        # Priority 3: One-ply tactical evaluation for forks and hidden threats
        move = find_tactical_move(board, self.player)
        if move is not None:
            return move
        
        # Priority 4: Create offensive fork (elevated - forks are powerful)
        move = find_offensive_fork(board, self.player)
        if move is not None:
            return move
        
        # Priority 5: Control center (elevated - center is crucial)
        move = find_center_control(board, self.player)
        if move is not None:
            return move
        
        # Priority 6: Strategic patterns (center vs corner, etc.)
        move = find_strategic_pattern(board, self.player)
        if move is not None:
            return move
        
        # Priority 6: Create simplified winning sequence
        move = find_forced_sequence(board, self.player, depth=1)
        if move is not None:
            return move
        
        # Priority 7: Create full winning sequence
        move = find_forced_sequence(board, self.player, depth=2)
        if move is not None:
            return move
        
        # Priority 8: Block opponent's simplified sequence
        move = find_defensive_move(board, self.player, complex_defense=False)
        if move is not None:
            return move
        
        # Priority 9: Block opponent's full sequence
        move = find_defensive_move(board, self.player, complex_defense=True)
        if move is not None:
            return move
        
        # Priority 10: Prevent opponent fork
        move = find_fork_prevention(board, self.player)
        if move is not None:
            return move
        
        # Priority 11: Best positional move
        move = find_best_positional_move(board, self.player)
        if move is not None:
            return move
        
        return None
    
