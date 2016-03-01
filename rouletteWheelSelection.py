#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Perform 3 kinds of roulette wheel selections for Evolutionary Algorithms (EAs).

After plotting time efficiency curve, it shows that the Stochastic Acceptance has
the minimum total running time, followed by basic and bisecting search roulette wheel selection algorithms.

-----------------------------------
Created on Mon Feb 29, 2016
@author: mangwang
-----------------------------------
"""


import random
from bisect import bisect_left
import numpy as np
import timeit
import matplotlib.pyplot as plt


"""
Basic roulette wheel selection: O(N)
"""
def basic(fitness):
    '''
    Input: a list of N fitness values (list or tuple)
    Output: selected index
    '''
    sumFits = sum(fitness)
    # generate a random number
    rndPoint = random.uniform(0, sumFits)
    # calculate the index: O(N)
    accumulator = 0.0
    for ind, val in enumerate(fitness):
        accumulator += val
        if accumulator > rndPoint:
            return ind


"""
Bisecting search roulette wheel selection: O(N + logN)
"""
def bisectSearch(fitness):
    '''
    Input: a list of N fitness values (list or tuple)
    Output: selected index
    '''
    sumFits = sum(fitness)
    # generate a random number
    rndPoint = random.uniform(0, sumFits)
    # calculate the accumulator: O(N)
    accumulator = []
    accsum = 0.0
    for fit in fitness:
        accsum += fit
        accumulator.append(accsum)
    return bisect_left(accumulator, rndPoint)   # O(logN)


"""
Stochastic Acceptance: O(1) if given the N and maxFit before
"""
def stochasticAccept(fitness):
    '''
    Input: a list of N fitness values (list or tuple)
    Output: selected index
    '''
    # calculate N and max fitness value
    N = len(fitness)
    maxFit = max(fitness)
    # select: O(1)
    while True:
        # randomly select an individual with uniform probability
        ind = int(N * random.random())
        # with probability wi/wmax to accept the selection
        if random.random() < fitness[ind] / maxFit:
            return ind


"""
main function
"""
def main():
    # init number of fitness values
    N = [10, 10**2, 10**3, 10**4, 10**5]
    # calculate average total run time for each algorithm
    times = [[], [], []]
    algos = [basic, bisectSearch, stochasticAccept]
    for n in N:
        fitness = np.random.random((n,))
        for ind, algo in enumerate(algos):
            sample_times = []
            start = timeit.default_timer()
            for _ in range(100):
                algo(fitness)
                sample_times.append(timeit.default_timer() - start)
            times[ind].append(np.array(sample_times).mean())
    # plot the result
    lineStyle = ['b-o', 'g--p', 'r:*']
    algoName = ['basic', 'bisectSearch', 'stochasticAccept']
    for i in range(len(times)):
        plt.loglog(N, times[i], lineStyle[i], label=algoName[i])
    plt.legend(loc=2)
    plt.grid('on')


if __name__ == "__main__":
    main()
