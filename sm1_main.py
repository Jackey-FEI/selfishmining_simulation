from sm1_strategy import SelfishMining

iteration_number = 1000000

selfish_mining = SelfishMining(2)
selfish_mining.set_alphas([0.32, 0.32])
selfish_mining.set_gammas([0.5, 0.5])

selfish_mining.start_simulate(iteration_number)


selfish_mining = SelfishMining(1)
selfish_mining.set_alphas([0.25])
selfish_mining.set_gammas([0.5])

selfish_mining.start_simulate(iteration_number)
