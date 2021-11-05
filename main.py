from random import random, randrange, uniform

import numpy as np
import matplotlib.pyplot as plt
from pgg import bucketModel as bucket
from pgg_graph import bucketModel as bucketg
from tqdm import tqdm
from multiprocessing import Pool


def oneRun(nplayers, rounds, nparticipants, c, r, cop, defe, spit, last_amount, show_plot, graph):
    # rounds each player (approximately) plays
    strategies = np.zeros(shape=(rounds, 3))

    if graph:
        bm = bucketg(nplayers, cop, defe, spit, nparticipants, c)
        temp = nplayers
    else:
        bm = bucket(nplayers, cop, defe, spit)
        temp = int(nplayers/nparticipants)

    for j in range(rounds):

        strategies[j, :] = bm.countStrategies()

        for game in range(temp):
            bm.playGame(game, c, r)

    #bm.updateM()

        for p in range(nplayers):
            bm.reviseStrategy(p)

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
    return strategies[-last_amount:, 0]


def plot_data_graph(plot_data, title):
    plt.title(title)
    plt.ylabel("fraction of cooperators")
    plt.xlabel("η")
    plt.plot(plot_data[0], plot_data[1])
    plt.ylim(-0.05, 1.05)
    # plt.xlim(0, 1.55)
    plt.show()


if __name__ == '__main__':
    players = 500
    rounds = 1500
    z = 4
    c = 1.
    r = 5
    cop = 0.5
    defe = 0.5
    spit = 0.0
    last_amount = 300
    show_plot = False
    plot_data = [[], []]
    graph = True
    resolution = 40
    repetitions = 15
    enhancement = False


    if enhancement:
        # fixed z
        mx = 2 * (z + 1)
        for i in range(resolution):
            r = ((i * mx) / (resolution - 1))
            #pbar = tqdm(range(repetitions))
            #pbar.set_description("Processing %s" % i)
            arg = (players, rounds, z, c, r, cop, defe, spit, last_amount, show_plot, graph)
            with Pool(4) as p:
                res = p.starmap(oneRun, [arg] * repetitions)
                last = [ent for sublist in res for ent in sublist]

            #for j in pbar:
            #    last.extend(oneRun(players, rounds, z, c, r, cop, defe, spit, last_amount, show_plot, graph))
            weird = r / (z + 1)
            plot_data[0].append(weird)
            frac = float(sum(last)) / float(players * last_amount * repetitions)
            plot_data[1].append(frac)
            plot_data_graph(plot_data, r)
        plot_data_graph(plot_data, "Final")

        plt.ylabel("fraction of cooperators")
        plt.xlabel("η")
        plt.plot(plot_data[0], plot_data[1])
        plt.ylim(0, 1)
        plt.xlim(0, 1.5)
        plt.show()

    else:
        players = 500
        rounds = 1500
        z = 4
        c = 1.
        r = 5
        cop = 0.5
        defe = 0.5
        spit = 0.0
        show_plot = True
        graph = True
        oneRun(players, rounds, z, c, r, cop, defe, spit, last_amount, show_plot, graph)
