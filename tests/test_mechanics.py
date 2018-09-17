import unittest

from stone_game.board import Board
from stone_game.mechanics import Mechanics
from stone_game.piece import Piece, StoneState
from stone_game.player import Player

class MechanicsTestCase(unittest.TestCase):
  def setUp(self):
    self.board = Board()
    self.player1 = Player('p1', 'x')
    self.player2 = Player('p2', 'o')
    self.mechanics = Mechanics(self.player1, self.player2)

  def testTurnCounter(self):
    p = self.player1.inactive_piece()
    self.mechanics.place_piece(self.board, p, 1)
    self.assertEqual(self.mechanics.turn_counter, 1)
    self.assertEqual(self.mechanics.active_player(), self.player2)

  def testMoves(self):
    # populate the board
    for i in range(1,19):
      player = self.mechanics.active_player()
      p = player.inactive_piece()
      self.mechanics.place_piece(self.board, p, i)

    # player1 can only move to 24
    player = self.mechanics.active_player()
    moves = self.mechanics.available_moves(self.board, player)
    self.assertEqual(moves, {24})

    with self.assertRaises(ValueError):
      self.mechanics.move_piece(self.board, 19, 24)

    # player2 has more options
    self.mechanics.move_piece(self.board, 17, 24)
    player = self.mechanics.active_player()
    self.assertEqual(player, self.player2)
    moves = self.mechanics.available_moves(self.board, player)
    self.assertEqual(moves, {17, 19, 20, 22})

  def testMillCheck(self):
    player = self.mechanics.active_player()
    for i in range(1,4):
      p = player.inactive_piece()
      self.board.add_piece(p, i)

    self.assertTrue(self.mechanics.mill_check(self.board, 3))
