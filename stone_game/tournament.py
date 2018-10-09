import math
import random

import stone_game.terminalui as ui

class Tournament:
    def __init__(self, players):
        num_rounds = math.ceil(math.log2(len(players))) + 1

        random.shuffle(players)

        rounds = []

        for round_i in range(num_rounds):
            round_size = 2 ** (num_rounds - round_i - 1)

            round = [None for _ in range(round_size)]

            if round_i == 0:
                player_i = 0

                for side in range(2):
                    slot_i = side

                    while player_i < len(players) and slot_i < round_size:
                        round[slot_i] = players[player_i]

                        player_i = player_i + 1
                        slot_i = slot_i + 2

            rounds = rounds + [round]

        self.num_rounds = num_rounds
        self.round_winners = rounds
        self.current_round = 0
        self.current_match = 0
