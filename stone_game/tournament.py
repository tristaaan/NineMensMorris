import math
import random

from .player import Player
import stone_game.terminalui as ui

class Tournament:
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
    return 2 ** (self.num_rounds - round - 1)

  def num_players_in_round(self, round):
    return 2 ** (self.num_rounds - round)

  def play_next_game(self):
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
      # TODO play match between player1 & player2
      if input('winner (1/2): ') == '1':
        winner = player1
      else:
        winner = player2

    print()

    self.rounds_players[self.current_round + 1][self.current_game] = winner

    self.current_game += 1

    if self.current_game >= self.num_games_in_round(self.current_round):
      self.current_game = 0
      self.current_round += 1

  def is_finished(self):
    return self.current_round >= self.num_rounds

  def winner(self):
    return self.rounds_players[-1][0]

  def begin(self):
    self.draw()
    print()

    while not self.is_finished():
      self.play_next_game()
      self.draw()
      print()

    print('Winner: %s' % (self.winner().name,))

  def draw(self):
    ui.clear()
    ui.draw_tournament(self)
    ui.output_buffer()

def tournament_from_console_input():
  players = []

  adding_players = True

  while adding_players:
    player_type = input('Please select a type for player %d (human/ai): ' % (len(players) + 1,)).strip().lower()

    if player_type == 'human' or player_type == 'ai':
      player_name = ''
      while player_name == '':
        player_name = input('Please select a name: ').strip()
      print()

      players.append(TournamentPlayer(player_type == 'human', player_name))
    else:
      continue

    if len(players) >= 2:
      while True:
        yn = input('Add another player? (y/n) ').strip().lower()
        if yn == 'y':
          print()
          break
        elif yn == 'n':
          adding_players = False
          break

  return Tournament(players)

class TournamentPlayer:
  def __init__(self, is_human, name):
    self.is_human = is_human
    self.name = name

  def __str__(self):
    return self.name

  def __repr__(self):
    return 'TournamentPlayer(is_human = %s, name = %s)' % (repr(self.is_human), repr(self.name))
