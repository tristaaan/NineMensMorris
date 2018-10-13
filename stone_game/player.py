from .piece import Piece, StoneState
from .util import take_input


class Player(object):
  """
  A container for pieces and the player name
  name: the player's name
  icon: the piece icons
  reserves: an array of Pieces, initialized in the constructor
  """
  def __init__(self, name, icon):
    self.name = name
    self.icon = icon
    self.reserves = []
    for i in range(9):
      self.reserves.append(Piece(self.name, self.icon))

  def __str__(self):
    """
    What to show when this is in a print()
    """
    return self.name

  def make_placement(self, open_spots, board=None):
    """
    Place a stone
    open_spots: possible placements
    board: board, used in AIPlayer
    """
    return (self.inactive_piece(),
      take_input('Place piece: ',
                 'You cannot place there',
                 open_spots)
      )
  def make_move(self, possible_positions, moves_map, board=None):
    """
    Make a move for a stone, returns a tuple (at, to)
    possible_positons: a list of possible stones to move
    moves_map: a dict of {stone: [moves]}
    board: board, used in AIPlayer
    """
    at = take_input('Move piece at: ',            \
                    'You cannot move that piece', \
                    possible_positions)

    print('Possible moves: ', moves_map[at])
    to = take_input('Move piece to: ',       \
                    'You cannot move there', \
                    moves_map[at])
    return (at, to)

  def make_steal_move(self, stealable, opponent=None, board=None):
    """
    Choose a piece to steal
    stealable: a list of stealable positions
    opponent: the opposing player, used in AIPlayer
    board: board, used in AIPlayer
    """
    return take_input(                           \
      'Which piece would you like to remove?: ', \
      'You cannot remove that piece',            \
      stealable)

  def remaining_unplaced(self):
    """
    Get a list of unplaced pieces
    """
    ret = []
    for piece in self.reserves:
      if piece.state == StoneState.UNPLACED:
        ret.append(piece)
    return ret

  def remaining_in_play(self):
    """
    Get a list of the pieces that are still in play
    """
    ret = []
    for piece in self.reserves:
      if piece.state == StoneState.IN_PLAY:
        ret.append(piece)
    return ret

  def inactive_piece(self):
    """
    get a piece that has not been placed yet
    """
    for piece in self.reserves:
      if piece.state == StoneState.UNPLACED:
        return piece
    return None
