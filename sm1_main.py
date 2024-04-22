from sm1_strategy import SelfishMining

iteration_number = 100000

selfish_mining = SelfishMining(False)
selfish_mining.alpha = 0.4
selfish_mining.gamma = 1

selfish_mining.start_simulate(iteration_number)

