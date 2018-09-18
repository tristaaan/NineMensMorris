import unittest

from stone_game.board import Board
from stone_game.piece import Piece, StoneState


class BoardTestCase(unittest.TestCase):
  def create_pieces(self, count=5):
    player_name = 'p1'
    player_icon = 'x'
    stones = []
    for i in range(count):
      stones.append(Piece(player_name, player_icon))
    return stones

  # test that for each node a with an edge to b
  # node b has an edge to a
  def testEdges(self):
    board = Board()
    for i in range(1,25):
      edges = board.nodes[i].edges
      for e in edges:
        self.assertTrue(i in board.nodes[e].edges,
                        'no edge from %d to %d' % (e, i))

  def testAddPiece(self):
    board = Board()
    stones = self.create_pieces()

    board.add_piece(stones[0], 1)
    with self.assertRaises(ValueError):
      board.add_piece(stones[1], 1)

    self.assertEqual(stones[0].position, 1)
    self.assertEqual(stones[0].state, StoneState.IN_PLAY)

  def testRemovePiece(self):
    board = Board()
    stones = self.create_pieces()

    board.add_piece(stones[0], 1)
    board.add_piece(stones[1], 2)
    board.add_piece(stones[2], 3)

    with self.assertRaises(ValueError):
      board.remove_piece(4)

    p = board.remove_piece(3)
    self.assertEqual(p, stones[2])
    self.assertEqual(p.position, 0)
    self.assertIsNone(board.nodes[3].piece, 'piece not removed')

  def testGetPiece(self):
    board = Board()
    stones = self.create_pieces()

    board.add_piece(stones[0], 1)
    p = board.get_piece(1)
    self.assertEqual(p, stones[0])

  def testGetPieces(self):
    board = Board()
    stones = self.create_pieces()

    board.add_piece(stones[0], 1)
    board.add_piece(stones[1], 2)
    board.add_piece(stones[2], 3)
    p = board.get_pieces([2, 3])
    self.assertEqual(len(p), 2)

    q = board.get_pieces([2, 4])
    self.assertEqual(q, [stones[1], None])

  def open_spots(self):
    board = Board()
    stones = self.create_pieces(22)
    for s in stones:
      board.add_piece(s)

    open_spots = board.open_spots()
    assertEqual(open_spots, [23,24])
