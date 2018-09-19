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
      self.mechanics.place_piece(self.board, current_piece,spot)

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
      self.mechanics.move_piece(self.board, at, to)


  def take_input(self, text, error, valid_ints):
    while(1):
      try:
        inp = int(input(text))
        if inp in valid_ints:
          return inp
        raise ValueError(error)
        break
      except ValueError as error:
        print(error)
        continue
      except:
        print('Thats not a number')
        continue
