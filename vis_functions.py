
import pickle
from utils import *
from config import *
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(['science', 'ieee'])

def generate_simulation_results(base_cases):
    fig, axs = plt.subplots(len(base_cases), 1, figsize=(6, 5), sharex=True, sharey=True,
                            gridspec_kw={'wspace': 0.3,
                                         'hspace': 0.3})
    axs = axs.flatten()  # Flatten the 2D array of axes to a 1D array
    fig.suptitle('Before Training')
    for ax, base_case in zip(axs, base_cases):
        hist = load_file(filename='hist.pkl', path=base_case.path)

        tiger_win_percentage, num_games, final_tiger_win_percentage = calculate_winning_ratio(hist)

        std = np.std(tiger_win_percentage, axis=0)

        ax.set_title(base_case.title)
        ax.plot(num_games, tiger_win_percentage, label='Tiger Winning Percentage')
        ax.fill_between(num_games, tiger_win_percentage - std,
                        tiger_win_percentage + std, color='red',
                        alpha=0.2)
        ax.plot(num_games, final_tiger_win_percentage * np.ones_like(num_games),
                label='Converged Tiger Winning Percentage')
        ax.text(0.5, 0.8, rf'Tiger: Deer \\ = {final_tiger_win_percentage:0.2f} $\pm$ {std:0.2f} :'
                          rf' {100 - final_tiger_win_percentage:0.2f} $\pm$ {std:0.2f}',
                ha='center', va='center', transform=ax.transAxes)
        ax.set_ylim(0, 100)
    axs[1].set_xlabel('Number of Games')
    axs[0].set_ylabel('Winning Percentage (Tigers)')
    fig.savefig('./results/fig1.png', dpi=300, format='png')
    fig.show()
