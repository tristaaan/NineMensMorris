from .game import Game
from .player import Player
from .ai_player import AIPlayer
from .piece import StoneColor
from .ai import Difficulty
from .util import take_input_int, take_input_str
from .tournament import tournament_from_console_input

def run_game(player1, player2):
  g = Game(player1, player2)
  winner = g.begin()
  if winner == 0:
    print('It\'s a tie!')
  elif winner == 1:
    print('\n%s is victorious!\n' % player1.name)
  else:
    print('\n%s is victorious!\n' % player2.name)

if __name__ == '__main__':
  print('1) player vs player')
  print('2) player vs ai')
  print('3) ai vs ai')
  print('4) tournament')
  print()

  mode = take_input_int(
    'Select a mode: ',
    'Please select a mode between 1 and 4. ',
    list(range(1, 4 + 1)))

  print()

  if mode == 1:
    run_game(
      player1 = Player('Player 1', StoneColor.BLACK),
      player2 = Player('Player 2', StoneColor.WHITE)
    )
  elif mode == 2:
    ai_difficulty = take_input_str(
      'Please select an AI difficulty (easy/medium/hard): ', None,
      ['easy', 'medium', 'hard']
    )
    ai_difficulty = Difficulty[ai_difficulty.upper()]

    run_game(
      player1 = Player('Player', StoneColor.BLACK),
      player2 = AIPlayer('AI', StoneColor.WHITE, ai_difficulty)
    )
  elif mode == 3:
    ai_difficulty_1 = take_input_str(
      'Please select a difficulty for the first AI (easy/medium/hard): ', None,
      ['easy', 'medium', 'hard']
    )
    ai_difficulty_2 = take_input_str(
      'Please select a difficulty for the second AI (easy/medium/hard): ', None,
      ['easy', 'medium', 'hard']
    )

    ai_difficulty_1 = Difficulty[ai_difficulty_1.upper()]
    ai_difficulty_2 = Difficulty[ai_difficulty_2.upper()]

    run_game(
      player1 = AIPlayer('AI 1', StoneColor.BLACK, ai_difficulty_1),
      player2 = AIPlayer('AI 2', StoneColor.WHITE, ai_difficulty_2)
    )
  elif mode == 4:
    tournament = tournament_from_console_input()
    tournament.begin()
