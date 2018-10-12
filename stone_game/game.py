from .board import Board
from .rules import Rules
from .player import Player


class Game(object):

  # 18 moves for placing, and 50 after.
  draw_threshold = 68

  def __init__(self, player1, player2):
    self.player1 = player1
    self.player2 = player2

    self.board = Board()
    self.rules = Rules(self.player1, self.player2)

  def begin(self):
    # PLACE PHASE
    self.board.draw()

    self.place_phase()
    self.move_phase()

    if self.rules.turn_counter >= self.draw_threshold:
      return 0

    print('----- GAME OVER -----')
    print('\n%s is victorious!\n' % self.rules.inactive_player().name)
    return (self.rules.turn_counter % 2) + 1

  def place_phase(self):
    active_player = self.rules.active_player()
    while self.place_phase_conditional():
      print('---- Turn %d ----' % self.rules.turn_counter)
      possible_placements = self.board.open_spots()
      active_player = self.rules.active_player()
      (current_piece, spot) = active_player.make_placement(
        possible_placements, board=self.board)
      # Place piece, steal if a mill was formed
      millFormed = self.rules.place_piece(self.board, current_piece, spot)
      self.board.draw()
      if millFormed:
        print('A mill was created!')
        pieces_to_steal = self.rules.stealable_pieces(self.board)
        print("Remove one of the following pieces:", pieces_to_steal)
        piece_to_remove = active_player.make_steal_move(pieces_to_steal,
          board=self.board, opponent=self.rules.inactive_player())
        self.rules.steal_piece(piece_to_remove, self.board)
        self.board.draw()

  def move_phase(self):
    while self.move_phase_conditional():
      active_player = self.rules.active_player()
      possible_pieces = self.rules.movable_pieces(self.board, active_player)
      possible_positions = [p.position for p in possible_pieces]

      print('---- Turn %d ----' % self.rules.turn_counter)
      print('Available moves: ', possible_positions)
      print('%s\'s turn' % active_player)

      move_map = {}
      for s in possible_positions:
        move_map[s] = self.rules.moves_for_piece(self.board, s)

      (at,to) = active_player.make_move(possible_positions, move_map, board=self.board)

      # Move piece, steal if a mill was formed
      millFormed = self.rules.move_piece(self.board, at, to)
      self.board.draw();
      if millFormed:
        print('A mill was created!')
        pieces_to_steal = self.rules.stealable_pieces(self.board)
        print("Remove one of the following pieces:", pieces_to_steal)
        piece_to_remove = active_player.make_steal_move(pieces_to_steal,
          board=self.board, opponent=self.rules.inactive_player())
        self.rules.steal_piece(piece_to_remove, self.board)
        self.board.draw()

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
    current_player = self.rules.active_player()
    current_movables = self.rules.movable_pieces(self.board, current_player)
    return len(current_player.remaining_in_play()) > 2 and \
           len(current_movables) > 0 and \
           self.rules.turn_counter <= self.draw_threshold
