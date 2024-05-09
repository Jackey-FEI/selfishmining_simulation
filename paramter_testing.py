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


if __name__ == '__main__':
    selfish_mining = SelfishMining()
    iters = 100000
    results = np.zeros((10,10))
    gammas = [i/10 for i in range(0,10)]
    alphas = [i/20 for i in range(0,10)]
    for i in range(len(gammas)):
        for j in range(len(alphas)):
            selfish_mining.alpha = alphas[j]
            selfish_mining.gamma = gammas[i]
            selfish_mining.start_simulate(iters)
            results[i][j] = selfish_mining.selfish_mining_revenue
            selfish_mining.reset()
    show_results(results, alphas, gammas)
    
