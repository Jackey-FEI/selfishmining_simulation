from sm1_strategy import SelfishMining

iteration_number = 100000

selfish_mining = SelfishMining(2)
selfish_mining.set_alphas([0.3, 0.2])
selfish_mining.set_gammas([0.33, 0.33])

selfish_mining.start_simulate(iteration_number)


selfish_mining = SelfishMining(1)
selfish_mining.set_alphas([0.3])
selfish_mining.set_gammas([0.1])

selfish_mining.start_simulate(iteration_number)
