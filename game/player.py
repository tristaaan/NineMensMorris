from piece import Piece, StoneStates


class Player(object):

  def __init__(self, name, icon):
    self.name = name
    self.icon = icon
    self.reserves = []
    for i in range(9):
      self.reserves.append(Piece(self.name, self.icon))

  def __str__(self):
    return self.name

  def remaining(self):
    val = 0
    for piece in self.reserves:
      if piece.state == StoneStates.IN_PLAY:
        val += 1
    return val

  def inactive_piece(self):
    for piece in self.reserves:
      if piece.state == StoneStates.UNPLACED:
        return piece
    return None
