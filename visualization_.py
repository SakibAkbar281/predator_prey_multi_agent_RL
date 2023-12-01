import pickle
from utils import *
from config import *
import matplotlib.pyplot as plt
import scienceplots
from vis_functions import *

plt.style.use(['science', 'ieee'])
makedir('./results/')

train_cases, base_cases = get_all_trained_cases()




# Figure 1
# generate_simulation_results(base_cases)


fig, axs = plt.subplots(len(base_cases), 1, figsize=(6, 5), sharex=False,
                        gridspec_kw={'wspace': 0.3,
                                     'hspace': 0.3})
axs = axs.flatten()  # Flatten the 2D array of axes to a 1D array
fig.suptitle('After Training')

for ax, base_case in zip(axs, base_cases):
    hist = load_file(filename='hist.pkl', path=base_case.path)
    _, num_games, baseline_ftwp = calculate_winning_ratio(hist)
    ax.set_title(base_case.title)
    ax.plot(num_games, baseline_ftwp * np.ones_like(num_games), color='black', linewidth=2,
            linestyle='dashed',
            label='Baseline')
    ax.set_ylim(0, 100)

axs[1].set_xlabel('Number of Episodes')
axs[0].set_ylabel('Winning Percentage (Tigers)')
axs[1].legend(loc='center left', bbox_to_anchor=(1.15, 0.5))
fig.savefig('./results/fig2.png', dpi=300, format='png')
fig.show()


