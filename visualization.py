import pickle
from utils import *
from config import *
import matplotlib.pyplot as plt
import numpy as np
import scienceplots
plt.style.use(['science', 'ieee'])

hist = get_simulation_results(game_case='2tiger2deer50steps', sim_case='none')
tiger_wins = np.array(hist['tiger_wins'])
deer_wins = np.array(hist['deer_wins'])
num_games = np.array(hist['num_games'])
tiger_win_percentage = tiger_wins / num_games
final_tiger_win_percentage = np.average(tiger_win_percentage[-100:])

fig, axs = plt.subplots(2,2, figsize=(4,4))
plt.plot(num_games, tiger_win_percentage)
plt.plot(num_games, final_tiger_win_percentage * np.ones_like(num_games))
plt.show()
