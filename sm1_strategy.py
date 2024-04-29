import sys

import random 
from matplotlib import pyplot as plt 

import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class SelfishMining:
    def __init__(self, num_selfish = 2):
        random.seed(None)
        self.num_selfish = num_selfish
        self._alphas = [0.0] * num_selfish
        self._gammas = [0.0] * num_selfish
        self.honest_alpha = 0.0
        self.honest_gamma = 0.0
        self.selfish_mining_revenue = [0.0] * num_selfish
        self.public_chain_length = 0
        self.private_chain_length = [0.0] * num_selfish
        self.selfish_mining_block = [0.0] * num_selfish
        self.honest_mining_block = 0
        self.selfish_naive_mining_block = [0.0] * num_selfish # caculate the block number if seflish miner honestly mining
        self.delta = 0 # same as state delta which is the difference between the private and public chain length

    def set_alphas(self, alphas):
        self._alphas = alphas
        self.honest_alpha = 1- sum(alphas)
        
    def set_gammas(self,gammas):
        self._gammas = gammas
        self.honest_gamma = 1 - sum(gammas)

    def print_input_statistic(self):
        print('alpha_1 is : {}'.format(self._alphas[0]))
        print('gamma_1 is : {}'.format(self._gammas[0]))
        print('alpha_2 is : {}'.format(self._alphas[1]))
        print('gamma_2 is : {}'.format(self._gammas[1]))

        return
    
    def random_pick(self):
        prop_list  = [0.0] * (self.num_selfish+1)
        for i in range(self.num_selfish):
            if i == 0:
                prop_list[i] = self._alphas[i]
            else:
                prop_list[i] = self._alphas[i]+ prop_list[i-1]
        prop_list[self.num_selfish] = 1.0
        rand = random.uniform(0, 1)
        for i in range(self.num_selfish+1):
            if rand <= prop_list[i]:
                return i
        return 0 # shouldn't reach here
    
    def select_candidate_gamma(self,gammas):
        total_gamma = sum(gammas)
        probabilities = [gammas[i] / total_gamma for i in range(len(gammas))]
        accum_probabilities = []
        prob_sum = 0
        for prob in probabilities:
            prob_sum += prob
            accum_probabilities.append(prob_sum)
        rand = random.uniform(0, 1)
        for i, prob in enumerate(accum_probabilities):
            if rand <= prob:
                return i

    def start_simulate(self, iteration):
        # When the random number is less than alpha, 
        # the selfish miner will mine a block, otherwise the honest miner will mine a block
        self.iteration = iteration
        for i in range(iteration):
            rand_index = self.random_pick()
            if rand_index<self.num_selfish:
                self.selfish_mining(rand_index)
                self.selfish_naive_mining_block[rand_index] += 1
            else:
                self.honest_mining()

        max_private_chain = 0
        candidates = []
        for i in range(self.num_selfish):
            if self.private_chain_length[i] > max_private_chain:
                max_private_chain = self.private_chain_length[i]
                candidates = [i]
            elif self.private_chain_length[i] == max_private_chain:
                candidates.append(i)
        if max_private_chain >=1 :
            gammas = []
            for i in candidates:
                gammas.append(self._gammas[i])
            index = self.select_candidate_gamma(gammas) # index in the candidates
            self.selfish_mining_block[candidates[index]]+=self.private_chain_length[candidates[index]]
        self.calculating_revenue()
        self.print_final_result()
        return

    def selfish_mining(self, selfish_index):
        # mine a block and increase the private chain length
        # may need to update the public chain length
        delta = self.private_chain_length[selfish_index] - self.public_chain_length
        self.private_chain_length[selfish_index] += 1
        if delta == 0 and self.private_chain_length == 2: # TODO what if private chain leangth > 2, should we adopt this strategy
            self.selfish_mining_block[selfish_index] +=  self.private_chain_length[selfish_index] 
            self.private_chain_length = [0 for _ in range(self.num_selfish)]
            self.public_chain_length = 0 # only one public chain (longest chain)
        return

    def honest_mining(self):
        # mine a block and increase the public chain length
        # disclose the private chain if the delta is 0
        
        max_delta = -1
        candidates = []
        gammas = []
        # Determine the maximum delta and collect candidates with this delta
        for i in range(self.num_selfish):
            delta = self.private_chain_length[i] - self.public_chain_length
            if delta > max_delta:
                max_delta = delta
                candidates = [i]
            elif delta == max_delta:
                candidates.append(i)
        self.public_chain_length += 1
        if max_delta == 0 and self.private_chain_length[candidates[0]] == 0:
            self.honest_mining_block += 1
            self.private_chain_length = [0 for _ in range(self.num_selfish)]
            self.public_chain_length = 0
        elif max_delta == 0:
            for i in candidates:
                gammas.append(self._gammas[i])
            gammas.append(1-sum(gammas))
            index = self.select_candidate_gamma(gammas) # index in the candidates
            if index == (len(gammas)-1):
                self.honest_mining_block+=2
            else:
                self.honest_mining_block+=1
                self.selfish_mining_block[candidates[index]]+=1
            self.public_chain_length = 0
            self.private_chain_length = [0 for _ in range(self.num_selfish)]
        elif max_delta == 2:
            for i in candidates:
                gammas.append(self._gammas[i])
            index = self.select_candidate_gamma(gammas) # index in the candidates
            self.selfish_mining_block[candidates[index]]+=self.private_chain_length[candidates[index]]
            self.public_chain_length = 0
            self.private_chain_length = [0 for _ in range(self.num_selfish)]

        return

    def calculating_revenue(self):
        # calculate the revenue of the selfish miner and the honest miner
        self.total_mining_block  = self.honest_mining_block + sum(self.selfish_mining_block)
        self.wasted_iteration = self.iteration - self.total_mining_block
        self.selfish_mining_revenue = [float(self.selfish_mining_block[i]) / self.total_mining_block for i in range(self.num_selfish)]
        self.selfish_honest_mining_revenue = [float(self.selfish_naive_mining_block[i]) / self.iteration for i in range(self.num_selfish)]
        return
    
    def print_final_result(self):
        print('Total mining block is : {}'.format(self.total_mining_block))
        print('Selfish Mining Revenue is : {}'.format(self.selfish_mining_revenue))
        print('Selfish Honest Mining Revenue is : {}'.format(self.selfish_honest_mining_revenue))

        return

    def reset(self):
        random.seed(None)
        self.public_chain_length = 0
        self.private_chain_length = [0.0] * self.num_selfish
        self.selfish_mining_block = [0.0] * self.num_selfish
        self.honest_mining_block = 0
        self.selfish_naive_mining_block = [0.0] * self.num_selfish
        self.delta = 0
        self.selfish_mining_revenue = [0.0] * self.num_selfish