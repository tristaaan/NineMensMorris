

class StoneStates(object):
  UNPLACED = 'UNPLACED'
  IN_PLAY = 'IN_PLAY'
  CAPTURED = 'CAPTURED'


class Piece(object):
  icon = ''
  owner = None
  state = StoneStates.UNPLACED
  position = 0

  def __init__(self, player_name, piece_icon):
    self.owner = player_name
    self.icon = piece_icon

  def __repr__(self):
    return '<Piece: %s %s>' % (self.owner, self.icon)

  def __str__(self):
    return self.icon

  def set_active(self, at):
    self.position = at
    self.state = StoneStates.IN_PLAY

  # def move(self, to):
  #   self.position = to

  def remove_from_play(self):
    self.position = 0
    self.state = StoneStates.CAPTURED