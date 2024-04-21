from sm1_strategy import SelfishMining

iteration_number = 10000

selfish_mining = SelfishMining(False)
selfish_mining.alpha = 0.5
selfish_mining.gamma = 1

selfish_mining.start_simulate(iteration_number)
selfish_mining.print_final_result()

