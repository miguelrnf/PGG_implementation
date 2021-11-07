import math
import random

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class generalModel(object):

    def __init__(self):
        self.r = None
        self._players = None

    def _assignPayoff(self, participants, host):
        spite_factor = 0.3  # Fraction of the cost that the spiteful pays in relation to the cooperator
        rep_factor = (1, -0.5, -1)  # Amount of reputation each strategy changes

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
                self._players.nodes[nodeIndex]["Last Payoff"] += -self._players.nodes[host]["Cost"] * spite_factor + \
                                                                 pool_amount + self._players.nodes[host]["Cost"]

            self._players.nodes[nodeIndex]["Reputation"] += rep_factor[self._players.nodes[nodeIndex]["Strategy"]]

            self._players.nodes[nodeIndex]["Knowledge"] += self._players.nodes[nodeIndex]["Last Payoff"]

    def _revisionProtocol(self, payoff1, payoff2, M):
        if payoff1 >= payoff2:
            return 0
        else:
            return (payoff2 - payoff1) / M


class bucketModel(generalModel):
    def __init__(self, nplayers, coop, defec, trouble, nParticipants, c, r):
        super().__init__()
        self.nplayers = nplayers
        self.c = c
        self.r = r
        self.__initBucket(coop, defec, trouble, nParticipants, c)

    def __initBucket(self, coop, defec, trouble, nParticipants, c):
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
            if strategies[s] == 1:
                graph.nodes[s]["Cost"] = 0
                continue
            graph.nodes[s]["Cost"] = c / (graph.degree[s] + 1)

        self._players = graph
        # self.draw_graph(False)

    def playGame(self, game):
        participants = list(self._players.edges(game))
        participants.append((game, game))

        self._assignPayoff(participants, game)

    def reviseStrategy(self, player_index):
        size = len(self._players.edges(player_index))
        if size > 0:
            neighbours = list(self._players.edges(player_index))
            random_player_index = np.random.choice(size)
            random_player_index = neighbours[random_player_index][1]
            neighbours.append((player_index, player_index))

            max_payoff = 0
            min_payoff = math.inf
            for t in neighbours:
                p = self._players.nodes[t[1]]["Last Payoff"]
                if p > max_payoff:
                    max_payoff = p
                if p < min_payoff:
                    min_payoff = p
            M = max_payoff - min_payoff

            payoff1 = self._players.nodes[player_index]["Last Payoff"]
            payoff2 = self._players.nodes[random_player_index]["Last Payoff"]
            p = self._revisionProtocol(payoff1, payoff2, M)

            change = np.random.choice([False, True], p=[1 - p, p])

            if change:
                self._players.nodes[player_index]["Strategy"] = self._players.nodes[random_player_index]["Strategy"]

    def clearPayoffs(self):
        for i in self._players:
            self._players.nodes[i]["Last Payoff"] = 0

    def cutReputations(self, node, cut_factor):

        rep_1 = self._players.nodes[node]["Reputation"]
        to_remove = []
        for u, v in self._players.edges(node):
            rep_2 = self._players.nodes[v]["Reputation"]
            if abs(rep_1 - rep_2) >= cut_factor and self._players.nodes[v]["Strategy"] != 0:
                to_remove.append(v)

        for v in to_remove:
            self._players.remove_edge(node, v)

    def countStrategies(self, reputation):
        nc, nd, nt, nc2, nd2, nt2 = 0, 0, 0, 0, 0, 0

        for node in self._players:
            if self._players.nodes[node]["Strategy"] == 0:
                nc += 1
            elif self._players.nodes[node]["Strategy"] == 1:
                nd += 1
            elif self._players.nodes[node]["Strategy"] == 2:
                nt += 1

        if reputation:
            for node in self._players:
                if self._players.degree(node) > 0:
                    if self._players.nodes[node]["Strategy"] == 0:
                        nc2 += 1
                    elif self._players.nodes[node]["Strategy"] == 1:
                        nd2 += 1
                    elif self._players.nodes[node]["Strategy"] == 2:
                        nt2 += 1

        return nc, nd, nt, nc2, nd2, nt2

    def draw_graph(self, custom):
        colourMap = []
        sizeMap = []
        edgec = []
        if custom:
            for s in self._players:
                if self._players.nodes[s]["Strategy"] == 0:
                    colourMap.append('cornflowerblue')
                    edgec.append('royalblue')
                elif self._players.nodes[s]["Strategy"] == 1:
                    colourMap.append('orange')
                    edgec.append('darkorange')
                elif self._players.nodes[s]["Strategy"] == 2:
                    colourMap.append('green')
                    edgec.append('darkgreen')
                sizeMap.append((self._players.degree(s)*5)**1.5)
        else:
            colourMap = ['indianred'] * self.nplayers
            edgec = ['firebrick'] * self.nplayers
            for s in self._players:
                sizeMap.append((self._players.degree(s)*3)**2)

        pos = nx.spring_layout(self._players, seed=11)  # Seed for reproducible layout
        plt.figure(1, figsize=(7, 7), dpi=500)
        nx.draw_networkx_nodes(self._players, pos, node_color=colourMap, node_size=sizeMap, alpha=0.9, edgecolors=edgec)
        nx.draw_networkx_edges(self._players, pos, edge_color="slategray")
        plt.show()

    def rm_edgeless_and_draw_graph(self, degree):
        to_be_removed = [x for x in self._players.nodes() if self._players.degree(x) < degree]

        for x in to_be_removed:
            self._players.remove_node(x)
        self.draw_graph(True)
