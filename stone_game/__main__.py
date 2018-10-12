from .game import Game
from .player import Player
from .ai_player import AIPlayer
from .piece import StoneColor

if __name__ == '__main__':
  p1 = AIPlayer('Player1', StoneColor.BLACK)
  p2 = AIPlayer('Player2', StoneColor.WHITE)
  g = Game(p1, p2)
  g.begin()
