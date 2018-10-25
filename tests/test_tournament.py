import unittest

from stone_game.tournament import Tournament, TournamentPlayer
from stone_game.player import Player
from stone_game.ai_player import AIPlayer
from stone_game.piece import StoneColor


class TournamentTestCase(unittest.TestCase):

  def create_two_player_tournament(self):
    players = [
      Player('p1', '1'),
      Player('p2', '2')
    ]
    self.t = Tournament(players)

  def create_four_player_tournament(self):
    players = [
      Player('p1', '1'),
      Player('p2', '2'),
      Player('p3', '1'),
      Player('p4', '2')
    ]
    self.t = Tournament(players)

  def testGamesInRound(self):
    self.create_two_player_tournament()
    self.assertEqual(self.t.num_rounds, 1,
      'incorrect number of rounds for two players')
    self.assertEqual(self.t.num_games_in_round(0), 1,
      'incorrect number of games in round 1 for two players')

    self.create_four_player_tournament()
    self.assertEqual(self.t.num_rounds, 2,
      'incorrect number of rounds for four players')
    self.assertEqual(self.t.num_games_in_round(0), 2,
      'incorrect number of games in round 1')

  def testPlayersInRound(self):
    self.create_two_player_tournament()
    self.assertEqual(self.t.num_players_in_round(0), 2,
      'incorrect number of players in round 1')

    self.create_four_player_tournament()
    self.assertEqual(self.t.num_players_in_round(0), 4,
      'incorrect number of players in round 1')
    self.assertEqual(self.t.num_players_in_round(1), 2,
      'incorrect number of players in round 2')

class TournamentPlayerTestCase(unittest.TestCase):

  def testToGamePlayer(self):
    tp = TournamentPlayer(True, 'Alice')
    p = tp.to_game_player(StoneColor.BLACK)
    self.assertIsInstance(p, Player)

    tp = TournamentPlayer(False, 'Bob')
    p = tp.to_game_player(StoneColor.WHITE)
    self.assertIsInstance(p, AIPlayer)
