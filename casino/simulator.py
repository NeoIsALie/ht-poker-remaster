from itertools import combinations
from textwrap import wrap
from typing import List
import itertools as it

from casino.table import Table
from evaluator.evaluator import Evaluator


class Simulator:
    def __init__(self, players_num: int = 3, simulations_num: int = 10):
        """

        :param players_num: number of players
        :param simulations_num: number of simulations
        """
        self._simulations_num = simulations_num
        self.table = Table(players_num=players_num)
        self.evaluator = Evaluator()

    def simulate(self, deck_type: str = "full"):
        """
        Simulates a number of poker games
        :param deck_type: number of cards in deck (52 for full, 36 for short)
        :return:
        """
        self.table.generate_deck(deck_type)
        self.table.set_stage_deck(self.table.hands)
        self.table.set_stage_deck(self.table.start_community_hand)
        comb_num = 5-len(self.table.start_community_hand)//2
        hands_cache = list(map(lambda x: tuple(wrap(x, 2)), self.table.hands))
        for deck in it.combinations(self.table._deck, comb_num):
            self.table._deck = list(deck)+["!"]
            self.table._community_hand = self.table.start_community_hand
            rounds = self.table.set_stage_iterator(self.table.start_game_stage)
            for round_num in range(rounds):
                self.table.new_round()
            print(f"Community hand: {self.table.community_hand}")
            hands = self.play(self.table.community_hand, hands_cache)
            for player in self.table.players:
                if player.hand == hands[0]:
                    player.wins_game()
                    print(f"Player {player.number} wins")
        self._simulations_num = all_combinations_num

    def evaluate_one_player(self, board: tuple, hand: str):
        # print(board)
        all_4_combinations = [hand[2:], hand[:2] + hand[4:], hand[:4] + hand[6:], hand[:6] + hand[8:], hand[:8]]
        for i in range(len(all_4_combinations)):
            all_4_combinations[i] = tuple(wrap(all_4_combinations[i], 2))
        all_4_combinations.sort(key=lambda x: self.evaluator.evaluate_cards(*board, *x))
        ranks = list(map(lambda x: self.evaluator.evaluate_cards(*board, *x), all_4_combinations))
        print(all_4_combinations)
        print(ranks)
        return all_4_combinations[0], ranks[0]

    def play(self, community_hand: str, players_hands):
        """
        Simulates one poker game
        :param community_hand: cards on table
        :param players_hands: cards in players' pockets
        :return: all players' hands with appropriate ranks (the less the rank the better hand is)
        """
        print(community_hand)
        board = tuple(wrap(community_hand, 2))
        hands = players_hands
        hands.sort(key=lambda x: self.evaluator.evaluate_cards(*board, *x))
        hands = [''.join(hand) for hand in hands]
        return hands
      
    def show_status(self) -> None:
        """
        Show win probability from all simulations
        :return:
        """
        total = sum(player.wins for player in self.table.players)
        for player in self.table.players:
            print("Player {} with {:.2f} percent win probability".format(player.number, player.wins / total * 100))
