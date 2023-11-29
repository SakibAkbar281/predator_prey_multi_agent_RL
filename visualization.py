import pickle
from utils import *
from config import *
import matplotlib.pyplot as plt
import numpy as np

game_case = '2tiger2deer50steps'
train_case = 'none'
sim_case = 'none'

sim_path = './' + GAME_CASES[game_case]["folder_name"] + '/' + SIM_CASES[sim_case]["folder_name"] + '/sim/'
train_path = './' + GAME_CASES[game_case]["folder_name"] + '/' + SIM_CASES[sim_case]["folder_name"] + '/sim/'
print(sim_path)
hist = load_file(filename='hist.pkl', path=sim_path)
print(hist)
tiger_wins = np.array(hist['tiger_wins'])
deer_wins = np.array(hist['deer_wins'])
num_games = np.array(hist['num_games'])

tiger_win_percentage = tiger_wins/num_games
final_tiger_win_percentage = np.average(tiger_win_percentage[-100:])
plt.plot(num_games,tiger_win_percentage)
plt.plot(num_games,final_tiger_win_percentage*np.ones_like(num_games))
plt.show()