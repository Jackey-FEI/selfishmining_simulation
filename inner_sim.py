# Based on this implementation by Ali Nikhalat-Jahromi, Ali Mohammad Saghiri, and Mohammad Reza Meybodi https://github.com/AliNikhalat/SelfishMining/tree/main

from inner2 import SelfishMining

iteration_number = 500

selfish_mining = SelfishMining()
selfish_mining.alpha1 = 0.4
selfish_mining.alpha2 = 0.3
selfish_mining.gamma = .5

selfish_mining.start_simulate(iteration_number)