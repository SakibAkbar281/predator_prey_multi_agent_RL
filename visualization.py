import pickle
from utils import *
from config import *
import matplotlib.pyplot as plt
import numpy as np
import scienceplots

plt.style.use(['science', 'ieee'])
makedir('./results/')
# figure 1: Calculation of winning probabilities before training
fig, axs = plt.subplots(2, 2, figsize=(6, 5), sharex=True, sharey=True,
                        gridspec_kw={'wspace': 0.3,
                                     'hspace': 0.3})
axs = axs.flatten()  # Flatten the 2D array of axes to a 1D array
fig.suptitle('Before Training')
for ax, game_case in zip(axs, GAME_CASES.keys()):
    hist = get_simulation_results(game_case=game_case, sim_case='none')

    tiger_win_percentage, num_games, final_tiger_win_percentage = calculate_winning_ratio(hist)

    ax.set_title(GAME_CASES[game_case]['title'])
    ax.plot(num_games, tiger_win_percentage,
            label='Tiger Winning Percentage')
    ax.plot(num_games, final_tiger_win_percentage * np.ones_like(num_games),
            label='Converged Tiger Winning Percentage')
    ax.text(0.5, 0.5, f'Tiger: Deer = {final_tiger_win_percentage:0.2f} :'
                      f' {100 - final_tiger_win_percentage:0.2f}',
            ha='center', va='center', transform=ax.transAxes)
    ax.set_ylim(0, 100)
axs[2].set_xlabel('Number of Games')
axs[0].set_ylabel('Winning Percentage (Tigers)')
fig.savefig('./results/fig1.png', dpi=300, format='png')
fig.show()

# Fig2: Winning Probabilities after training
fig, axs = plt.subplots(2, 2, figsize=(6, 5), sharex=False,
                        gridspec_kw={'wspace': 0.3,
                                     'hspace': 0.3})
axs = axs.flatten()  # Flatten the 2D array of axes to a 1D array
fig.suptitle('After Training')
for ax, game_case in zip(axs, GAME_CASES.keys()):
    hist = get_simulation_results(game_case=game_case, sim_case='none')
    hist_only_tiger = get_training_results(game_case=game_case, train_case='only_tiger')
    hist_only_deer = get_training_results(game_case=game_case, train_case='only_deer')
    hist_both = get_training_results(game_case=game_case, train_case='both')

    _, _, baseline_ftwp = calculate_winning_ratio(hist)
    twp_only_tiger, neps_only_tiger, ftwp_only_tiger = calculate_winning_ratio(hist_only_tiger)
    twp_only_deer, neps_only_deer, ftwp_only_deer = calculate_winning_ratio(hist_only_deer)
    twp_both, neps_both, ftwp_both = calculate_winning_ratio(hist_both)
    ax.set_title(GAME_CASES[game_case]['title'])

    ax.plot(neps_only_tiger, baseline_ftwp * np.ones_like(neps_only_tiger), color='black', linestyle='dashed',
            label='Baseline')
    ax.plot(neps_only_tiger, ftwp_only_tiger * np.ones_like(neps_only_tiger), color='navy', linestyle='dashed')
    ax.plot(neps_only_deer, ftwp_only_deer * np.ones_like(neps_only_deer), color='darkred', linestyle='dashed')
    ax.plot(neps_both, ftwp_both * np.ones_like(neps_both), color='darkgreen', linestyle='dashed')

    ax.plot(neps_only_tiger, twp_only_tiger, color='navy', linestyle='solid',
            label='Trained Tiger Vs Untrained Deer')
    ax.plot(neps_only_deer, twp_only_deer, color='darkred', linestyle='solid',
            label='Untrained Tiger Vs trained Deer')
    ax.plot(neps_both, twp_both, color='darkgreen', linestyle='solid',
            label='Trained Tiger Vs Trained Deer')

    ax.set_ylim(0, 100)
axs[2].set_xlabel('Number of Episodes')
axs[0].set_ylabel('Winning Percentage (Tigers)')
axs[1].legend(loc='center left', bbox_to_anchor=(1.15, 0.5))
fig.savefig('./results/fig2.png', dpi=300, format='png')
fig.show()

# Fig3: Number of states visited by agents

fig, axs = plt.subplots(2, 2, figsize=(6, 5), sharex=False,
                        gridspec_kw={'wspace': 0.3,
                                     'hspace': 0.3})
