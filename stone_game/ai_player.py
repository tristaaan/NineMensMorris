from .player import Player
from .piece import StoneColor
from .ai import AI, Difficulty

class AIPlayer(Player):
  """
  A container for pieces and the player name
  name: the player's name
  icon: the piece icons
  reserves: an array of Pieces, initialized in the constructor
  """

  def __init__(self, name, icon, difficulty=Difficulty.HARD):
    super().__init__(name, icon)
    self.difficulty = difficulty
    self.engine = AI(self, difficulty)

  def make_placement(self, possible_positions, board=None):
    return (self.inactive_piece(),
      self.engine.place_stone(board, self))

  def make_move(self, movable, moves_map, board=None):
    return self.engine.move_stone(board, self, movable, moves_map)

  def make_steal_move(self, stealable, opponent=None, board=None):
    return self.engine.steal_stone(board, stealable, opponent)