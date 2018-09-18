from .piece import Piece


class Node(object):
  """
  A simple node object for the board
  piece: Piece
  edges: array of numbers
  """
  piece = None
  def __init__(self, edges):
    self.edges = edges


class Board(object):
  """
  A board for the game
  node: a graph of Node objects
  """
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

    self.add_node(17, [18, 24])
    self.add_node(19, [18,20])
    self.add_node(21, [20,22])
    self.add_node(23, [22,24])

  def add_piece(self, piece, to):
    """
    Adds a piece to the board
    piece: Piece
    to: the name of the node in self.nodes to add piece to
    """
    if self.nodes[to].piece != None:
      raise ValueError('A piece is already on %d' % to)
    piece.position = to
    self.nodes[to].piece = piece
    self.nodes[to].piece.set_active(to)

  def remove_piece(self, at):
    """
    Removes a piece from the board
    at: name of the node in self.nodes to remove the piece from
    """
    if self.nodes[at].piece == None:
      raise ValueError('There is no piece on %d' % at)
    piece = self.nodes[at].piece
    piece.position = 0
    self.nodes[at].piece = None
    return piece

  def get_piece(self, at):
    """
    Get piece from a specific spot on the board
    at: name of the node to fetch the piece from
    """
    return self.nodes[at].piece

  def get_pieces(self, at):
    """
    Query multiple pieces from the board
    at: array of names referencing nodes on the board
    """
    ret = []
    for pos in at:
      ret.append(self.nodes[pos].piece)
    return ret

  def open_spots(self):
    """
    Fetch available nodes to add pieces to
    """
    ret = []
    for i in range(1,25):
      if self.nodes[i].piece == None:
        ret.append(i)
    return ret

  def add_node(self, name, edges):
    """
    Add node to board, ideally this should be in a graph class
    name: name of node, this will be its key
    edges: array of names
    """
    self.nodes[name] = Node(edges)

  def draw(self):
    """
    Print out the board
    """
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
    """
    Print the icon of just a single piece at a node
    at: the name of the node
    """
    if self.nodes[at].piece == None:
      return '☐'
    return self.nodes[at].piece.icon
