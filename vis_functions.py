import pickle
from utils import *
from config import *
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(['science', 'ieee'])


def generate_simulation_results(base_cases):
    fig, axs = plt.subplots(1, len(base_cases), figsize=(6, 3), sharex=True, sharey=True,
                            gridspec_kw={'wspace': 0.3,
                                         'hspace': 0.3})
    # axs = axs.flatten()  # Flatten the 2D array of axes to a 1D array
    axs = [axs] if len(base_cases) == 1 else axs.flatten()
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
    axs[len(base_cases)-1].set_xlabel('Number of Games')
    axs[0].set_ylabel('Winning Percentage (Tigers)')
    fig.savefig('./results/fig1.png', dpi=300, format='png')
    fig.show()


def generate_after_training_plots(game_cases):
    fig, axs = plt.subplots(1, len(game_cases), figsize=(6, 3), sharex=False,
                            gridspec_kw={'wspace': 0.3,
                                         'hspace': 0.3})
    # axs = axs.flatten()  # Flatten the 2D array of axes to a 1D array
    fig.suptitle('After Training')
    axs = [axs] if len(game_cases) == 1 else axs.flatten()
    for ax, train_cases in zip(axs, game_cases):
        for train_case in train_cases:
            if train_case.is_base_case():
                hist = load_file(filename='hist.pkl', path=train_case.path)
                _, num_games, baseline_ftwp = calculate_winning_ratio(hist)
                ax.set_title(train_case.title)
                ax.plot(num_games, baseline_ftwp * np.ones_like(num_games), color=train_case.color, linewidth=2,
                        linestyle='dashed',
                        label=train_case.label)
            else:
                hist = load_file(filename='hist.pkl', path=train_case.path)
                twp, neps, ftwp = calculate_winning_ratio(hist)
                ax.plot(neps, twp, color=train_case.color, linestyle='solid',
                        label=train_case.label)
            ax.set_ylim(0, 100)

    axs[len(game_cases)-1].set_xlabel('Number of Episodes')
    axs[0].set_ylabel('Winning Percentage (Tigers)')
    axs[len(game_cases)-1].legend(loc='center left', bbox_to_anchor=(1.15, 0.5))
    fig.savefig('./results/fig2.png', dpi=300, format='png')
    fig.show()


def generate_states_visited_plots(game_cases):
    fig, axs = plt.subplots(1, len(game_cases), figsize=(6, 3), sharex=False,
                            gridspec_kw={'wspace': 0.3,
                                         'hspace': 0.3})
    # axs = axs.flatten()  # Flatten the 2D array of axes to a 1D array
    # fig.suptitle('Number of States Visited by both tigers and deer')
    axs = [axs] if len(game_cases) == 1 else axs.flatten()
    for ax, train_cases in zip(axs, game_cases):
        for train_case in train_cases:
            if train_case.is_base_case():
                ax.set_title(train_case.title)
                hist = load_file(filename='hist.pkl', path=train_case.path)
                _, num_games, _ = calculate_winning_ratio(hist)
                ax.text(0.3, 0.8, f'Total States: {train_case.total_states}',
                        ha='center', va='center', transform=ax.transAxes)
                ax.plot(num_games,
                        train_case.total_states * np.ones_like(num_games),
                        color=train_case.color,
                        linestyle='dashed',
                        label='Total States')
            else:
                hist = load_file(filename='hist.pkl', path=train_case.path)
                (q_sum,
                 states_visited_tiger,
                 states_visited_deer,
                 neps) = get_q_history(hist)
                if not np.all(states_visited_tiger == 0):
                    ax.plot(neps,
                            states_visited_tiger,
                            color=train_case.color,
                            linestyle='dotted',
                            label=f'States (tiger) {train_case.label}')
                if not np.all(states_visited_deer==0):
                    ax.plot(neps,
                            states_visited_deer,
                            color=train_case.color,
                            linestyle='-.',
                            label=f'States (deer) {train_case.label}')

    axs[len(game_cases)-1].set_xlabel('Number of Episodes')
    axs[0].set_ylabel('States Visited')
    axs[len(game_cases)-1].legend(loc='center left', bbox_to_anchor=(1.15, 0.5))
    fig.savefig('./results/fig3.png', dpi=300, format='png')
    fig.show()


def generate_q_conv_plots(game_cases):
    fig, axs = plt.subplots(1, len(game_cases), figsize=(6, 3), sharex=False,
                            gridspec_kw={'wspace': 0.3,
                                         'hspace': 0.3})
    # axs = axs.flatten()  # Flatten the 2D array of axes to a 1D array
    # fig.suptitle('Convergence of Aggregate Q values')
    axs = [axs] if len(game_cases) == 1 else axs.flatten()
    for ax, train_cases in zip(axs, game_cases):
        for train_case in train_cases:
            if train_case.is_base_case():
                ax.set_title(train_case.title)
            else:
                hist = load_file(filename='hist.pkl', path=train_case.path)
                (q_sum,
                 states_visited_tiger,
                 states_visited_deer,
                 neps) = get_q_history(hist)

                ax.plot(neps,
                        q_sum,
                        color=train_case.color,
                        linestyle='solid',
                        label=f'{train_case.label}')

    axs[len(game_cases) - 1].set_xlabel('Number of Episodes')
    axs[0].set_ylabel('Aggregate Q')
    axs[len(game_cases) - 1].legend(loc='center left', bbox_to_anchor=(1.15, 0.5))
    fig.savefig('./results/fig4.png', dpi=300, format='png')
    fig.show()
