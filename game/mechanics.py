from constants import GamePhases


class Mechanics(object):

  mills = [
    [1, 2,  3], [3, 4, 5 ], [5,  6, 7], [7, 8, 1], # outer
    [9, 10,11], [11,12,13], [13,14,15], [15,16,9], # middle
    [17,18,19], [19,20,21], [21,22,23], [23,24,17], # inner
    [2, 10,18], [4, 12,20], [6, 14,22], [8, 16,24]  # cross mills
  ]
  game_phase = GamePhases.PLACE_PHASE
  turn_counter = 0

  def __init__(self, player1, player2):
    self.player1 = player1
    self.player2 = player2

  def place_piece(self, board, piece, at):
    try:
      board.add_piece(piece, at)
    except ValueError as e:
      print(e)
      return
    player = self.active_player().name
    if self.mill_check(board, at):
        print('%s made a mill!' % player)
        print('~~~STEALING UNIMPLEMENTED~~~')
    self.turn_counter += 1
    board.draw()

  def move_piece(self, board, at, to):
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

    if self.mill_check(board, to):
      print('%s made a mill!' % player)
      print('~~~STEALING UNIMPLEMENTED~~~')
    self.turn_counter += 1
    board.draw()

  def available_moves(self, board, player):
    available_pieces = board.get_pieces(belonging_to=player.name)
    ret = set()
    for p in available_pieces:
      adjacent = board.nodes[p.position].edges
      open_spots = {a for a in adjacent if board.get_piece(a) == None}
      ret = ret | open_spots
    return ret

  def mill_check(self, board, at):
    player = self.active_player()
    for mill in self.mills:
      if at in mill:
        pieces = board.get_pieces(mill)
        if [p != None and p.owner == player for p in pieces].count(True) == 3:
          return True
        continue
    return False

  def active_player(self):
    if self.turn_counter % 2 == 0:
      return self.player1
    return self.player2
