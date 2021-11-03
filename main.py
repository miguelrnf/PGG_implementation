from random import random, randrange, uniform

import numpy as np
import matplotlib.pyplot as plt
from pgg import bucketModel


def oneRun(nplayers, rounds, nparticipants, c, r, cop, defe, spit, show_plot):
    # rounds each player (approximately) plays
    strategies = np.zeros(shape=(rounds, 3))

    bm = bucketModel(nplayers, cop, defe, spit)

    for j in range(rounds):

        strategies[j, :] = bm.countStrategies()

        for game in range(int(nplayers/nparticipants)):
            bm.playGame(game, c, r)

        bm.updateM()

        for i in range(nplayers):
            bm.reviseStrategy(i)

        bm.clearPayoffs()

    if show_plot:
        plt.title("Strategies played")
        plt.xlabel("round")
        plt.ylabel("amount")
        plt.plot(np.arange(rounds), strategies[:, 0], label="Cooperators")
        plt.plot(np.arange(rounds), strategies[:, 1], label="Defectors")
        plt.plot(np.arange(rounds), strategies[:, 2], label="Spiteful")
        plt.ylim(0, nplayers)
        plt.xlim(0, rounds)
        plt.legend()
        plt.show()


oneRun(300, 20, 4, 1., 10, 0.5, 0.5, 0, True)

# 28 testes diferentes por graph
# enhancment de 0 a 1.5