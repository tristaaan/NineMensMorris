import copy

from .rules import mills
from .piece import Piece
from .rules import Rules

class Heuristics(object):

  def __init__(self, player):
    self.player = player
    self.rules = Rules(player, None)

  def creates_mill(self, board, at):
    """
    Check if placing a piece at `at` a mill
    """
    test_board = copy.deepcopy(board)
    faux_piece = Piece(self.player.name, self.player.icon)
    test_board.add_piece(faux_piece, at)
    for mill in mills:
      if at in mill:
        pieces = test_board.get_pieces(mill)
        if [p != None and p.owner == self.player.name for p in pieces].count(True) == 3:
          return True
        continue
    return False

  def creates_semi_mill(self, board, at):
    """
    Check if placing a piece at `at` forms 2/3rds of a mill
    """
    test_board = copy.deepcopy(board)
    faux_piece = Piece(self.player.name, self.player.icon)
    test_board.add_piece(faux_piece, at)

    for mill in mills:
      if at in mill:
        pieces = test_board.get_pieces(mill)
        if [p != None and p.owner == self.player.name for p in pieces].count(True) == 2:
          return True
        continue
    return False

  def blocks_mill(self, board, at):
    """
    Check if placing a piece at `at` blocks a mill
    very similar to `creates_semi_mill` note the != in
    the inner-most conditional
    """
    test_board = copy.deepcopy(board)
    faux_piece = Piece(self.player.name, self.player.icon)
    test_board.add_piece(faux_piece, at)

    for mill in mills:
      if at in mill:
        pieces = test_board.get_pieces(mill)
        if [p != None and p.owner != self.player.name for p in pieces].count(True) == 2:
          return True
        continue
    return False

  def opponent_adjacent(self, board, at):
    edges = board[at].edges
    count = 0
    for n in edges:
      if board[n].piece != None and board[n].piece.owner == self.player.name:
        count += 1
    return count

  def movable_pieces(self, board):
    return self.rules.movable_pieces(board, self.player)

  def moves_for_piece(self, board, at):
    return self.rules.moves_for_piece(board, at)

  def open_adjacent(self, board, at):
    edges = board[at].edges
    count = 0
    for n in edges:
      if board[n].piece == None:
        count += 1
    return count
