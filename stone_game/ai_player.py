from .player import Player
from .piece import StoneColor
from .ai import AI, Difficulty

class AIPlayer(Player):
  """
  AIPlayer a subclass of player
  Overrides and automates methods pertaining to
  stone placement, movement, and stealing
  """

  def __init__(self, name, icon, difficulty=Difficulty.HARD):
    super().__init__(name, icon)
    self.difficulty = difficulty
    self.engine = AI(self, difficulty)

  def make_placement(self, possible_positions, board=None):
    """
    Make a placement
    """
    return (self.inactive_piece(),
      self.engine.place_stone(board, self))

  def make_move(self, movable, moves_map, board=None):
    """
    Make a move, returns a tuple (at, to)
    """
    return self.engine.move_stone(board, self, movable, moves_map)

  def make_steal_move(self, stealable, opponent=None, board=None):
    """
    Choose a piece to steal
    """
    return self.engine.steal_stone(board, stealable, opponent)