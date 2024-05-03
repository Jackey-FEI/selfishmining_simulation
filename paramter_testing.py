from sm1_strategy import SelfishMining
import numpy as np
import matplotlib.pyplot as plt

def show_results(results, alphas, gammas):
    for i in range(results.shape[0]):
        print("plotting", i)
        plt.plot(alphas, results[i], label='gamma = ' + str(gammas[i]))
    print('showing')
    plt.title('Selfish Mining Revenue for Different Alpha and Gamma Parameters')
    plt.xlabel("Alpha Value")
    plt.ylabel("Revenue")
    plt.legend()
    plt.show()
    plt.savefig('simulation.png')


    
def simulate_selfish_mining(alpha_range, gamma=0.5):
    revenue_miner2 = np.zeros((len(alpha_range), len(alpha_range)))
    for i, alpha1 in enumerate(alpha_range):
        for j, alpha2 in enumerate(alpha_range):
            miner = SelfishMining(num_selfish=2)
            miner.set_alphas([alpha1, alpha2])
            miner.set_gammas([gamma, gamma])
            miner.start_simulate(100000)  
            # revenue_miner2[i, j] = miner.selfish_mining_revenue[1]
            revenue_miner2[i, j] = sum(miner.selfish_mining_revenue)
    return revenue_miner2

def simulate_selfish_mining_2(alpha_range, gamma=0.5):
    revenue_miner2 = np.zeros((len(alpha_range), len(alpha_range)))
    for i, alpha1 in enumerate(alpha_range):
        miner = SelfishMining(num_selfish=2)
        miner.set_alphas([alpha1, 0.25])
        miner.set_gammas([gamma, gamma])
        miner.start_simulate(100000)  # Assuming 10000 iterations is enough for stable results
        revenue_miner2[i] = miner.selfish_mining_revenue[0]
    return revenue_miner2

if __name__ == '__main__':
    alpha_range = np.linspace(0, 0.4, 40)  # 40 points from 0 to 0.4
    alphas1, alphas2 = np.meshgrid(alpha_range, alpha_range)
    revenues_miner1 = simulate_selfish_mining(alpha_range)
    # alphas1, alphas2, revenues = zip(*simulation_results)
    fig = plt.figure()
   
    ax1 = fig.add_subplot(121, projection='3d')
    #surf1 = ax1.plot_surface(alphas1, alphas2, revenues_miner1, cmap='viridis', edgecolor='none')
    ax1.scatter(alphas1, alphas2, revenues_miner1, c='r', marker='o')
    ax1.set_title('Revenue of Miner 1')
    ax1.set_xlabel('Alpha 1')
    ax1.set_ylabel('Alpha 2')
    ax1.set_zlabel('Revenue')
    #fig.colorbar(surf1, ax=ax1, shrink=0.5, aspect=10)

    
    # plt.figure(figsize=(10, 5))
    # plt.plot(alpha_range, revenues_miner1, label='Revenue of Miner 1', color='blue')
    # plt.title('Revenue of Miner 1 vs. Alpha 1 with Alpha 2 Fixed at 0.25')
    # plt.xlabel('Alpha 1')
    # plt.ylabel('Revenue')
    # plt.legend()
    plt.show()




