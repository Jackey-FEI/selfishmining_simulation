# Based on this implementation by Ali Nikhalat-Jahromi, Ali Mohammad Saghiri, and Mohammad Reza Meybodi https://github.com/AliNikhalat/SelfishMining/tree/main

import sys

import random 
from matplotlib import pyplot as plt 

import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class SelfishMining:
    def __init__(self):
        random.seed(None)
        self._alpha_inner = 0
        self._alpha_outer = 0
        self._gamma = 0
        self.selfish_mining_revenue_inner = 0
        self.selfish_mining_revenue_outer = 0
        self.public_chain_length = 0
        self.private_chain_length_outer = 0
        self.private_chain_length_inner = 0
        self.selfish_mining_block_outer = 0
        self.selfish_mining_block_inner = 0
        self.honest_mining_block = 0
        self.selfish_naive_mining_block = 0 # caculate the block number if seflish miner honestly mining
        self.delta_outer = 0 # same as state delta which is the difference between the private and public chain length
        self.delta_inner = 0

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        if value < 0 or value > 1:
            raise ValueError('alpha value should be between 0 and 1')
        self._alpha = value
        return

    @property
    def gamma(self):
        return self._gamma

    @gamma.setter
    def gamma(self, value):
        if value < 0 or value > 1:
            raise ValueError('gamma value should be between 0 and 1')
        self._gamma = value
        return

    def print_input_statistic(self):
        print('alpha is : {}'.format(self._alpha))
        print('gamma is : {}'.format(self._gamma))

        return

    def start_simulate(self, iteration):
        # When the random number is less than alpha, 
        # the selfish miner will mine a block, otherwise the honest miner will mine a block
        self.iteration = iteration
        for i in range(iteration):
            rand = random.uniform(0, 1)
            if rand <= self._alpha:
                self.simulate_inner()
                self.selfish_naive_mining_block += 1 #LOOK INTO WHAT THIS DOES
            else:
                self.honest_mining_outer()
        if self.private_chain_length >=2 :
            self.selfish_mining_block += self.private_chain_length

        self.calculating_revenue()
        self.print_final_result()
        return
    
    def simulate_inner(self):
        rand = random.uniform(0,1)
        if rand <= self._alpha_inner:
            self.selfish_mining_inner()
        else:
            self.selfish_mining_outer()
            self.honest_mining_inner()
        return

    def selfish_mining_outer(self):
        # mine a block and increase the private chain length
        # may need to update the public chain length
        self.delta_outer = self.private_chain_length_outer - self.public_chain_length
        self.private_chain_length_outer += 1
        if self.delta_outer == 0 and self.private_chain_length_outer == 2: # TODO what if private chain leangth > 2, should we adopt this strategy
            self.selfish_mining_block_outer += self.private_chain_length_outer 
            self.private_chain_length_outer = 0
            self.public_chain_length = 0
        return
    
    def selfish_mining_inner(self):
        # mine a block and increase the private chain length
        # may need to update the public chain length
        self.delta_inner = self.private_chain_length_inner - self.private_chain_length_outer
        self.private_chain_length_inner += 1
        if self.delta_inner == 0 and self.private_chain_length_inner == 2: # TODO what if private chain leangth > 2, should we adopt this strategy
            self.selfish_mining_block_inner += self.private_chain_length_inner 
            self.private_chain_length_inner = 0
            self.private_chain_length_outer = 0
        return

    def honest_mining_outer(self):
        # mine a block and increase the public chain length
        # disclose the private chain if the delta is 0
        self.delta_outer = self.private_chain_length_outer - self.public_chain_length
        self.public_chain_length += 1
        if self.delta_outer == 0 and self.private_chain_length_outer > 0:
            rand = random.uniform(0, 1)
            if rand <= self._gamma: # mining on the private pool honest miner won
                self.honest_mining_block+=1
                self.selfish_mining_block_outer+=1
            else:                   # mining on the public pool honest miner won
                self.honest_mining_block+=2
            self.private_chain_length_outer = 0
            self.public_chain_length = 0
        elif self.delta == 2:
            # selfish miner disclose the chain and get all the profit rightnow
            self.selfish_mining_block_outer += self.private_chain_length_outer 
            self.private_chain_length_outer = 0
            self.public_chain_length = 0
        elif self.delta == 0:
            # honest miner is keeping the lead
            self.honest_mining_block += 1
            self.private_chain_length_outer = 0
            self.public_chain_length = 0

        return
    
    def honest_mining_inner(self):
        # mine a block and increase the public chain length
        # disclose the private chain if the delta is 0
        self.delta_inner = self.private_chain_length_inner - self.private_chain_length_outer
        self.private_chain_length_outer += 1
        if self.delta_inner == 0 and self.private_chain_length_inner > 0:
            rand = random.uniform(0, 1)
            if rand <= self._gamma_inner: # mining on the private pool honest miner won
                self.selfish_mining_block_inner+=1
                self.selfish_mining_block_outer+=1
            else:                   # mining on the public pool honest miner won
                self.selfish_mining_block_outer+=2
            self.private_chain_length_outer = 0
            self.private_chain_length_inner = 0
        elif self.delta_inner == 2:
            # selfish miner disclose the chain and get all the profit rightnow
            self.selfish_mining_block_inner += self.private_chain_length_inner 
            self.private_chain_length_inner = 0
            self.private_chain_length_outer = 0
        elif self.delta_inner == 0:
            # honest miner is keeping the lead
            self.selfish_mining_block_outer += 1
            self.private_chain_lengthInner = 0
            self.private_chain_length_outer = 0

        return

    def calculating_revenue(self):
        # calculate the revenue of the selfish miner and the honest miner
        self.total_mining_block  = self.honest_mining_block + self.selfish_mining_block
        self.wasted_iteration = self.iteration - self.total_mining_block
        self.selfish_mining_revenue = float(self.selfish_mining_block) / self.total_mining_block
        self.selfish_honest_mining_revenue = float(self.selfish_naive_mining_block) / self.iteration
        return
    
    def print_final_result(self):
        print('Total mining block is : {}'.format(self.total_mining_block))
        print('Selfish Mining Revenue is : {}'.format(self.selfish_mining_revenue))
        print('Selfish Honest Mining Revenue is : {}'.format(self.selfish_honest_mining_revenue))

        return

    def reset(self):
        random.seed(None)
        self._alpha = 0
        self._gamma = 0
        self.selfish_mining_revenue = 0
        self.public_chain_length = 0
        self.private_chain_length = 0
        self.selfish_mining_block = 0
        self.honest_mining_block = 0
        self.selfish_naive_mining_block = 0 # caculate the block number if seflish miner honestly mining
        self.delta = 0 # same as state delta which is the difference between the private and public chain length