from random import random, randrange, uniform

import numpy as np
import matplotlib.pyplot as plt
from pgg_graph import bucketModel

# total number of players
nplayers = 500

# rounds each player (approximately) plays
rounds = 500

# Public goods game settings
# number of players that is offered to play PGG
nparticipants = 4

# cost of participating
c = 1.
# multipliaction factor for the pot
r = 5

# loners payoff
# Allocate array to save the time evolution of strategies
strategies = np.zeros(shape=(rounds,3))

bm = bucketModel(nplayers, 0.5, 0.5, 0, nparticipants, c)

for j in range(rounds):

    strategies[j, :] = bm.countStrategies()

    for game in range(nplayers):
        bm.playGame(game, c, r)

    bm.updateM()

    for i in range(nplayers):
        bm.reviseStrategy(i)

    bm.clearPayoffs()
    if j == 2 or j == 5 or j == 30:
        bm.draw_graph()



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
bm.draw_graph()