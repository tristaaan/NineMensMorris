import unittest

from stone_game.board import Board
from stone_game.heuristics import Heuristics
from stone_game.rules import Rules
from stone_game.piece import Piece, StoneColor
from stone_game.player import Player

class HeuristicsTestCase(unittest.TestCase):

  def create_pieces(self, player, count=5):
    player_name = player.name
    player_icon = player.icon
    stones = []
    for i in range(count):
      stones.append(Piece(player_name, player_icon))
    return stones

  def setUp(self):
    self.p1 = Player('Alice', StoneColor.BLACK)
    self.p2 = Player('Bob', StoneColor.WHITE)
    self.h = Heuristics(self.p1)
    self.board = Board()

  def testOpenAdjacent(self):
    stones = self.create_pieces(self.p1)
    self.board.add_piece(stones[0], 1)
    self.assertEqual(self.h.open_adjacent(self.board, 2), 2,
      'Wrong count for open spot')

  def testOpponentAdjacent(self):
    s1 = self.create_pieces(self.p1)
    s2 = self.create_pieces(self.p2)
    self.board.add_piece(s2[0], 1)
    self.board.add_piece(s2[1], 3)
    self.board.add_piece(s2[3], 10)
    self.assertEqual(self.h.opponent_adjacent(self.board, 2), 3,
      'Wrong count for opponent-adjacent')