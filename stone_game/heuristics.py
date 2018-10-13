import copy

from .rules import mills
from .piece import Piece

class Heuristics(object):

  def __init__(self, player):
    self.player = player

  def creates_mill(self, board, at):
    """
    Check if placing a piece at `at` a mill
    board: board
    at: the spot on the board to check
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
    board: board
    at: the spot on the board to check
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
    board: board
    at: the spot on the board to check
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
    """
    Count the number of opponent pieces adjacent to `at` on the board
    board: board
    at: the spot on the board to check
    """
    edges = board[at].edges
    count = 0
    for n in edges:
      if board[n].piece != None and board[n].piece.owner != self.player.name:
        count += 1
    return count

  def open_adjacent(self, board, at):
    """
    Count the number of empty spaces adjacent to `at` on the board
    board: board
    at: the spot on the board to check
    """
    edges = board[at].edges
    count = 0
    for n in edges:
      if board[n].piece == None:
        count += 1
    return count
