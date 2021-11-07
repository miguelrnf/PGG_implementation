# PGG simulation

PGG simulation is a Python script capable of running a PGG game with or without an initial network. 
It also supports three different strategies, Cooperator, Defector and Spiteful

## Installation

No need to install, just follow usage

## Variables

main.py

| Variable      | Type     | Line | Description | 
| ------------- | -------- | ---- | ------------|
| `players`     | Integer  | 82   | Number of players that play PGG|
| `rounds`      | Integer  | 83   | Number of rounds in the PGG|
| `z`           | Integer  | 84   |  If graph == True z is the average degree of the network else z is the number of players in each PGG|
| `c`           | Integer  | 85   | Cost of cooperators to play the PGG|
| `r`           | Integer  | 86   | Shared pool multiplier|
| `cop`         | Float    | 87   | Approximate initial fraction of cooperators|
| `defe`        | Float    | 88   | Approximate initial fraction of defectors|
| `spit`        | Float    | 89   | Approximate initial fraction of spitefuls|
| `last_amount` | Integer  | 90   | Number of rounds to take into account on the averages|
| `show_plot`   | Boolean  | 91   | If the graph of evolution of the three strategies is shown|
| `graph`       | Boolean  | 92   | If the simulation is run with an initial graph|
| `enhancement` | Boolean  | 93   |If false run only sim_repeat separated times, if true calculate and show the evolution of the enhancement factor (WARNING:Might take a lot of time and use a lot of resources)|
| `cpu_cores`   | Integer  | 96   | How many cpu cores to use, only used if enhancement = True|
| `sim_repeat`  | Integer  | 98   | Only used if enhancement = False, how many times to run the simulation|
| `reputation`  | Boolean  | 99   | If true, use reputation and cut ties|
| `cut_factor`  | Integer  | 100  | How much the difference in reputation before cutting the edge|

pgg_graph.py

| Variable      | Type       | Line | Description                                                               | 
| ------------- | ---------- | ---- | ------------------------------------------------------------------------- |
| `spite_factor`| Float      | 16   | Fraction of the cost that the spiteful pays in relation to the cooperator |
| `rep_factor`  | Tuple(3)   | 17   | Amount of reputation each strategy changes                                |

## Usage

Just run main.py with the desired parameters
```python
from main import run_PGG
 
run_PGG(players, rounds, z, c, r, cop, defe, spit, last_amount, show_plot, graph, reputation, cut_factor)
```
