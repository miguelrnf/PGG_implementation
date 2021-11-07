import numpy as np
import matplotlib.pyplot as plt
from pgg import bucketModel as bucket
from pgg_graph import bucketModel as bucketg
from multiprocessing import Pool


def run_PGG(nplayers, rounds, nparticipants, c, r, cop, defe, spit, last_amount, show_plot, graph, reputation, cut_factor):
    strategies = np.zeros(shape=(rounds + 1, 6))

    if graph:
        bm = bucketg(nplayers, cop, defe, spit, nparticipants, c, r)
        temp = nplayers
    else:
        bm = bucket(nplayers, cop, defe, r, c)
        temp = int(nplayers / nparticipants)

    strategies[0, :] = cop * nplayers, defe * nplayers, spit * nplayers, cop * nplayers, defe * nplayers, spit * nplayers
    for j in range(rounds):
        for game in range(temp):
            bm.playGame(game)
            if reputation:
                bm.cutReputations(game, cut_factor)

        for p in range(nplayers):
            bm.reviseStrategy(p)

        strategies[j + 1, :] = bm.countStrategies(reputation)
        bm.clearPayoffs()

    if reputation:
        result = [strategies[-1:, 3], strategies[-1:, 4], strategies[-1:, 5]]
    else:
        result = strategies[-last_amount:, 0]

    if show_plot:
        plt.title("Strategies played")
        plt.xlabel("Round")
        plt.ylabel("Players")
        plt.plot(np.arange(rounds + 1), strategies[:, 0], label="Cooperators")
        plt.plot(np.arange(rounds + 1), strategies[:, 1], label="Defectors")
        if spit > 0:
            plt.plot(np.arange(rounds + 1), strategies[:, 2], label="Spiteful")
        plt.ylim(0, nplayers)
        plt.xlim(0, rounds)
        plt.legend()
        plt.show()

        if reputation:
            plt.title("Strategies played (community > 1)")
            plt.xlabel("Round")
            plt.ylabel("Players")
            plt.plot(np.arange(rounds - last_amount, rounds), strategies[-last_amount:, 3], label="Cooperators")
            plt.plot(np.arange(rounds - last_amount, rounds), strategies[-last_amount:, 4], label="Defectors")
            plt.plot(np.arange(rounds - last_amount, rounds), strategies[-last_amount:, 5], label="Spiteful")
            mxx = 0
            for x in range(len(strategies) - last_amount, len(strategies)):
                te = int(strategies[x:x + 1, 3] + strategies[x:x + 1:, 4] + strategies[x:x + 1:, 5])
                if te > mxx:
                    mxx = te
            plt.ylim(0, mxx)
            plt.xlim(rounds - last_amount, rounds)
            plt.legend()
            plt.show()

    if reputation:
        bm.rm_edgeless_and_draw_graph(1)

    return result


def plot_data_graph(data, title):
    plt.title(title)
    plt.ylabel("fraction of cooperators")
    plt.xlabel("η")
    plt.plot(data[0], data[1])
    plt.ylim(-0.05, 1.05)
    plt.show()


if __name__ == '__main__':
    players = 100  # Number of players that play PGG
    rounds = 50  # Number of rounds in the PGG
    z = 4  # If graph == True z is the average degree of the network else z is the number of players in each PGG
    c = 1  # Cost of cooperators to play the PGG
    r = 5  # Shared pool multiplier
    cop = 0.5  # Approximate initial fraction of cooperators
    defe = 0.5  # Approximate initial fraction of defectors
    spit = 0.0  # Approximate initial fraction of spitefuls
    last_amount = 10  # Number of rounds to take into account on the averages
    show_plot = False  # If the graph of evolution of the three strategies is shown
    graph = True  # If the simulation is run with an initial graph
    enhancement = True  # If false run only sim_repeat separated times,
    #                      if true calculate and show the evolution of the enhancement factor
    #                      (WARNING: Might take a lot of time and use a lot of resources)
    cpu_cores = 4  # How many cpu cores to use, only used if enhancement = True

    sim_repeat = 1  # Only used if enhancement = False, how many times to run the simulation
    reputation = False  # If true, use reputation and cut ties
    cut_factor = 20  # How much the difference in reputation before cutting the edge

    if enhancement:
        resolution = 10  # How many points on the evolution of the enhancement factor graph to show
        repetitions = 2  # How many repetitions per point to calculate average
        plot_data = [[], []]  # Empty variable to hold the plot data
        mx = 2 * (z + 1)
        for i in range(resolution):
            r = ((i * mx) / (resolution - 1))
            arg = (players, rounds, z, c, r, cop, defe, spit, last_amount, show_plot, graph, reputation, cut_factor)
            with Pool(cpu_cores) as p:
                res = p.starmap(run_PGG, [arg] * repetitions)
            if reputation:
                nc, total = 0, 0
                for l in range(len(res)):
                    nc += int(res[l][0])
                    total += int(res[l][0] + res[l][1] + res[l][2])
                frac = float(nc) / float(total)
            else:
                last = [ent for sublist in res for ent in sublist]
                frac = float(sum(last)) / float(players * last_amount * repetitions)
            weird = r / (z + 1)
            plot_data[0].append(weird)
            plot_data[1].append(frac)
            plot_data_graph(plot_data, "r = " + str(r))
        plot_data_graph(plot_data, "Final")
    else:
        for k in range(sim_repeat):
            run_PGG(players, rounds, z, c, r, cop, defe, spit, last_amount, show_plot, graph, reputation, cut_factor)