axs = axs.flatten()  # Flatten the 2D array of axes to a 1D array
fig.suptitle('Number of States Visited by both tigers and deer')

for ax, game_case in zip(axs, GAME_CASES.keys()):
    hist_only_tiger = get_training_results(game_case=game_case, train_case='only_tiger')
    hist_only_deer = get_training_results(game_case=game_case, train_case='only_deer')
    hist_both = get_training_results(game_case=game_case, train_case='both')

    (q_sum_ot,
     states_visited_tiger_ot,
     states_visited_deer_ot,
     neps_only_tiger) = get_q_history(hist_only_tiger)

    (q_sum_od,
     states_visited_tiger_od,
     states_visited_deer_od,
     neps_only_deer) = get_q_history(hist_only_deer)

    (q_sum_b,
     states_visited_tiger_b,
     states_visited_deer_b,
     neps_both) = get_q_history(hist_both)

    ax.set_title(GAME_CASES[game_case]['title'])

    ax.text(0.3, 0.8, f'Total States:{GAME_CASES[game_case]["total_states"]}',
            ha='center', va='center', transform=ax.transAxes)
    ax.plot(neps_only_tiger,
            GAME_CASES[game_case]['total_states'] * np.ones_like(neps_only_tiger),
            color='black',
            linestyle='dashed',
            label='Total States')

    ax.plot(neps_only_tiger,
            states_visited_tiger_ot,
            color='navy',
            linestyle='dotted',
            label='States (tiger) [Trained only tiger]')
    ax.plot(neps_only_tiger,
            states_visited_deer_ot,
            color='navy',
            linestyle='-.',
            label='States (deer) [Trained only tiger]')

    ax.plot(neps_only_deer,
            states_visited_tiger_od,
            color='darkgreen',
            linestyle='dotted',
            label='States (tiger) [Trained only deer]')
    ax.plot(neps_only_deer,
            states_visited_deer_od,
            color='darkgreen',
            linestyle='-.',
            label='States (deer) [Trained only deer]')

    ax.plot(neps_both,
            states_visited_tiger_b,
            color='darkred',
            linestyle='dotted',
            label='States (tiger) [Trained both]')
    ax.plot(neps_both,
            states_visited_deer_b,
            color='darkred',
            linestyle='-.',
            label='States (deer) [Trained both]')

axs[2].set_xlabel('Number of Episodes')
axs[0].set_ylabel('States Visited')
axs[1].legend(loc='center left', bbox_to_anchor=(1.15, 0.5))
fig.savefig('./results/fig3.png', dpi=300, format='png')
fig.show()

# Fig4: Q_sum convergence


fig, axs = plt.subplots(2, 2, figsize=(6, 5), sharex=False,
                        gridspec_kw={'wspace': 0.3,
                                     'hspace': 0.3})
axs = axs.flatten()  # Flatten the 2D array of axes to a 1D array

fig.suptitle('Convergence of Aggregate Q values')

for ax, game_case in zip(axs, GAME_CASES.keys()):
    hist_only_tiger = get_training_results(game_case=game_case, train_case='only_tiger')
    hist_only_deer = get_training_results(game_case=game_case, train_case='only_deer')
    hist_both = get_training_results(game_case=game_case, train_case='both')

    (q_sum_ot,
     states_visited_tiger_ot,
     states_visited_deer_ot,
     neps_only_tiger) = get_q_history(hist_only_tiger)

    (q_sum_od,
     states_visited_tiger_od,
     states_visited_deer_od,
     neps_only_deer) = get_q_history(hist_only_deer)

    (q_sum_b,
     states_visited_tiger_b,
     states_visited_deer_b,
     neps_both) = get_q_history(hist_both)

    ax.set_title(GAME_CASES[game_case]['title'])

    ax.plot(neps_only_tiger,
            q_sum_ot,
            color='navy',
            linestyle='solid',
            label='Trained only tiger')

    ax.plot(neps_only_deer,
            q_sum_od,
            color='darkgreen',
            linestyle='solid',
            label='Trained only deer')

    ax.plot(neps_both,
            q_sum_b,
            color='darkred',
            linestyle='solid',
            label='Trained both')

axs[2].set_xlabel('Number of Episodes')
axs[0].set_ylabel('Aggregate Q_values')
axs[1].legend(loc='center left', bbox_to_anchor=(1.15, 0.5))
fig.savefig('./results/fig4.png', dpi=300, format='png')
fig.show()
