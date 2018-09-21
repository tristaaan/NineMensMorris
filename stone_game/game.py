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
    while self.place_phase_conditional():
      print('---- Turn %d ----' % self.mechanics.turn_counter)
      active_player = self.mechanics.active_player()
      current_piece = active_player.inactive_piece()
      print('%s\'s turn' % active_player)
      spot = self.take_input('Place piece: ',          \
                             'You cannot place there', \
                             self.board.open_spots())
      # Place piece, steal if a mill was formed
      if self.mechanics.place_piece(self.board, current_piece,spot):
        print('A mill was created!')
        pieces_to_steal = self.mechanics.stealable_pieces(self.board)
        print("Remove one of the following pieces:", pieces_to_steal)
        piece_to_remove = self.take_input(           \
          'Which piece would you like to remove?: ', \
          'You cannot remove that piece',            \
          pieces_to_steal)
        self.mechanics.steal_piece(piece_to_remove, self.board)

    # MOVE PHASE
    print('move phase')
    while self.move_phase_conditional():
      active_player = self.mechanics.active_player()
      possible_pieces = self.mechanics.movable_pieces(self.board, active_player)
      possible_positions = [p.position for p in possible_pieces]

      print('---- Turn %d ----' % self.mechanics.turn_counter)
      print('Available moves: ', possible_positions)
      print('%s\'s turn' % active_player)

      at = self.take_input('Move piece at: ', 'You cannot move that piece',
                           possible_positions)
      possible_moves = self.mechanics.moves_for_piece(self.board, at)
      print('Possible moves: ', possible_moves)
      to = self.take_input('Move piece to: ', 'You cannot move there',
                           possible_moves)
      # Move piece, steal if a mill was formed
      if self.mechanics.move_piece(self.board, at, to):
        print('A mill was created!')
        pieces_to_steal = self.mechanics.stealable_pieces(self.board)
        print("Remove one of the following pieces:", pieces_to_steal)
        piece_to_remove = self.take_input(
          'Which piece would you like to remove?: ', \
          'You cannot remove that piece',            \
          pieces_to_steal)
        self.mechanics.steal_piece(piece_to_remove, self.board)

    print('----- GAME OVER -----')
    print('\n%s is victorious!\n' % self.mechanics.inactive_player().name)

  def place_phase_conditional(self):
    """
    True until the players have placed all their pieces
    """
    return len(self.player1.remaining_unplaced()) + \
           len(self.player2.remaining_unplaced()) > 0

  def move_phase_conditional(self):
    """
    True until a player has 2 pieces left, or
    """
    current_player = self.mechanics.active_player()
    current_movables = self.mechanics.movable_pieces(self.board, current_player)
    return len(current_player.remaining_in_play()) > 2 and \
           len(current_movables) > 0

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