from random import random, randrange, uniform

import numpy as np
import matplotlib.pyplot as plt
from pgg import bucketModel as bucket
from pgg_graph import bucketModel as bucketg
from tqdm import tqdm
from multiprocessing import Pool


def oneRun(nplayers, rounds, nparticipants, c, r, cop, defe, spit, last_amount, show_plot, graph, reputation):
    # rounds each player (approximately) plays
    strategies = np.zeros(shape=(rounds, 6))

    if graph:
        bm = bucketg(nplayers, cop, defe, spit, nparticipants, c)
        temp = nplayers
    else:
        bm = bucket(nplayers, cop, defe, spit)
        temp = int(nplayers/nparticipants)

    for j in range(rounds):

        strategies[j, :] = bm.countStrategies(reputation)

        for game in range(temp):
            bm.playGame(game, c, r)
            if reputation:
                bm.cutReputations(game)

    #bm.updateM()

        for p in range(nplayers):
            bm.reviseStrategy(p)
            # bm.cutReputations(game)

        bm.clearPayoffs()
    if reputation:
        result = [strategies[-1:, 3], strategies[-1:, 4], strategies[-1:, 5]]
    else:
        result = strategies[-last_amount:, 0]

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

        if reputation:
            plt.title("Strategies played (community > 2)")
            plt.xlabel("round")
            plt.ylabel("amount")
            plt.plot(np.arange(rounds-last_amount, rounds), strategies[-last_amount:, 3], label="Cooperators")
            plt.plot(np.arange(rounds-last_amount, rounds), strategies[-last_amount:, 4], label="Defectors")
            plt.plot(np.arange(rounds-last_amount, rounds), strategies[-last_amount:, 5], label="Spiteful")
            mxx = 0
            for i in range(len(strategies)-last_amount, len(strategies)):
                te = int(strategies[i:i+1, 3] + strategies[i:i+1:, 4] + strategies[i:i+1:, 5])
                if te > mxx:
                    mxx = te
            plt.ylim(0, mxx)
            plt.xlim(rounds-last_amount, rounds)
            plt.legend()
            plt.show()

    #bm.rm_edgeless_and_draw_graph(1)
    #bm.rm_edgeless_and_draw_graph(3)
    return result


def plot_data_graph(plot_data, title):
    plt.title(title)
    plt.ylabel("fraction of cooperators")
    plt.xlabel("η")
    plt.plot(plot_data[0], plot_data[1])
    plt.ylim(-0.05, 1.05)
    # plt.xlim(0, 1.55)
    plt.show()


if __name__ == '__main__':
    players = 1000
    rounds = 300
    z = 4
    c = 1.
    r = 5
    cop = 0.335
    defe = 0.335
    spit = 0.33
    last_amount = 50
    show_plot = False
    plot_data = [[], []]
    graph = True
    resolution = 28
    repetitions = 8
    enhancement = True
    reputation = True


    if enhancement:
        # fixed z
        mx = 2 * (z + 1)
        for i in range(resolution):
            r = ((i * mx) / (resolution - 1))
            #pbar = tqdm(range(repetitions))
            #pbar.set_description("Processing %s" % i)
            arg = (players, rounds, z, c, r, cop, defe, spit, last_amount, show_plot, graph, reputation)
            with Pool(4) as p:
                res = p.starmap(oneRun, [arg] * repetitions)
            if reputation:
                nc, total = 0, 0
                for l in range(len(res)):
                    nc += int(res[l][0])
                    total += int(res[l][0] + res[l][1] + res[l][2])
                frac = float(nc) / float(total)
            else:
                last = [ent for sublist in res for ent in sublist]
                frac = float(sum(last)) / float(players * last_amount * repetitions)
                #for j in pbar:
                #    last.extend(oneRun(players, rounds, z, c, r, cop, defe, spit, last_amount, show_plot, graph))
            weird = r / (z + 1)
            plot_data[0].append(weird)

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
        players = 1000
        rounds = 100
        z = 4
        c = 1.
        r = 5
        cop = 0.34
        defe = 0.33
        spit = 0.33
        show_plot = True
        graph = True
        oneRun(players, rounds, z, c, r, cop, defe, spit, last_amount, show_plot, graph, reputation)
