import pickle
from utils import *
from config import *
import matplotlib.pyplot as plt
import scienceplots
from vis_functions import *

plt.style.use(['science', 'ieee'])
makedir('./results/')

game_cases = get_all_trained_cases()
base_cases = get_base_cases(game_cases)
ext = 'png'
# Figure 1
generate_simulation_results(base_cases, ext=ext)
generate_after_training_plots(game_cases, ext=ext)
generate_states_visited_plots(game_cases, ext=ext)
generate_q_conv_plots(game_cases, ext=ext)
