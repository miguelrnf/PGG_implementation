from random import random, randrange, uniform

import numpy as np
import matplotlib.pyplot as plt
from pgg import bucketModel

# total number of players
nplayers = 300

# rounds each player (approximately) plays
rounds = 20

# Public goods game settings
# number of players that is offered to play PGG
nparticipants = 4

# cost of participating
c = 1.

# multipliaction factor for the pot
r = 4.5

# loners payoff
# Allocate array to save the time evolution of strategies
strategies = np.zeros(shape=(rounds,3))

bm = bucketModel(nplayers, 0.5, 0.5, 0)

for j in range(rounds):

    strategies[j, :] = bm.countStrategies()

    for game in range(nplayers):
        bm.playGame(game, c, r)

    bm.updateM()

    for i in range(nplayers):
        bm.reviseStrategy(i)

    bm.clearPayoffs()

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