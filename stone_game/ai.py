import copy
from enum import Enum
from random import randint
from .heuristics import Heuristics

class Difficulty(Enum):
    """
    Difficulty levels
    """
    EASY   = 1
    MEDIUM = 2
    HARD   = 3

class AI():
    """
    The core of the Engine component
    difficulty: a difficulty level
    heuristics: a heuristics object to evaluate the board
    """
    def __init__(self, player, difficulty):
        self.difficulty = difficulty
        self.heuristics = Heuristics(player)

    def _scoring(self, board, pos, player):
        """
        Score a position
        board: board
        pos: position to inspect
        player: player making the move
        """
        score = 0
        # score mill creation
        if self.heuristics.creates_mill(board, pos):
            score += 10
        # score partial mill
        if self.heuristics.creates_semi_mill(board, pos):
            score += 3
        # score  blocking mill
        if self.heuristics.blocks_mill(board, pos):
            score += 7
        elif self.heuristics.opponent_adjacent(board, pos) > 0:
            score -= 2

        # score position
        if len(board[pos].edges) == 4: # 4 crossing
            score += 2
        elif len(board[pos].edges) == 3: # 3 crossing
            score += 1

        # score openness
        if self.heuristics.open_adjacent(board, pos) >= 1:
            score += 1

        # Adjust score with some random value based on difficulty
        if self.difficulty == Difficulty.EASY:
            score -= randint(1, 30)
        elif self.difficulty == Difficulty.MEDIUM:
            score -= randint(0, 11)
        return score

    def place_stone(self, board, player):
        """
        Find the best placement
        board: board
        player: the player which is placing
        """
        bestPosition = None
        best_score = -100
        for n in range(1, 25):
            if board[n].piece == None:
                score = self._scoring(board, n, player)
                if score > best_score:
                    best_score = score
                    bestPosition = n
        return bestPosition

    def move_stone(self, board, player, movable, move_map):
        """
        Find the best stone to move and where to move it to,
        returns a tuple (at, to)
        board: board
        player: the player which is moving
        movable: moveable stones
        move_map: a dict of {stone: [moves]}
        """
        test_board = copy.deepcopy(board)
        best_score = -100
        best_new_position = None
        best_movable_stone = None
        for s in movable:
            possible_moves = move_map[s]
            piece = test_board.remove_piece(s)
            for pos in possible_moves:
                score = self._scoring(test_board, pos, player)
                if score > best_score:
                    best_score = score
                    best_movable_stone = s
                    best_new_position = pos
            test_board.add_piece(piece, s)
        return (best_movable_stone, best_new_position)

    def steal_stone(self, board, stealable, opponent):
        """
        Find the best stone to steal
        board: board
        stealable: a list of stealable stones
        opponent: the opponent
        """
        test_board = copy.deepcopy(board)
        best_position = None
        best_score = -100
        for s in stealable:
            piece = test_board.remove_piece(s)
            score = self._scoring(test_board, s, opponent)
            if score > best_score:
                best_position = s
                best_score = score
            test_board.add_piece(piece, s)
        return best_position
