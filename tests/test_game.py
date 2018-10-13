import unittest
from unittest.mock import patch

from stone_game.game import Game
from stone_game.board import Board
from stone_game.player import Player
from stone_game.piece import StoneState, StoneColor

class GameTestCase(unittest.TestCase):
  def setUp(self):
    p1 = Player('Player1', StoneColor.BLACK)
    p2 = Player('Player2', StoneColor.WHITE)
    self.game = Game(p1, p2)

  def testEndOfPlacePhase(self):
    for i in range(0,17):
      if i % 2 == 0:
        p = self.game.player1.inactive_piece()
        self.game.board.add_piece(p, i+1)
      else:
        p = self.game.player2.inactive_piece()
        self.game.board.add_piece(p, i+1)

    self.assertTrue(self.game.place_phase_conditional(), \
                    'The place phase ended early')

    p = self.game.player2.inactive_piece()
    self.game.board.add_piece(p, 18)

    self.assertFalse(self.game.place_phase_conditional(), \
                    'The place phase did not end')


  def testConditionalWhereNotEnoughPieces(self):
    player1 = self.game.rules.active_player()
    stones = player1.remaining_unplaced()
    self.game.board.add_piece(stones[0], 1)
    self.game.board.add_piece(stones[1], 2)
    self.game.board.add_piece(stones[2], 3)

    self.assertTrue(self.game.move_phase_conditional(),
                    'The game stopped early when testing not enough pieces')
    self.game.board.remove_piece(2)
    stones[1].state = StoneState.CAPTURED
    self.assertFalse(self.game.move_phase_conditional(),
                    'The game did not end when no moves')

  def testConditionalWhereNoMoves(self):
    # populate a board with cornered pieces
    player1 = self.game.rules.active_player()
    stones = player1.remaining_unplaced()
    self.game.board.add_piece(stones[0], 1)
    self.game.board.add_piece(stones[1], 3)
    self.game.board.add_piece(stones[2], 7)
    self.game.board.add_piece(stones[3], 5)

    player2 = self.game.rules.inactive_player()
    stones = player2.remaining_unplaced()
    self.game.board.add_piece(stones[0], 2)
    self.game.board.add_piece(stones[1], 4)
    self.game.board.add_piece(stones[2], 6)

    self.assertTrue(self.game.move_phase_conditional(),
                    'The game stopped early when testing no moves')
    self.game.board.add_piece(stones[3], 8)
    self.assertFalse(self.game.move_phase_conditional(),
                     'The game did not end when no moves')
