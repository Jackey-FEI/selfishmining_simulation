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
        self.alpha1 = 0
        self.alpha2 = 0
        self.gamma = 0
        self.selfish_mining_revenue1 = 0
        self.selfish_mining_revenue2 = 0
        self.public_chain_length = 0
        self.private_chain_length1 = 0
        self.private_chain_length2 = 0
        self.private_chain_length2_diff = 0
        self.selfish_mining_block1 = 0
        self.selfish_mining_block2 = 0
        self.honest_mining_block = 0
        self.selfish_naive_mining_block = 0 # caculate the block number if seflish miner honestly mining
        self.delta1 = 0 # same as state delta which is the difference between the private and public chain length
        self.delta2 = 0

        self.temp_public_blocks = 0
        self.temp_private_blocks = 0

        self.choosing1 = False
        self.choosing2 = False


    def chooseFork(self):
        if self.choosing1:
            randAlpha = random.uniform(0,1)
            if randAlpha < self.alpha1 + self.alpha2:
                self.selfish_mining_block1 += 2
            else:
                randGamma = random.uniform(0,1)
                if randGamma < self.gamma:
                    self.selfish_mining_block1 += 1
                    self.honest_mining_block += 1
                else:
                    self.honest_mining_block += 2
            self.private_chain_length2 -= self.private_chain_length2_diff
            self.private_chain_length1 = 0
            self.public_chain_length = 0
            self.choosing1 = False
            return True

        elif self.choosing2:
            randAlpha = random.uniform(0,1)
            if randAlpha < self.alpha2:
                self.selfish_mining_block2 += 2
            else:
                randGamma = random.uniform(0,1)
                if randGamma < self.gamma:
                    self.selfish_mining_block2 += 1
                    self.honest_mining_block += 1
                else:
                    self.honest_mining_block += 2
            self.private_chain_length1 = 0
            self.private_chain_length2 = 0
            self.public_chain_length = 0
            self.choosing2 = False
            return True
        
        else:
            return False


    def start_simulate(self, iteration):
        # When the random number is less than alpha, 
        # the selfish miner will mine a block, otherwise the honest miner will mine a block

        self.iteration = iteration
        for i in range(iteration):
            # print(self.public_chain_length, self.private_chain_length1, self.private_chain_length2)
            if self.chooseFork():
                # print("chose fork")
                continue
            rand = random.uniform(0, 1)
            if rand <= self.alpha1:
                self.selfish_mining1()
                # print("selfish mine 1")
            elif rand <= self.alpha1 + self.alpha2:
                self.selfish_mining2()
                # print("selfish mine 2")
            else:
                self.honest_mining()
                # print("honest mine")
        if self.private_chain_length1 >=2 and self.private_chain_length2 > self.private_chain_length1:
            self.selfish_mining_block2 += self.private_chain_length2
        elif self.private_chain_length1 >=2:
            self.selfish_mining_block1 += self.private_chain_length1

        self.calculating_revenue()
        self.print_final_result()
        return

    def selfish_mining1(self):
        # mine a block and increase the private chain length
        # may need to update the public chain length
        self.private_chain_length1 += 1
        if self.private_chain_length1 > self.private_chain_length2:
            self.private_chain_length2 = self.private_chain_length1
            self.private_chain_length2_diff = self.private_chain_length1
            self.temp_public_blocks = 0
            self.temp_private_blocks = 0
        return
    
    def selfish_mining2(self):
        # mine a block and increase the private chain length
        # may need to update the public chain length
        self.private_chain_length2 += 1
        return

    def honest_mining(self):
        # mine a block and increase the public chain length
        # disclose the private chain if the delta is 0
        self.delta1 = self.private_chain_length1 - self.public_chain_length
        self.delta2 = self.private_chain_length2 - self.public_chain_length
        self.public_chain_length += 1

        if self.delta1 == 1: 
            self.choosing1 = True

        elif self.delta2 == 1:
            self.choosing2 = True

        elif self.delta1 == 2:
            self.selfish_mining_block1 += self.private_chain_length1
            self.private_chain_length2 -= self.private_chain_length1
            self.private_chain_length1 = 0
            self.public_chain_length = 0
            self.temp_private_blocks += self.private_chain_length1

        elif self.delta2 == 2:
            self.selfish_mining_block2 += self.private_chain_length2
            self.selfish_mining_block1 -= self.temp_private_blocks
            self.honest_mining_block -= self.temp_public_blocks
            self.private_chain_length1 = 0
            self.private_chain_length2 = 0
            self.public_chain_length = 0
            self.temp_public_blocks = 0
            self.temp_private_blocks = 0

        elif self.delta1 == 0:
            # honest miner is keeping the lead
            self.honest_mining_block += 1
            self.private_chain_length1 = 0
            self.private_chain_length2 = 0
            self.public_chain_length = 0
            self.temp_private_blocks = 0
            self.temp_public_blocks += 1

        return

    def calculating_revenue(self):
        # calculate the revenue of the selfish miner and the honest miner
        self.total_mining_block  = self.honest_mining_block + self.selfish_mining_block1 + self.selfish_mining_block2
        self.wasted_iteration = self.iteration - self.total_mining_block
        self.selfish_mining_revenue1 = float(self.selfish_mining_block1) / self.total_mining_block
        self.selfish_mining_revenue2 = float(self.selfish_mining_block1) / self.total_mining_block + float(self.selfish_mining_block2) / self.total_mining_block
        self.selfish_honest_mining_revenue = float(self.selfish_naive_mining_block) / self.iteration
        return
    
    def print_final_result(self):
        print('Total mining block is : {}'.format(self.total_mining_block))
        print('Selfish Mining Revenue Outer is : {}'.format(self.selfish_mining_revenue1))
        print('Selfish Mining Revenue Inner is : {}'.format(self.selfish_mining_revenue2))
        # print('Selfish Honest Mining Revenue is : {}'.format(self.selfish_honest_mining_revenue))

        return

    def reset(self):
        random.seed(None)
        self.alpha = 0
        self.gamma = 0
        self.selfish_mining_revenue = 0
        self.public_chain_length = 0
        self.private_chain_length1 = 0
        self.private_chain_length2 = 0
        self.selfish_mining_block1 = 0
        self.selfish_mining_block2 = 0
        self.temp_public_blocks = 0
        self.temp_private_blocks = 0
        self.honest_mining_block = 0
        self.selfish_naive_mining_block = 0 # caculate the block number if seflish miner honestly mining
        self.delta1 = 0 # same as state delta which is the difference between the private and public chain length
        self.delta2 = 0
 