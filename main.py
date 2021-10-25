from random import random, randrange, uniform

import numpy as np
import matplotlib.pyplot as plt
from pgg import bucketModel

# total number of players
nplayers = 500

# rounds each player (approximately) plays
rounds = 100

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
r = 0.4

# loners payoff

# Allocate array to save the time evolution of strategies
strategies = np.zeros(shape=(rounds,3))

bm = bucketModel(nplayers, cop, defe, trbl)

for j in range(rounds):

    for i in range(int(nplayers / nparticipants)):
        bm.playGame(nparticipants, c, r)

    for i in range(nplayers):
        bm.reviseStragey(i)

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