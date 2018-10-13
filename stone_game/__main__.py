from .game import Game
from .player import Player
from .ai_player import AIPlayer
from .piece import StoneColor
from .ai import Difficulty

from .tournament import tournament_from_console_input

if __name__ == '__main__':
  print('1) player vs player')
  print('2) player vs ai')
  print('3) ai vs ai')
  print('4) tournament')
  print()

  while True:
    mode = input('Select a mode: ')

    print()

    if mode == '1':
      g = Game()
      g.begin()
    elif mode == '2':
      # TODO
      print('Uninplemented')
      pass
    elif mode == '3':
      # TODO
      print('Uninplemented')
      pass
    elif mode == '4':
      tournament = tournament_from_console_input()
      tournament.begin()
    else:
      print('Please select a mode between 1 and 4. ')
      continue

    break
