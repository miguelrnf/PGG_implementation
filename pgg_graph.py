# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 12:42:12 2019

@author: paul
"""
import math
import random

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class generalModel(object):
    """
    This is the base class for different public goods game model. It holds methods and properties
    that are shared thoughout the different models
    """

    def _assignPayoff(self, participants, host):
        """
        assign a payoff o one player of a public goods game

        :param player_instance: a instance of the player class
        :ncooperators: number of cooperators in the public goods game
        :nparticipants: number of participants in the public goods game
        """


        spite_factor = 0.3

        total_cost = 0

        for node in participants:
            nodeIndex = node[1]
            if self._players.nodes[nodeIndex]["Strategy"] == 2:
                total_cost -= self._players.nodes[host]["Cost"]
                continue
            elif self._players.nodes[nodeIndex]["Strategy"] == 1:
                continue
            total_cost += self._players.nodes[host]["Cost"]

        pool_amount = (total_cost * self.r) / len(participants)

        for node in participants:
            nodeIndex = node[1]
            # assign payoff depending on the strategy played by the player
            if self._players.nodes[nodeIndex]["Strategy"] == 0:
                self._players.nodes[nodeIndex]["Last Payoff"] += -self._players.nodes[host]["Cost"] + pool_amount

            elif self._players.nodes[nodeIndex]["Strategy"] == 1:
                self._players.nodes[nodeIndex]["Last Payoff"] += pool_amount

            elif self._players.nodes[nodeIndex]["Strategy"] == 2:
                self._players.nodes[nodeIndex]["Last Payoff"] += -self._players.nodes[host]["Cost"] * spite_factor + pool_amount + self._players.nodes[host]["Cost"]

            self._players.nodes[nodeIndex]["Knowledge"] += self._players.nodes[nodeIndex]["Last Payoff"]

    def _revisionProtocol(self, payoff1, payoff2, M):
        if payoff1 >= payoff2:
            return 0
        else:
            return (payoff2 - payoff1) / M


class bucketModel(generalModel):
    def __init__(self, nplayers, coop, defec, trouble, nParticipants, c):
        """
        The bucket model class holds the variables that define a public goods game in
        a mean field and the methods to play the public goods game

        :param nplayers: number of total players
        """
        self.nplayers = nplayers
        self.__initBucket(coop, defec, trouble, nParticipants, c)

    def __initBucket(self, coop, defec, trouble, nParticipants, c):
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
            if strategies[s] == 1:
                graph.nodes[s]["Cost"] = 0
                continue
            graph.nodes[s]["Cost"] = c / (graph.degree[s] + 1)

        self._players = graph
        # self.draw_graph()

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

        # set game properties
        self.c = c
        self.r = r


        participants = list(self._players.edges(game))
        participants.append((game, game))


        # assign payoffs
        self._assignPayoff(participants, game)

    def reviseStrategy(self, player_index):
        """
        revision protocol for player1 to change his strategy to the strategy of player2

        :param player1,player2: instance of class player
        """
        # choose a randomely players
        size = len(self._players.edges(player_index))
        neighbours = list(self._players.edges(player_index))
        random_player_index = np.random.choice(size)
        random_player_index = neighbours[random_player_index][1]
        neighbours.append((player_index, player_index))

        max = 0
        min = math.inf
        for t in neighbours:
            p = self._players.nodes[t[1]]["Last Payoff"]
            if p > max:
                max = p
            if p < min:
                min = p
        M = max - min



        payoff1 = self._players.nodes[player_index]["Last Payoff"]
        payoff2 = self._players.nodes[random_player_index]["Last Payoff"]

        p = self._revisionProtocol(payoff1, payoff2, M)

        change = np.random.choice([False, True], p=[1 - p, p])

        if change:
            self._players.nodes[player_index]["Strategy"] = self._players.nodes[random_player_index]["Strategy"]

    def clearPayoffs(self):
        for i in range(self.nplayers):
            self._players.nodes[i]["Last Payoff"] = 0

    def countStrategies(self):
        nc = 0
        nd = 0
        nt = 0

        for node in self._players:
            if self._players.nodes[node]["Strategy"] == 0:
                nc += 1
            elif self._players.nodes[node]["Strategy"] == 1:
                nd += 1
            elif self._players.nodes[node]["Strategy"] == 2:
                nt += 1

        return nc, nd, nt

    def draw_graph(self):
        colourMap = []
        sizeMap = []

        for node_index in self._players:
            if self._players.nodes[node_index]["Strategy"] == 0:
                colourMap.append('blue')
            elif self._players.nodes[node_index]["Strategy"] == 1:
                colourMap.append('orange')
            elif self._players.nodes[node_index]["Strategy"] == 2:
                colourMap.append('green')
            sizeMap.append((self._players.degree(node_index)*5)**2)

        pos = nx.spring_layout(self._players, seed=11)  # Seed for reproducible layout
        plt.figure(1, figsize=(40, 40))
        nx.draw(self._players, pos, node_color=colourMap, node_size=sizeMap, alpha=0.9)
        plt.show()

    def updateM(self):
        max = 0
        min = math.inf
        for node_index in self._players:
            p = self._players.nodes[node_index]["Last Payoff"]
            if p > max:
                max = p
            if p < min:
                min = p
        self.M = max - min



