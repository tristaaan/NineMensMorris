from piece import Piece


class Node(object):
  piece = None
  def __init__(self, edges):
    self.edges = edges


class Board(object):

  def __init__(self):
    self.nodes = {}
    for i in range(1,25):
      # edges
      if i % 2 == 0:
        # outer
        if i <= 8:
          self.add_node(i, [i-1, (i + 1) % 8, i+8])
        # middle
        elif i > 8 and i <= 16:
          self.add_node(i, [i-1, max((i+1) % 16, 9), i+8, i-8])
        # inner
        else:
          self.add_node(i, [i-1, max((i+1) % 24, 17), i-8])
    self.add_node(1, [2,8])
    self.add_node(3, [2,4])
    self.add_node(5, [4,6])
    self.add_node(7, [6,8])

    self.add_node(9, [10,16])
    self.add_node(11, [10,12])
    self.add_node(13, [12,14])
    self.add_node(15, [14,16])

    self.add_node(17, [18,24])
    self.add_node(19, [18,20])
    self.add_node(21, [20,22])
    self.add_node(23, [22,24])

  def add_piece(self, piece, to):
    if self.nodes[to].piece != None:
      raise ValueError('A piece is already on %d' % to)
    piece.position = to
    self.nodes[to].piece = piece
    self.nodes[to].piece.set_active(to)

  def remove_piece(self, at):
    if self.nodes[at].piece == None:
      raise ValueError('There is no piece on %d' % at)
    piece = self.nodes[at].piece
    self.nodes[at].piece = None
    return piece

  def get_piece(self, at):
    return self.nodes[at].piece

  def get_pieces(self, at=[], belonging_to=''):
    ret = []
    if len(belonging_to) > 0:
      for i in range(1,25):
        if self.nodes[i].piece != None and \
          self.nodes[i].piece.owner == belonging_to:
          ret.append(self.nodes[i].piece)
      return ret

    for pos in at:
      ret.append(self.nodes[pos].piece)
    return ret

  def open_spots(self):
    ret = []
    for i in range(1,25):
      if self.nodes[i].piece == None:
        ret.append(i)
    return ret

  def add_node(self, name, edges):
    self.nodes[name] = Node(edges)

  def draw(self):
    print('%s---------%s---------%s' % (self.piece_str(1), self.piece_str(2), self.piece_str(3)))
    print('|         |         |')
    print('|  %s------%s------%s  |' % (self.piece_str(9), self.piece_str(10), self.piece_str(11)))
    print('|  |      |      |  |')
    print('|  |  %s---%s---%s  |  |' % (self.piece_str(17), self.piece_str(18), self.piece_str(19)))
    print('|  |  |       |  |  |')
    print('%s--%s--%s       %s--%s--%s' % (self.piece_str(8),  self.piece_str(16), self.piece_str(24),
                                           self.piece_str(20), self.piece_str(12), self.piece_str(4)))
    print('|  |  |       |  |  |')
    print('|  |  %s---%s---%s  |  |' % (self.piece_str(23), self.piece_str(22), self.piece_str(21)))
    print('|  |      |      |  |')
    print('|  %s------%s------%s  |' % (self.piece_str(15), self.piece_str(14), self.piece_str(13)))
    print('|         |         |')
    print('%s---------%s---------%s' % (self.piece_str(7), self.piece_str(6), self.piece_str(5)))

  def piece_str(self, at):
    if self.nodes[at].piece == None:
      return '☐'
    return self.nodes[at].piece.icon
