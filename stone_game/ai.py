import copy
from random import randint
from .heuristics import Heuristics


class AI():
    def __init__(self, player, difficulty):
        self.difficulty = difficulty
        self.heuristics = Heuristics(player)

    def _scoring(self, board, pos, player):
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
        if self.heuristics.open_adjacent(board, pos) > 1:
            score += 1

        # Adjust score with some random value based on difficulty
        if self.difficulty == 1:  # Easy difficulty
            score -= randint(1, 4)
        elif self.difficulty == 2:  # Medium difficulty
            score -= randint(0, 2)
        return score

    def _bestPlacement(self, color, phase):
        # TODO
        pass

    def place_stone(self, board, player):
        bestPosition = None
        best_score = -100
        for n in range(1, 25):
            if board[n].piece == None:
                score = self._scoring(board, n, player)
                if score > best_score:
                    best_score = score
                    bestPosition = n
        return bestPosition

    def move_stone(self, board, player):
        test_board = copy.deepcopy(board)
        best_score = -100
        best_new_position = None
        best_movable_stone = None
        stones = player.remaining_in_play()
        for s in stones:
            possible_moves = self.heuristics.moves_for_piece(board, s.position)
            current_position = s.position
            piece = test_board.remove_piece(current_position)
            for pos in possible_moves:
                score = self._scoring(board, pos, player)
                if score > best_score:
                    best_score = score
                    best_movable_stone = s.position
                    best_new_position = pos
            test_board.add_piece(piece, current_position)
        return (best_movable_stone, best_new_position)

    def steal_stone(self, board, stealable, opponent):
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
