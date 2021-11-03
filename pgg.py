#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 12:42:12 2019

@author: paul
"""
import math
import numpy as np


class player(object):
    def __init__(self, strategy=None):
        """
        The player class holds all variables that belong to one person.
        Namely the current strategy and the last payoff.

        :type strategy: int
        :param strategy: The strategies are encoded by integers.
        Where 0 represents a cooperator, 1 a defector and 2 a loner

        """

        if strategy == None:
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
    """
    This is the base class for different public goods game model. It holds methods and properties
    that are shared thoughout the different models
    """

    @property
    def players(self):
        return self._players

    def _assignPayoff(self, player_instance, ncooperators, ndefectors, ntroubles):
        """
        assign a payoff o one player of a public goods game

        :param player_instance: a instance of the player class
        :ncooperators: number of cooperators in the public goods game
        :nparticipants: number of participants in the public goods game
        """

        assert isinstance(player_instance, player)

        spite_factor = 0.3
        total_cost = (ncooperators) * self.c
        pull_amount = total_cost/(ncooperators + ndefectors)

        # assign payoff depending on the strategy played by the player
        if player_instance.strategy == 0:
            player_instance.payoff += -self.c + pull_amount

        elif player_instance.strategy == 1:
            player_instance.payoff += pull_amount

        elif player_instance.strategy == 2:
            player_instance.payoff += - self.c * spite_factor + pull_amount + self.c

    def _revisionProtocol(self, payoff1, payoff2):
        if payoff1 >= payoff2:
            return 0

        return (payoff2 - payoff1) / self.M


class bucketModel(generalModel):
    def __init__(self, nplayers, coop, defec, trouble):
        """
        The bucket model class holds the variables that define a public goods game in
        a mean field and the methods to play the public goods game

        :param nplayers: number of total players
        """
        self.nplayers = nplayers
        self.__initBucket(coop, defec, trouble)

    def __initBucket(self, coop, defec, trouble):
        """
        initialize strategies with a equal propability for each strategy when inital_distribution is None.
        Or using the initial distribution.
        """

        assert (coop + defec + trouble) == 1.

        pc = coop
        pd = defec
        pt = trouble

        strategies = np.random.choice([0, 1, 2], size=self.nplayers, replace=True, p=[pc, pd, pt])

        self._players = [player(strategies[i]) for i in range(self.nplayers)]

    def playGame(self, nparticipants, c, r):
        """
        play one time the public goods game

        :param nparticipants: The number of players that are chosen randomely from all players and
        given the opportunity to particpate in the public
        goods game (note:loners do not play the public goods game!).

        :param cost: The cost of playing the public goods game for the cooperator

        :param r: The facor with which the pot of costs is multiplied

        :param sigma: The payoff for the loner

        """
        # check if r and sigma are chosen correctly
        #assert (1 < r and r < nparticipants)

        # set game properties
        self.c = c
        self.r = r

        # choose randomely players
        random_player_indexes = np.random.choice(self.nplayers, nparticipants, replace=False)

        # count the cooperators and defectors
        nc = 0
        nd = 0

        for i in random_player_indexes:
            if self.players[i].strategy == 0:
                nc += 1
            elif self.players[i].strategy == 1:
                nd += 1
        nt = nparticipants - nc - nd

        # assign payoffs
        for i in random_player_indexes:
            self._assignPayoff(self.players[i], nc, nd, nt)

    def reviseStrategy(self, player_index):
        """
        revision protocol for player1 to change his strategy to the strategy of player2

        :param player1,player2: instance of class player
        """
        # choose a randomely players
        random_player_index = np.random.choice(self.nplayers)

        payoff1 = self.players[player_index].payoff
        payoff2 = self.players[random_player_index].payoff

        p = self._revisionProtocol(payoff1, payoff2)

        change = np.random.choice([False, True], p=[1 - p, p])

        if change:
            self.players[player_index].strategy = self.players[random_player_index].strategy

    def clearPayoffs(self):
        for i in range(self.nplayers):
            self.players[i].payoff = 0

    def countStrategies(self):
        nc = 0
        nd = 0

        for i in range(self.nplayers):
            if self.players[i].strategy == 0:
                nc += 1
            elif self.players[i].strategy == 1:
                nd += 1
        nt = self.nplayers - nc - nd

        return nc, nd, nt

    def updateM(self):
        max = 0
        min = math.inf
        for i in range(self.nplayers):
            p = self._players[i].payoff
            if p > max:
                max = p
            if p < min:
                min = p

        self.M = max - min
