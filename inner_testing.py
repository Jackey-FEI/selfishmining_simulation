# Based on this implementation by Ali Nikhalat-Jahromi, Ali Mohammad Saghiri, and Mohammad Reza Meybodi https://github.com/AliNikhalat/SelfishMining/tree/main

from inner2 import SelfishMining
import numpy as np
import matplotlib.pyplot as plt

def show_results(results1, results2, alphas, gammas):
    for i in range(results1.shape[0]):
        print("plotting", i)
        plt.plot(alphas, results2[i] - results1[i], label='gamma = ' + str(gammas[i]))
    print('showing')
    plt.title('Subgroup Revenue Advantage (Outer group alpha = .2)')
    plt.xlabel("Subgroup Alpha Value")
    plt.ylabel("Revenue Advantage")
    plt.legend()
    plt.show()
    plt.savefig('simulation.png')


if __name__ == '__main__':
    selfish_mining = SelfishMining()
    iters = 100000
    results1 = np.zeros((10,8))
    results2 = np.zeros((10,8))
    gammas = [i/10 for i in range(0,10)]
    alpha1 = .2
    alphas2 = [i/40 for i in range(0,8)]
    for i in range(len(gammas)):
        for j in range(len(alphas2)):
                selfish_mining.alpha1 = alpha1
                selfish_mining.alpha2 = alphas2[j]
                selfish_mining.gamma = gammas[i]
                selfish_mining.start_simulate(iters)
                results1[i][j] = selfish_mining.selfish_mining_revenue1
                results2[i][j] = selfish_mining.selfish_mining_revenue2
                selfish_mining.reset()
    show_results(results1, results2, alphas2, gammas)
    
