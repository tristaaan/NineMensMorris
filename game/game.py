from board import Board
from mechanics import Mechanics
from player import Player


class Game(object):

  def __init__(self):
    self.player1 = Player('Player1', '◎')
    self.player2 = Player('Player2', '◉')

    self.board = Board()
    self.mechanics = Mechanics(self.player1, self.player2)

  def begin(self):
    # PLACE PHASE
    active_player = self.mechanics.active_player()
    while len(self.board.open_spots()) > 6:
      print('---- Turn %d ----' % self.mechanics.turn_counter)
      active_player = self.mechanics.active_player()
      current_piece = active_player.inactive_piece()
      print('%s\'s turn' % active_player)
      spot = int(input('Place piece:'))
      self.mechanics.place_piece(self.board, current_piece, spot)

    # MOVE PHASE
    print('move phase')
    while len(self.player1.remaining()) > 2 and len(self.player2.remaining()) > 2 and \
      len(self.mechanics.available_moves(self.board, active_player)) != 0:
      active_player = self.mechanics.active_player()
      print('---- Turn %d ----' % self.mechanics.turn_counter)
      possible_moves = self.mechanics.available_moves(self.board, active_player)
      print('Available moves: ', possible_moves)
      print('%s\'s turn' % active_player)
      current_piece
      at = int(input('Move piece at:'))
      to = int(input('           to:'))
      try:
        if to not in possible_moves:
          raise ValueError('You cannot move that piece at %d' % at)
        self.mechanics.move_piece(self.board, at, to)
      except ValueError as e:
        print(e)
        continue


if __name__ == '__main__':
  g = Game()
  g.begin()
