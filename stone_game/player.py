from .piece import Piece, StoneState


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
