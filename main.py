from random import random, randrange, uniform

import numpy as np
import matplotlib.pyplot as plt
from pgg_graph import bucketModel


# total number of players
nplayers = 100

# rounds each player (approximately) plays
rounds = 20

# Public goods game settings
# number of players that is offered to play PGG
nparticipants = 4

# cost of participating
c = 1.

cop = random()

defe = 1 - uniform(cop, 1.0)

trbl = 1 - (defe + cop)

print("Cooperators: ", cop)
print("Defectors: ", defe)
print("Spite: ", trbl)

# multipliaction factor for the pot
r = 1.7

# loners payoff

# Allocate array to save the time evolution of strategies
strategies = np.zeros(shape=(rounds,3))

bm = bucketModel(nplayers, 0.33, 0.33, 0.34, nparticipants)

for j in range(rounds):

    for game in range(nplayers):
        bm.playGame(game, c, r)

    for i in range(nplayers):
        bm.reviseStrategy(i)
        bm.cutReputations(i)

    bm.clearPayoffs()


    strategies[j, :] = bm.countStrategies()

plt.title("Stragies played")
plt.xlabel("round")
plt.ylabel("amount")
plt.plot(np.arange(rounds), strategies[:, 0], label="Cooperators")
plt.plot(np.arange(rounds), strategies[:, 1], label="Defectors")
plt.plot(np.arange(rounds), strategies[:, 2], label="Troublemaker")
plt.ylim(0, nplayers)
plt.xlim(0, rounds)
plt.legend()
plt.show()
bm.draw_graph()