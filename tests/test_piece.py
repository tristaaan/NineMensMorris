import unittest

from stone_game.piece import Piece, StoneState


class PieceTestCase(unittest.TestCase):
  def testStorage(self):
    name = 'p1'
    icon = 'o'
    p = Piece(name, icon)
    self.assertEqual(p.owner, name)
    self.assertEqual(p.icon, icon)

  def testStates(self):
    p = Piece('p1', 'x')
    self.assertEqual(p.position, 0)
    self.assertEqual(p.state, StoneState.UNPLACED)

    p.set_active(12)
    self.assertEqual(p.position, 12)
    self.assertEqual(p.state, StoneState.IN_PLAY)

    p.remove_from_play()
    self.assertEqual(p.position, 0)
    self.assertEqual(p.state, StoneState.CAPTURED)

