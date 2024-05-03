from sm1_strategy import SelfishMining
import numpy as np
import matplotlib.pyplot as plt

def simulate_alpha_variation(alpha1_range, alpha2_fixed, gamma=0.5):
    revenues_miner1 = []
    for alpha1 in alpha1_range:
        miner = SelfishMining(num_selfish=2)
        miner.set_alphas([alpha1, alpha2_fixed])
        miner.set_gammas([gamma, gamma])
        miner.start_simulate(10000)
        revenues_miner1.append(miner.selfish_mining_revenue[0])
    return revenues_miner1

def simulate_single_selfish_miner(alpha_range, gamma=0.5):
    revenues = []
    for alpha in alpha_range:
        miner = SelfishMining(num_selfish=1)
        miner.set_alphas([alpha])
        miner.set_gammas([gamma])
        miner.start_simulate(100000)
        revenues.append(miner.selfish_mining_revenue[0])
    return revenues

if __name__ == '__main__':

    alpha_range = np.linspace(0, 0.5, 50)
    alpha2_fixed = 0.25 

    revenues_single_miner = simulate_single_selfish_miner(alpha_range)
    revenues_two_miners = simulate_alpha_variation(alpha_range, alpha2_fixed)
    
    plt.figure(figsize=(10, 6))
    plt.plot(alpha_range, revenues_single_miner, label='Revenue of Single Selfish Miner', color='red')
    plt.plot(alpha_range, revenues_two_miners, label=f'Revenue of Miner 1 with Miner 2 Alpha Fixed at {alpha2_fixed}', color='blue')
    plt.title('Comparison of Selfish Miner Revenues')
    plt.xlabel('Alpha (Mining Power of Selfish Miner)')
    plt.ylabel('Revenue')
    plt.legend()
    plt.show()





