import pickle
from utils import *
from config import *
import matplotlib.pyplot as plt

case = 1
sim_case = 1

folder_path = './' + CASES[case]["folder_name"] + '/' + SIM_CASES[sim_case]["folder_name"] + '/sim/'
print(folder_path)
hist = load_file(filename='hist.pkl',path=folder_path)

tiger_wins = hist['tiger_wins']
deer_wins = hist['deer_wins']
num_games = hist['num_games']
plt.plot(num_games,deer_wins)
plt.show()