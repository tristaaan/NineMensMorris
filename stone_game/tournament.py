import math
import random

class Tournament:
    def __init__(self, players):
        self.num_rounds = math.ceil(math.log2(len(players))) + 1

        random.shuffle(players)

        rounds = []

        for round_i in range(self.num_rounds):
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
        self.current_match = 0

    def num_players_in_round(self, round):
        return 2 ** (self.num_rounds - round - 1)

    def play_next_match(self):
        if self.current_match >= self.num_rounds:
            raise Exception("All rounds have already been played. ")

        player1 = self.rounds_players[self.current_round][self.current_match * 2]
        player2 = self.rounds_players[self.current_round][self.current_match * 2 + 1]

        # TODO play match between player1 & player2
        # TODO insert winning player into self.rounds_player[self.current_round + 1][self.current_match // 2]

        self.current_round += 1

        if self.current_match * 2 > self.num_players_in_round(self.current_round):
            self.current_match = 0
            self.current_round += 1
