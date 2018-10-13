from enum import Enum


class StoneState(Enum):
  """
  Constants for the stone states
  """
  UNPLACED = 'UNPLACED'
  IN_PLAY = 'IN_PLAY'
  CAPTURED = 'CAPTURED'

class StoneColor(Enum):
  BLACK='●'
  WHITE='○'

class Piece(object):
  """
  A piece class
  icon: what shows when the piece is printed
  owner: who's piece this is
  state: one state of StoneStates
  position: the location of the piece on the board, 0 is none
  """
  icon = ''
  state = StoneState.UNPLACED

  def __init__(self, player_name, piece_icon):
    self.owner = None
    self.position = 0
    self.owner = player_name
    self.icon = piece_icon

  def __repr__(self):
    """
    How the piece gets printed as a raw object
    """
    return '<Piece: %s %s>' % (self.owner, self.icon)

  def __str__(self):
    """
    How the piece gets printed in a print()
    """
    return self.icon

  def set_active(self, at):
    """
    Sets the piece to the IN_PLAY state
    at: the new position of the node
    """
    self.position = at
    self.state = StoneState.IN_PLAY

  def remove_from_play(self):
    """
    Sets the piece to the CAPTURED state, sets position to 0
    """
    self.position = 0
    self.state = StoneState.CAPTURED
