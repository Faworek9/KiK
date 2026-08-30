"""Heuristic strategic move finder without minimax search."""

from typing import Optional
import random

import config
from game.board import Board, available_moves, make_move
from game.rules import check_winner
from game.board_constants import WINNING_LINES, CORNERS, EDGES, CENTER


def opponent(player: int) -> int:
    """Return the opposing player."""
    return config.PLAYER_O if player == config.PLAYER_X else config.PLAYER_X


def _position_score(move: int) -> int:
    """Return a simple positional priority for deterministic tie-breaking."""
    if move == CENTER:
        return 3
    if move in CORNERS:
        return 2
    return 1


def _is_corner(move: int) -> bool:
    """Check whether a move is a corner square."""
    return move in CORNERS


def _is_side(move: int) -> bool:
    """Check whether a move is a side square."""
    return move in EDGES


def _opposite_corner(move: int) -> Optional[int]:
    """Return the opposite corner for a corner square."""
    if move == 0:
        return 8
    if move == 2:
        return 6
    if move == 6:
        return 2
    if move == 8:
        return 0
    return None


def _has_opposite_corners(board: Board, player: int) -> bool:
    """Check whether a player occupies any opposite corner pair."""
    return (
        board[0] == player and board[8] == player
    ) or (
        board[2] == player and board[6] == player
    )


def find_opening_move(board: Board, player: int) -> Optional[int]:
    """Choose the opening move: first move is a random center or corner."""
    moves_played = 9 - len(available_moves(board))

    if moves_played == 0:
        return random.choice([CENTER, *CORNERS])

    if moves_played == 1:
        if board[CENTER] == config.EMPTY:
            return CENTER
        for corner in CORNERS:
            if board[corner] == config.EMPTY:
                return corner

    return None


def _winning_moves(board: Board, player: int) -> list[int]:
    """Return all immediate winning moves for a player."""
    moves: list[int] = []
    for move in available_moves(board):
        if check_winner(make_move(board, move, player)) == player:
            moves.append(move)
    return moves


def _fork_moves(board: Board, player: int) -> list[int]:
    """Return moves that create two or more immediate winning replies."""
    moves: list[int] = []
    for move in available_moves(board):
        after = make_move(board, move, player)
        if len(_winning_moves(after, player)) >= 2:
            moves.append(move)
    return moves


def _line_balance(board: Board, player: int) -> int:
    """Score open lines from the point of view of one player."""
    opp = opponent(player)
    score = 0

    for line in WINNING_LINES:
        values = [board[pos] for pos in line]
        our_count = values.count(player)
        opp_count = values.count(opp)
        empty_count = values.count(config.EMPTY)

        if our_count > 0 and opp_count > 0:
            continue

        if opp_count == 0:
            if our_count == 2 and empty_count == 1:
                score += 100
            elif our_count == 1 and empty_count == 2:
                score += 12
            elif our_count == 0 and empty_count == 3:
                score += 1
        elif our_count == 0:
            if opp_count == 2 and empty_count == 1:
                score -= 100
            elif opp_count == 1 and empty_count == 2:
                score -= 12
            elif opp_count == 0 and empty_count == 3:
                score -= 1

    return score


