import math
import random

from .game import Game
from .player import Player
from .ai_player import AIPlayer, Difficulty
from .piece import StoneColor
from .util import take_input_int, take_input_str
import stone_game.terminalui as ui

class Tournament:
  """
  A single-elimination tournament between any number of players.

  num_rounds:     number of rounds in the tournament
  rounds_players: keeps track of the players competing in each game
                  the structure of rounds_players is a 2d-array
                  the outer array contains rounds (n-th finals, ..., semi finals, finals, winner)
                  the inner arrays contains the players in a round from top to bottom
  current_round:  keeps track of the first round that has unplayed games in it
  current_game:   keeps track of the first game within the current round that is unplayed
  """

  def __init__(self, players):
    self.num_rounds = math.ceil(math.log2(len(players)))

    random.shuffle(players)

    rounds = []

    for round_i in range(self.num_rounds + 1):
      round_size = self.num_players_in_round(round_i)

      round = [None for _ in range(round_size)]

      if round_i == 0:
        player_i = 0

        for side in range(2):
          slot_i = side

          while player_i < len(players) and slot_i < round_size:
            round[slot_i] = players[player_i]

            player_i += 1
            slot_i += 2

      rounds += [round]

    self.rounds_players = rounds
    self.current_round = 0
    self.current_game = 0

  def num_games_in_round(self, round):
    """
    The number of games in the given round of the tournament.
    """
    return 2 ** (self.num_rounds - round - 1)

  def num_players_in_round(self, round):
    """
    The number of players in the given round of the tournament.
    """
    return 2 ** (self.num_rounds - round)

  def play_next_game(self):
    """
    Plays the next unplayed game in the tournament.
    """
    if self.current_round >= self.num_rounds:
      raise Exception("All rounds have already been played. ")

    player1 = self.rounds_players[self.current_round][self.current_game * 2]
    player2 = self.rounds_players[self.current_round][self.current_game * 2 + 1]

    winner = None

    if player1 == None:
      print('%s wins by walkover' % (player2.name,))
      winner = player2
    elif player2 == None:
      print('%s wins by walkover' % (player1.name,))
      winner = player1
    else:
      game = Game(
        player1.to_game_player(StoneColor.BLACK),
        player2.to_game_player(StoneColor.WHITE)
      )
      game_winner = game.begin()

      if game_winner == 0:
        print('Deciding winner by coin toss...')
        game_winner = random.randint(1, 2)

      if game_winner == 1:
        winner = player1
      elif game_winner == 2:
        winner = player2

      print('%s has won the game!' % (winner.name,))

    print()

    self.rounds_players[self.current_round + 1][self.current_game] = winner

    self.current_game += 1

    if self.current_game >= self.num_games_in_round(self.current_round):
      self.current_game = 0
      self.current_round += 1

  def is_finished(self):
    """
    Wether or not the tournament is completed.
    """
    return self.current_round >= self.num_rounds

  def winner(self):
    """
    The winning player of the tournament.
    Returns `None` if the tournament isn't completed.
    """
    return self.rounds_players[-1][0]

  def begin(self):
    """
    Plays the entire tournament, or the rest of the tournament
    if it has already been partially played.
    """
    self.draw()
    print()

    while not self.is_finished():
      self.play_next_game()
      self.draw()
      print()

    print('%s has won the tournament!' % (self.winner().name,))

  def draw(self):
    """
    Draws the tournament bracket to the console.
    """
    ui.clear()
    ui.draw_tournament(self)
    ui.output_buffer()

def tournament_from_console_input():
  """
  Creates a tournament using input from the console.
  Repeats asking for player types (human/ai),
  player names,
  and ai difficulty (if the type is ai).
  """
  players = []

  adding_players = True

  while adding_players:
    player_type = take_input_str(
      'Please select a type for player %d (human/ai): ' % (len(players) + 1), None,
      ['human', 'ai']
    ).lower()

    player_name = take_input_str('Please select a name: ', None, None)

    ai_difficulty = None
    if player_type == 'ai':
      ai_difficulty = take_input_str(
        'Please select an AI difficulty (easy/medium/hard): ', None,
        ['easy', 'medium', 'hard']
      )
      ai_difficulty = Difficulty[ai_difficulty.upper()]

    players.append(TournamentPlayer(
      player_type == 'human',
      player_name,
      ai_difficulty
    ))

    print()

    if len(players) >= 2:
      while True:
        if take_input_str('Add another player (y/n)? ', None, ['y', 'n']) == 'y':
          print()
          break
        else:
          adding_players = False
          break

  return Tournament(players)

class TournamentPlayer:
  """
  A competitor within a tournament.
  """

  def __init__(self, is_human, name, difficulty = None):
    """
    is_human:   true if this player is human, false if it's an AI
    name:       the players name
    difficulty: the difficulty of this player (only if it's an AI)
    """
    self.is_human = is_human
    self.name = name
    self.difficulty = difficulty
  
  def to_game_player(self, color):
    """
    Creates a Player or AIPlayer with the same name as this TournamentPlayer.
    """
    if self.is_human:
      return Player(self.name, color)
    else:
      return AIPlayer(self.name, color, self.difficulty)

  def __str__(self):
    return self.name

  def __repr__(self):
    return 'TournamentPlayer(is_human = %s, name = %s)' % (repr(self.is_human), repr(self.name))
