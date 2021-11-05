from random import random, randrange, uniform

import numpy as np
import matplotlib.pyplot as plt
from pgg_graph import bucketModel


def oneRun(nplayers, rounds, nparticipants, c, r, cop, defe, spit, last_amount, show_plot):
    # rounds each player (approximately) plays
    strategies = np.zeros(shape=(rounds, 3))

    bm = bucketModel(nplayers, cop, defe, spit, nparticipants, c)

    for j in range(rounds):

        strategies[j, :] = bm.countStrategies()

        for game in range(int(nplayers/nparticipants)):
            bm.playGame(game, c, r)

    #bm.updateM()

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

    return strategies[-last_amount:, ]



players = 500
rounds = 1000
z = 4
c = 1
r = 20
cop = 0.5
defe = 0.5
spit = 0
last_amount = 150
show_plot = False
plot_data = [[], []]

#fixed z
for i in range(10):
    r = ((i * 20) / 9)
    last = oneRun(players, rounds, z, c, r, cop, defe, spit, last_amount, show_plot)
    weird = r / (z + 1)
    nc = sum(last[:, 0])
    total = players * last_amount
    plot_data[0].append(weird)
    plot_data[1].append(nc/total)

plt.ylabel("fraction of cooperators")
plt.xlabel("η")
plt.plot(plot_data[0], plot_data[1])
plt.ylim(0, 1)
plt.xlim(0, 1.5)
plt.show()
