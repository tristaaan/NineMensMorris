

class Mechanics(object):
  """
  Rules and game mechanics for the Stone Game
  mills: An array of 3 length arrays which are mills on the board
  turn_counter: Keeping track which turn it is
  player1: Player 1
  player2: Player 2
  """

  # hard coded, this should maybe be in the board class to
  # keep the indexing pattern in-line with the board
  mills = [
    [1, 2,  3], [3, 4, 5 ], [5,  6, 7], [7, 8, 1], # outer
    [9, 10,11], [11,12,13], [13,14,15], [15,16,9], # middle
    [17,18,19], [19,20,21], [21,22,23], [23,24,17], # inner
    [2, 10,18], [4, 12,20], [6, 14,22], [8, 16,24]  # cross mills
  ]

  def __init__(self, player1, player2, drawing=False):
    self.turn_counter = 0
    self.player1 = player1
    self.player2 = player2
    self.drawing = drawing

  def place_piece(self, board, piece, at):
    """
    Place piece on the board
    board: the board to place the piece on
    piece: the piece being placed
    at: the name of the node the piece is being placed on
    """
    try:
      board.add_piece(piece, at)
    except ValueError as e:
      print(e)
      return
    if self.drawing:
      board.draw()
    return self.mill_check(board, at, self.active_player())

  def move_piece(self, board, at, to):
    """
    Place piece on the board
    board: the board the is piece on
    at: the name of the node the piece is being moved
    to: name of node to move the piece to
    """
    player = self.active_player().name
    if board.get_piece(at) == None:
      raise ValueError('There is no piece at %d' % at)
    if board.get_piece(at).owner != player:
      raise ValueError('You cannot move piece at %d, it is not yours' % at)
    elif board.get_piece(to) != None:
      raise ValueError('You cannot move to %d there is already a piece there' % to)
    elif to not in board.nodes[at].edges:
      raise ValueError('You cannot move to %d to %d, they are not adjacent' % (at, to))

    moving_piece = board.remove_piece(at)
    board.add_piece(moving_piece, to)

    if self.drawing:
      board.draw()
    return self.mill_check(board, at, self.active_player())

  def available_moves(self, board, player):
    """
    Get a set of available moves
    board: board
    player: whose pieces to fetch from the board
    """
    available_pieces = player.remaining()
    ret = set()
    for p in available_pieces:
      adjacent = board.nodes[p.position].edges
      open_spots = {a for a in adjacent if board.get_piece(a) == None}
      ret = ret | open_spots
    return ret

  def available_at(self,board,player):
    """
    returns the available pieces that can be moved
    """
    available_pieces = player.remaining()
    ret = set()
    for p in available_pieces:
      adjacent = board.nodes[p.position].edges
      moveable_pieces = {p for a in adjacent if board.get_piece(a) == None}
      ret = ret | moveable_pieces
    return ret

  def available_to(self,board,at):
    """
    returns the open spots for at to be moved to
    """
    adjacent = board.nodes[at.position].edges
    open_spots = {a for a in adjacent if board.get_piece(a) == None}
    return open_spots


  def mill_check(self, board, at, player):
    """
    Check for a mill given a piece
    board: the board to read to find a mill
    at: name of the node to check if its in a mill
    """
    for mill in self.mills:
      if at in mill:
        pieces = board.get_pieces(mill)
        if [p != None and p.owner == player.name for p in pieces].count(True) == 3:
          return True
        continue
    return False

  def active_player(self):
    """
    Get the active player
    """
    if self.turn_counter % 2 == 0:
      return self.player1
    return self.player2

  def inactive_player(self):
    """
    Get the inactive player
    """
    if self.turn_counter % 2 == 0:
      return self.player2
    return self.player1

  def steal_piece_1(self, board):
    enemy_pieces = self.inactive_player().remaining()
    pieces_not_in_mill = {a.position for a in enemy_pieces if not self.mill_check(board, a.position, self.inactive_player())}
    if not len(pieces_not_in_mill) == 0:
      return pieces_not_in_mill

    pieces_in_mill = {a.position for a in enemy_pieces if self.mill_check(board, a.position, self.inactive_player())}
    return pieces_in_mill

  def steal_piece_2(self,piece_to_remove,board):
    piece = board.get_piece(piece_to_remove)
    piece.remove_from_play()
    board.remove_piece(piece_to_remove)
    return
