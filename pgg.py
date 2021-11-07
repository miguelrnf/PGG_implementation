import math
import numpy as np


class player(object):
    def __init__(self, strategy=None):
        if strategy is None:
            self.__strategy = np.random.randint(0, 3)
        else:
            self.__strategy = strategy
        self.__payoff = 0.

    @property
    def strategy(self):
        return self.__strategy

    @strategy.setter
    def strategy(self, value):
        assert value in [0, 1, 2]
        self.__strategy = value

    @property
    def payoff(self):
        return self.__payoff

    @payoff.setter
    def payoff(self, value):
        self.__payoff = value


class generalModel(object):
    def __init__(self):
        self.M = None
        self.c = None
        self._players = None

    @property
    def players(self):
        return self._players

    def _assignPayoff(self, player_instance, ncooperators, ndefectors):

        assert isinstance(player_instance, player)

        total_cost = ncooperators * self.c
        pull_amount = total_cost/(ncooperators + ndefectors)

        # assign payoff depending on the strategy played by the player
        if player_instance.strategy == 0:
            player_instance.payoff += -self.c + pull_amount

        elif player_instance.strategy == 1:
            player_instance.payoff += pull_amount

    def _revisionProtocol(self, payoff1, payoff2):
        if payoff1 >= payoff2:
            return 0
        else:
            return (payoff2 - payoff1) / self.M


class bucketModel(generalModel):
    def __init__(self, nplayers, coop, defec, r, c):
        super().__init__()
        self.c = c
        self.r = r
        self.nplayers = nplayers
        self.__initBucket(coop, defec)

    def __initBucket(self, coop, defec):
        assert (coop + defec) == 1.

        pc = coop
        pd = defec

        strategies = np.random.choice([0, 1], size=self.nplayers, replace=True, p=[pc, pd])

        self._players = [player(strategies[i]) for i in range(self.nplayers)]

    def playGame(self, nparticipants):
        random_player_indexes = np.random.choice(self.nplayers, nparticipants, replace=False)

        nc = 0
        nd = 0

        for i in random_player_indexes:
            if self.players[i].strategy == 0:
                nc += 1
            elif self.players[i].strategy == 1:
                nd += 1

        for i in random_player_indexes:
            self._assignPayoff(self.players[i], nc, nd)

    def reviseStrategy(self, player_index):
        random_player_index = np.random.choice(self.nplayers)

        payoff1 = self.players[player_index].payoff
        payoff2 = self.players[random_player_index].payoff

        self.updateM()
        p = self._revisionProtocol(payoff1, payoff2)

        change = np.random.choice([False, True], p=[1 - p, p])

        if change:
            self.players[player_index].strategy = self.players[random_player_index].strategy

    def clearPayoffs(self):
        for i in range(self.nplayers):
            self.players[i].payoff = 0

    def countStrategies(self, rep):
        nc = 0
        nd = 0

        for i in range(self.nplayers):
            if self.players[i].strategy == 0:
                nc += 1
            elif self.players[i].strategy == 1:
                nd += 1

        return nc, nd, 0, 0, 0, 0

    def updateM(self):
        max_payoff = 0
        min_payoff = math.inf
        for i in range(self.nplayers):
            p = self._players[i].payoff
            if p > max_payoff:
                max_payoff = p
            if p < min_payoff:
                min_payoff = p

        self.M = max_payoff - min_payoff
