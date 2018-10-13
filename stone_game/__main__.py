from .game import Game
from .player import Player
from .ai_player import AIPlayer
from .piece import StoneColor
from .ai import Difficulty

if __name__ == '__main__':
  results = []
  for i in range(50):
    p1 = AIPlayer('Player1', StoneColor.BLACK)
    p2 = AIPlayer('Player2', StoneColor.WHITE)
    g = Game(p1, p2)
    results.append(g.begin())

  print('Draws:  %d ' % results.count(0))
  print('p1 win: %d ' % results.count(1))
  print('p2 win: %d ' % results.count(2))