def find_winning_move(board: Board, player: int) -> Optional[int]:
    """Find a move that wins immediately."""
    best_move: Optional[int] = None
    best_score = (-1, -1)

    for move in _winning_moves(board, player):
        score = (_position_score(move), -move)
        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def find_blocking_move(board: Board, player: int) -> Optional[int]:
    """Find the best move that reduces the opponent's immediate wins."""
    opp = opponent(player)
    opp_wins_before = _winning_moves(board, opp)
    if not opp_wins_before:
        return None

    best_move: Optional[int] = None
    best_score = (-10**9, -10**9, -10**9, -10**9, -10**9, -10**9, -10**9)

    for move in available_moves(board):
        after = make_move(board, move, player)
        opp_wins_after = len(_winning_moves(after, opp))
        opp_forks_after = len(_fork_moves(after, opp))
        our_wins_after = len(_winning_moves(after, player))
        score = (
            1 if opp_wins_after == 0 else 0,
            len(opp_wins_before) - opp_wins_after,
            -opp_wins_after,
            1 if opp_forks_after == 0 else 0,
            -opp_forks_after,
            our_wins_after,
            1 if _is_side(move) else 0,
            _position_score(move),
        )
        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def find_fork_move(board: Board, player: int) -> Optional[int]:
    """Find a move that creates a fork."""
    best_move: Optional[int] = None
    best_score = (-1, -1, -1, -1)

    for move in _fork_moves(board, player):
        after = make_move(board, move, player)
        score = (
            len(_winning_moves(after, player)),
            _line_balance(after, player),
            -len(_winning_moves(after, opponent(player))),
            _position_score(move),
        )
        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def find_fork_block_move(board: Board, player: int) -> Optional[int]:
    """Find a move that reduces the opponent's fork opportunities."""
    opp = opponent(player)
    opp_forks_before = _fork_moves(board, opp)
    if not opp_forks_before:
        return None

    best_move: Optional[int] = None
    best_score = (-10**9, -10**9, -10**9, -10**9, -10**9, -10**9, -10**9)

    for move in available_moves(board):
        after = make_move(board, move, player)
        opp_wins_after = len(_winning_moves(after, opp))
        opp_forks_after = len(_fork_moves(after, opp))
        our_wins_after = len(_winning_moves(after, player))
        score = (
            1 if opp_wins_after == 0 else 0,
            1 if opp_forks_after == 0 else 0,
            len(opp_forks_before) - opp_forks_after,
            -opp_forks_after,
            our_wins_after,
            1 if _is_side(move) and _has_opposite_corners(board, opp) and board[CENTER] == player else 0,
            _position_score(move),
        )
        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def find_opposite_corner_move(board: Board, player: int) -> Optional[int]:
    """Find an opposite corner move when the center is already controlled."""
    if board[CENTER] != player:
        return None

    opp = opponent(player)
    best_move: Optional[int] = None
    best_score = (-1, -1)

    for corner in CORNERS:
        if board[corner] != opp:
            continue

        opposite = _opposite_corner(corner)
        if opposite is None or board[opposite] != config.EMPTY:
            continue

        score = (1 if _is_corner(opposite) else 0, -opposite)
        if score > best_score:
            best_score = score
            best_move = opposite

    return best_move


def find_positional_move(board: Board, player: int) -> int:
    """Choose the strongest remaining move by board position."""
    moves = available_moves(board)
    if not moves:
        raise ValueError("No available moves")

    opp = opponent(player)
    best_move = moves[0]
    best_score = (-10**9, -10**9, -10**9, -10**9, -10**9, -10**9)

    for move in moves:
        after = make_move(board, move, player)
        score = (
            1 if _is_corner(move) else 0,
            1 if _is_side(move) else 0,
            _position_score(move),
            len(_winning_moves(after, player)),
            -len(_winning_moves(after, opp)),
            -len(_fork_moves(after, opp)),
        )
        if score > best_score:
            best_score = score
            best_move = move

    return best_move


class LegacyStrategicMoveFinder:
    """Purely heuristic strategic move finder."""

    def __init__(self, player: int):
        self.player = player

    def choose_move(self, board: Board) -> int:
        """Choose a move using a strict heuristic priority order."""
        moves = available_moves(board)
        if not moves:
            raise ValueError("No available moves for strategic AI")

        move = find_opening_move(board, self.player)
        if move is not None:
            return move

        move = find_winning_move(board, self.player)
        if move is not None:
            return move

        move = find_blocking_move(board, self.player)
        if move is not None:
            return move

        move = find_fork_move(board, self.player)
        if move is not None:
            return move

        move = find_fork_block_move(board, self.player)
        if move is not None:
            return move

        move = find_opposite_corner_move(board, self.player)
        if move is not None:
            return move

        return find_positional_move(board, self.player)


StrategicMoveFinder = LegacyStrategicMoveFinder
