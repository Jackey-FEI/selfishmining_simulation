# first strategy by using Sirer Aritcla published in 2014
import sys

import random 
from matplotlib import pyplot as plt 

import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class SelfishMining:
    def __init__(self, show_log=False):
        self._alpha = 0
        self._gamma = 0
        self.selfish_mining_revenue = 0

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        if value < 0 or value > 1:
            raise ValueError('alpha should be between 0 and 1')
        self._alpha = value
        return

    @property
    def gamma(self):
        return self._gamma

    @gamma.setter
    def gamma(self, value):
        if value < 0 or value > 1:
            raise ValueError('gamma should be between 0 and 1')
        self._gamma = value
        return

    @property
    def revenue(self):
        return self.__selfish_miner_revenue

    @property
    def stale_block(self):
        return self.__total_stale_block

    def print_input_statistic(self):
        print('alpha is : {}'.format(self._alpha))
        print('gamma is : {}'.format(self._gamma))

        return

    def start_simulate(self, iteration):
        # TODO: Implement the simulation, and calculate the revenue after the simulation
        # When the random number is less than alpha, 
        # the selfish miner will mine a block, otherwise the honest miner will mine a block

        return

    def selfish_mining(self):
        # mine a block and increase the private chain length
        # may need to update the public chain length

        return

    def honest_mining(self):
        # mine a block and increase the public chain length

        return

    def calculating_revenue(self):
        # calculate the revenue of the selfish miner and the honest miner

        return
    
    def print_final_result(self):
        print('Selfish Mining Revenue is : {}'.format(self.selfish_mining_revenue))
        print("Honest Mining Revenue is : {}".format(1 - self.selfish_mining_revenue))

        return

 