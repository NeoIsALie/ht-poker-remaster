from textwrap import wrap
import itertools as it
from multiprocessing import Pool
from ctypes import cdll

from casino.table import Table
from evaluator.evaluator import Evaluator


fast_evaluator = cdll.LoadLibrary('./fastc/evaluator.so')



class Simulator:

    def __init__(self, players_num = 4, procces_num = 4):
        self.players_num = players_num
        self.procces_num = procces_num
        self.table = Table(players_num=players_num)
        self.evaluator = Evaluator()
        self.players_wins = [0] * players_num
        self.cache = None


    def convert_card(self, cards):
        return set(self.evaluator.rank_map[card[0]]*4+self.evaluator.suit_map[card[1]] for card in cards)


    def simulate(self, deck_type: str = "full"):
        self.table.generate_deck(deck_type)
        self.table.set_stage_deck(self.table.hands)
        self.table.set_stage_deck(self.table.start_community_hand)

        deck = {*range(51)}
        players_hands = tuple(map(lambda x: self.convert_card(wrap(x, 2)), self.table.hands))
        community_hand = self.convert_card(wrap(self.table.start_community_hand, 2))
        for player_hand in players_hands: deck -= player_hand
        deck -= community_hand

        comb_num = 5-len(self.table.start_community_hand)//2
        all_decks = tuple(it.combinations(deck, comb_num))

        n = self.procces_num
        part = len(all_decks)//n

        self.cache = (players_hands, community_hand)
        args = [all_decks[i*part:(i+1)*part] for i in range(n)]
        with Pool(n) as p:
            res = p.map(self.play_multiply, args)

        self.players_wins = [sum(res[i][j] for i in range(self.procces_num)) for j in range(self.players_num)]


    def play_multiply(self, deck_cards_set):
        players_hands, community_hand = self.cache
        players_wins = [0] * len(players_hands)
        for deck_cards in deck_cards_set:
            result = tuple(fast_evaluator.evaluate_cards(*community_hand, *deck_cards, *player_hand) for player_hand in players_hands)
            winner_score = min(result)
            for i in range(len(result)):
                if result[i] == winner_score:
                    players_wins[i] += 1
        return players_wins


    def show_status(self):
        total = sum(self.players_wins)
        for player, player_wins in zip(self.table.players, self.players_wins):
            print("Player {} with {:.2f} percent win probability".format(player.number, player_wins / total * 100))
