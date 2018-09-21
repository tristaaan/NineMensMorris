import unittest

from stone_game.board import Board
from stone_game.player import Player


class PlayerTestCase(unittest.TestCase):
  def testStorage(self):
    p = Player('player1', 'x')
    self.assertEqual(p.name, 'player1', 'name not stored')
    self.assertEqual(p.icon, 'x', 'icon not stored')

  def testReserves(self):
    board = Board()
    player = Player('player1', 'x')
    self.assertEqual(len(player.reserves), 9,
                     'player has more than nine pieces')

    rem = player.remaining_in_play()
    self.assertEqual(len(rem), 0, 'new player has pieces in play')

    for i in range(1,10):
      piece = player.inactive_piece()
      board.add_piece(piece, i)

    rem = player.remaining_in_play()
    self.assertEqual(len(rem), 9, 'player does not have all pieces in play')
