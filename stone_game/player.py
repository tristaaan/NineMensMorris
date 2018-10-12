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

  def make_placement(self, open_spots, board=None):
    """
    Given a board, return a possible placement
    """
    return (self.inactive_piece(),
      self.take_input('Place piece: ',          \
                      'You cannot place there', \
                      open_spots)
      )
  def make_move(self, possible_positons, moves_map, board=None):
    """
    Make a move for a stone
    possible_moves: a list of possible positions
    """
    at = self.take_input('Move piece at: ', \
                         'You cannot move that piece',      \
                         possible_positions),

    print('Possible moves: ', moves_map[at])
    to = self.take_input('Move piece to: ',       \
                         'You cannot move there', \
                         moves_map[at])
    return (at, to)

  def make_steal_move(self, stealable, opponent=None, board=None):
    """
    Choose a piece to steal
    stealable: a list of stealable positions
    """
    return self.take_input(                          \
          'Which piece would you like to remove?: ', \
          'You cannot remove that piece',            \
          stealable)

  def take_input(self, text, error, valid_ints):
    try:
      inp = int(input(text))
      if inp in valid_ints:
        return inp
      raise NameError(error)
    except NameError:
      print(error)
    except ValueError:
      print('Thats not a number')

    return self.take_input(text, error, valid_ints)

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
