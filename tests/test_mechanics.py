import unittest

from stone_game.board import Board
from stone_game.mechanics import Mechanics
from stone_game.piece import Piece, StoneState
from stone_game.player import Player

class MechanicsTestCase(unittest.TestCase):
  def setUp(self):
    self.board = Board()
    self.player1 = Player('p1', '1')
    self.player2 = Player('p2', '2')
    self.mechanics = Mechanics(self.player1, self.player2)

  def testTurnCounter(self):
    p = self.player1.inactive_piece()
    self.mechanics.place_piece(self.board, p, 1)
    self.assertEqual(self.mechanics.turn_counter, 1)
    self.assertEqual(self.mechanics.active_player(), self.player2, 'the turn did not increment')
    self.assertEqual(self.mechanics.inactive_player(), self.player1, 'the inactive_player is not correct')

  def testMoves(self):
    # populate the board, ignore mills
    for i in range(0,18):
      if i%2 == 0:
        p = self.player1.inactive_piece()
        self.board.add_piece(p, i+1)
      else:
        p = self.player2.inactive_piece()
        self.board.add_piece(p, i+1)

    # player1 can only move to 17 to 24
    player = self.mechanics.active_player()
    movable_pieces = self.mechanics.movable_pieces(self.board, player)
    move_set = [p.position for p in movable_pieces]
    self.assertEqual(move_set, [17], 'a piece which should be movable is not')
    moves_for_piece = self.mechanics.moves_for_piece(self.board, 17)
    self.assertEqual(moves_for_piece, {24})

    with self.assertRaises(ValueError):
      self.mechanics.move_piece(self.board, 19, 24)
    self.mechanics.move_piece(self.board, 17, 24)

    # player2 has more options
    player = self.mechanics.active_player()
    self.assertEqual(player, self.player2)
    movable_pieces = self.mechanics.movable_pieces(self.board, player)
    move_set = {p.position for p in movable_pieces}
    self.assertEqual(move_set, {18, 12, 14})

  def testLongMoves(self):
    stones = self.player1.remaining_unplaced()
    self.board.add_piece(stones[0], 1)
    self.board.add_piece(stones[1], 2)
    self.board.add_piece(stones[2], 5)
    moves = self.mechanics.moves_for_piece(self.board, 1)
    self.assertEqual(moves, {8,7}, 'single long move not registering')
    moves = self.mechanics.moves_for_piece(self.board, 5)
    self.assertEqual(moves, {3,4,6,7}, 'two long moves not registering')
    # check that we can't do long moves when more than three pieces
    self.board.add_piece(stones[3], 6)
    moves = self.mechanics.moves_for_piece(self.board, 6)
    self.assertEqual(moves, {7,14}, 'we can do a long move when >3 pieces')

  def testMillCheck(self):
    player = self.mechanics.active_player()
    for i in range(1,4):
      p = player.inactive_piece()
      self.board.add_piece(p, i)

    self.assertTrue(self.mechanics.mill_check(self.board, 3, player), 'a mill was not detected')

  def testMillCheckAfterPlace(self):
    player = self.mechanics.active_player()
    stones = player.remaining_unplaced()
    self.board.add_piece(stones[0], 1)
    self.board.add_piece(stones[1], 2)

    # adding a stone at position 3 makes a mill
    self.assertTrue(self.mechanics.place_piece(self.board, stones[2], 3))
    # it is still player1's turn to steal a piece
    self.assertEqual(self.mechanics.turn_counter, 0, 'the turn should not change after placing into a mill')

  def testMillCheckAfterMove(self):
    player = self.mechanics.active_player()
    stones = player.remaining_unplaced()
    self.board.add_piece(stones[0], 1)
    self.board.add_piece(stones[1], 2)
    self.board.add_piece(stones[2], 4)

    # moving from 4 to 3 makes a mill
    self.assertTrue(self.mechanics.move_piece(self.board, 4, 3))
    # it is still player1's turn to steal a piece
    self.assertEqual(self.mechanics.turn_counter, 0, 'the turn should not change after moving into a mill')

