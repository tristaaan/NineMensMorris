

# hard coded, used in heuristics too
# keep the indexing pattern in-line with the board
# An array of 3 length arrays which are mills on the board
mills = [
  [1, 2,  3], [3, 4, 5 ], [5,  6, 7], [7, 8, 1], # outer
  [9, 10,11], [11,12,13], [13,14,15], [15,16,9], # middle
  [17,18,19], [19,20,21], [21,22,23], [23,24,17], # inner
  [2, 10,18], [4, 12,20], [6, 14,22], [8, 16,24]  # cross mills
]

class Rules(object):
  """
  Rules and game mechanics for the Stone Game
  turn_counter: Keeping track which turn it is
  player1: Player 1
  player2: Player 2
  """

  def __init__(self, player1, player2):
    super().__init__()
    self.turn_counter = 0
    self.player1 = player1
    self.player2 = player2

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
    mill = self.mill_check(board, at, self.active_player())
    if not mill:
      self.turn_counter += 1
    return mill

  def move_piece(self, board, at, to):
    """
    Place piece on the board
    board: the board the is piece on
    at: the name of the node the piece is being moved
    to: name of node to move the piece to
    """
    player = self.active_player()
    if board.get_piece(at) == None:
      raise ValueError('There is no piece at %d' % at)
    if board.get_piece(at).owner != player.name:
      raise ValueError('You cannot move piece at %d, it is not yours' % at)
    elif board.get_piece(to) != None:
      raise ValueError('You cannot move to %d there is already a piece there' % to)
    elif to not in board.nodes[at].edges and len(player.remaining_in_play()) > 3:
      raise ValueError('You cannot move to %d to %d, they are not adjacent' % (at, to))

    moving_piece = board.remove_piece(at)
    board.add_piece(moving_piece, to)

    mill = self.mill_check(board, to, player)
    if not mill:
      self.turn_counter += 1
    return mill

  def movable_pieces(self, board, player):
    """
    Get a list of the available pieces that a player can move
    board: the board
    player: the player
    """
    available_pieces = player.remaining_in_play()
    ret = []
    for p in available_pieces:
      adjacent = board.nodes[p.position].edges
      empty_adjacents = [a for a in adjacent if board.get_piece(a) == None]
      if empty_adjacents:
        ret.append(p)
    return ret

  def moves_for_piece(self, board, at):
    """
    Get a list of available moves for a piece
    board: board
    at: piece to get moves from
    """
    adjacent = board.nodes[at].edges
    open_spots = {a for a in adjacent if board.get_piece(a) == None}
    # gather long moves.
    if len(self.active_player().remaining_in_play()) == 3 and \
       at not in [10,12,14,16]: # we cannot make long moves from these spots
      for mill in mills:
        # print(at, mill, board.get_pieces(mill))
        if at in mill and board.get_pieces(mill).count(None) == 2:
          open_spots.update([m for m in mill if m != at])
    return open_spots


  def mill_check(self, board, at, player):
    """
    Check for a mill given a piece
    board: the board to read to find a mill
    at: position the node to check if it's in a mill
    """
    for mill in mills:
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

  def stealable_pieces(self, board):
    """
    Returns a list of all pieces that can be stolen from the inactive player
    :param board:
    :return:
    """
    enemy_pieces = self.inactive_player().remaining_in_play()
    pieces_not_in_mill = {a.position for a in enemy_pieces if not self.mill_check(board, a.position, self.inactive_player())}
    if not len(pieces_not_in_mill) == 0:
      return pieces_not_in_mill

    pieces_in_mill = {a.position for a in enemy_pieces if self.mill_check(board, a.position, self.inactive_player())}
    return pieces_in_mill

  def steal_piece(self,piece_to_remove,board):
    """
    Remove piece_to_remove from the board.

    :param piece_to_remove:
    :param board:
    :return:
    """
    piece = board.get_piece(piece_to_remove)
    piece.remove_from_play()
    board.remove_piece(piece_to_remove)
    self.turn_counter += 1
    return
