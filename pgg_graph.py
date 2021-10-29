# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 12:42:12 2019

@author: paul
"""
import random

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class generalModel(object):
    """
    This is the base class for different public goods game model. It holds methods and properties
    that are shared thoughout the different models
    """

    def _assignPayoff(self, nodeIndex, ncooperators, ndefectors, ntroubles):
        """
        assign a payoff o one player of a public goods game

        :param player_instance: a instance of the player class
        :ncooperators: number of cooperators in the public goods game
        :nparticipants: number of participants in the public goods game
        """


        spite_factor = 0.3
        rep_factor_c = 1
        rep_factor_d = -0.5
        rep_factor_s = -1

        # assign payoff depending on the strategy played by the player
        if self._players.nodes[nodeIndex]["Strategy"] == 0:
            self._players.nodes[nodeIndex]["Last Payoff"] += - self.c + self.r * (self.c * ncooperators - (self.c * spite_factor) * ntroubles) / (
                        ncooperators + ndefectors + ntroubles)
            self._players.nodes[nodeIndex]["Reputation"] += rep_factor_c

        elif self._players.nodes[nodeIndex]["Strategy"] == 1:
            self._players.nodes[nodeIndex]["Last Payoff"] += self.r * (self.c * ncooperators - (self.c * spite_factor) * ntroubles) / (
                        ncooperators + ndefectors + ntroubles)
            self._players.nodes[nodeIndex]["Reputation"] += rep_factor_d

        elif self._players.nodes[nodeIndex]["Strategy"] == 2:
            self._players.nodes[nodeIndex]["Last Payoff"] += - self.c * spite_factor + self.r * (self.c * ncooperators - (self.c * spite_factor) * ntroubles) / (
                        ncooperators + ndefectors + ntroubles)
            self._players.nodes[nodeIndex]["Reputation"] += rep_factor_s

        self._players.nodes[nodeIndex]["Knowledge"] += self._players.nodes[nodeIndex]["Last Payoff"]

    def _revisionProtocol(self, payoff1, payoff2, reputation1, reputation2):
        w_payoff = 0.7
        p_payoff = 1 / (1 + np.exp(payoff1 - payoff2 + self.tau) / self.K)
        p_reputation = 1 / (1 + np.exp(reputation1 - reputation2 + self.tau) / self.K)
        change_likelihood = w_payoff * p_payoff + (1 - w_payoff) * p_reputation
        return change_likelihood


class bucketModel(generalModel):
    def __init__(self, nplayers, coop, defec, trouble, nParticipants):
        """
        The bucket model class holds the variables that define a public goods game in
        a mean field and the methods to play the public goods game

        :param nplayers: number of total players
        """
        self.nplayers = nplayers
        self.__initBucket(coop, defec, trouble, nParticipants)

    def __initBucket(self, coop, defec, trouble, nParticipants):
        """
        initialize strategies with a equal propability for each strategy when inital_distribution is None.
        Or using the initial distribution.
        """

        assert (coop + defec + trouble) == 1.

        graph = nx.barabasi_albert_graph(self.nplayers, nParticipants)

        pc = coop
        pd = defec
        pt = trouble

        strategies = np.random.choice([0, 1, 2], size=self.nplayers, replace=True, p=[pc, pd, pt])
        for s in range(self.nplayers):
            graph.nodes[s]["Strategy"] = strategies[s]
            graph.nodes[s]["Knowledge"] = random.uniform(0, 100)
            graph.nodes[s]["Last Payoff"] = 0
            graph.nodes[s]["Reputation"] = 0

        self._players = graph
        self.draw_graph()

    def playGame(self, game, c, r):
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


        # count the cooperators and defectors
        nc = 0
        nd = 0
        nt = 0

        participants = list(self._players.edges(game))
        participants.append((game, game))
        for node in participants:
            if self._players.nodes[node[1]]["Strategy"] == 0:
                nc += 1
            elif self._players.nodes[node[1]]["Strategy"] == 1:
                nd += 1
            elif self._players.nodes[node[1]]["Strategy"] == 2:
                nt += 1

        # assign payoffs
        for node in participants:
            self._assignPayoff(node[1], nc, nd, nt)

    def reviseStrategy(self, player_index, tau=0.1, K=0.1):
        """
        revision protocol for player1 to change his strategy to the strategy of player2

        :param player1,player2: instance of class player
        """
        # choose a randomely players
        size = len(self._players.edges(player_index))
        if size > 0:
            random_player_index = np.random.choice(size)
            random_player_index = list(self._players.edges(player_index))[random_player_index][1]

            payoff1 = self._players.nodes[player_index]["Last Payoff"]
            payoff2 = self._players.nodes[random_player_index]["Last Payoff"]
            reputation1 = self._players.nodes[player_index]["Reputation"]
            reputation2 = self._players.nodes[random_player_index]["Reputation"]

            self.tau = tau
            self.K = K

            p = self._revisionProtocol(payoff1, payoff2, reputation1, reputation2)

            change = np.random.choice([False, True], p=[1 - p, p])

            if change:
                self._players.nodes[player_index]["Strategy"] = self._players.nodes[random_player_index]["Strategy"]

    def clearPayoffs(self):
        for i in self._players:
            self._players.nodes[i]["Last Payoff"] = 0


    def cutReputations(self, node):
        cut_factor = 5
        rep_1 = self._players.nodes[node]["Reputation"]
        to_remove = []
        for u, v in self._players.edges(node):
            rep_2 = self._players.nodes[v]["Reputation"]
            if abs(rep_1 - rep_2) >= cut_factor and self._players.nodes[v]["Strategy"] != 0:
                to_remove.append(v)

        for v in to_remove:
            self._players.remove_edge(node, v)


    def countStrategies(self):
        nc = 0
        nd = 0
        nt = 0

        for node in range(self.nplayers):
            if self._players.nodes[node]["Strategy"] == 0:
                nc += 1
            elif self._players.nodes[node]["Strategy"] == 1:
                nd += 1
            elif self._players.nodes[node]["Strategy"] == 2:
                nt += 1

        return nc, nd, nt

    def draw_graph(self):
        colourMap = []
        for s in self._players:
            if self._players.nodes[s]["Strategy"] == 0:
                colourMap.append('blue')
            elif self._players.nodes[s]["Strategy"] == 1:
                colourMap.append('orange')
            elif self._players.nodes[s]["Strategy"] == 2:
                colourMap.append('green')

        pos = nx.spring_layout(self._players)  # Seed for reproducible layout
        nx.draw(self._players, pos, node_color=colourMap)
        plt.show()
