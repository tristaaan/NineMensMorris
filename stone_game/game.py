from .board import Board
from .mechanics import Mechanics
from .player import Player


class Game(object):

  def __init__(self):
    self.player1 = Player('Player1', '◎')
    self.player2 = Player('Player2', '◉')

    self.board = Board()
    self.mechanics = Mechanics(self.player1, self.player2, drawing=True)

  def begin(self):
    # PLACE PHASE
    active_player = self.mechanics.active_player()
    while len(self.board.open_spots()) > 6:
      print('---- Turn %d ----' % self.mechanics.turn_counter)
      active_player = self.mechanics.active_player()
      current_piece = active_player.inactive_piece()
      print('%s\'s turn' % active_player)
      spot = self.take_input('Place piece: ','You cannot place there', self.board.open_spots())
      if (self.mechanics.place_piece(self.board, current_piece,spot)):
        print('%s made a mill!' % active_player)
        self.steal_piece()
        if self.mechanics.drawing:
          self.board.draw()
      self.mechanics.turn_counter += 1

    # MOVE PHASE
    print('move phase')
    while len(self.player1.remaining()) > 2 and len(self.player2.remaining()) > 2 and \
      len(self.mechanics.available_moves(self.board, active_player)) != 0:
      active_player = self.mechanics.active_player()
      print('---- Turn %d ----' % self.mechanics.turn_counter)
      possible_moves = self.mechanics.available_at(self.board, active_player)
      print('Available moves: ', possible_moves)
      print('%s\'s turn' % active_player)

      at = self.take_input('Move piece at: ', 'You cannot move that piece', possible_moves)
      to = self.take_input('Move piece to: ', 'You cannot move there', self.mechanics.available_to(self.board, at))
      if (self.mechanics.move_piece(self.board, at, to)):
        print('%s made a mill!' % active_player)
        self.steal_piece()
        if self.mechanics.drawing:
          self.board.draw()
      self.mechanics.turn_counter += 1


  def steal_piece(self):
    """
    Removes a piece from the enemy player
    """
    enemy_pieces = self.mechanics.inactive_player().remaining()
    print(enemy_pieces)
    pieces_not_in_mill = set()
    for a in enemy_pieces:
      if not self.mechanics.mill_check(self.board, a, self.mechanics.inactive_player()):
        pieces_not_in_mill = pieces_not_in_mill | {a}
    #pieces_not_in_mill = {a for a in enemy_pieces if not self.mechanics.mill_check(self.board, a, self.mechanics.inactive_player())}
    print(pieces_not_in_mill)
    if not len(pieces_not_in_mill) == 0:
      positions = {p.position for p in pieces_not_in_mill}
      print ("Remove one of the following pieces:", positions)
      piece_to_remove = self.take_input('Which piece would you like to remove?: ', 'You cannot remove that piece', positions)
      piece = self.board.get_piece(piece_to_remove)
      piece.remove_from_play()
      self.board.remove_piece(piece_to_remove)
      return

    pieces_in_mill = {a for a in enemy_pieces if self.mechanics.mill_check(self.board, a, self.mechanics.inactive_player())}
    positions2 = {p.position for p in pieces_in_mill}
    print("Remove one of the following pieces:", positions2)
    piece_to_remove2 = self.take_input('Which piece would you like to remove?: ', 'You cannot remove that piece',
                                      positions2)
    piece = self.board.get_piece(piece_to_remove2)
    piece.remove_from_play()
    self.board.remove_piece(piece_to_remove2)
    return


  def take_input(self, text, error, valid_ints):
    try:
      inp = int(input(text))
      if inp in valid_ints:
        return inp
      raise NameError(error)
    except NameError:
      print(error)
    except ValueError:
      print('Thats not a number')

    return self.take_input(text, error, valid_ints)