import math
import os
import pygame
import pickle
from config import *
import numpy as np
def makedir(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
def save_file(var, filename, path='./'):
    with open(path+filename, 'wb') as f:
        pickle.dump(var, f)
def load_file(filename, path='./'):
    with open(path+filename, 'rb') as f:
        var = pickle.load(f)
    return var
def get_simulation_results(game_case, sim_case):
    sim_path = get_sim_path(game_case,sim_case)
    hist = load_file(filename='hist.pkl', path=sim_path)
    return hist

def get_training_results(game_case, train_case):
    train_path = get_train_path(game_case,train_case)
    hist = load_file(filename='hist.pkl', path=train_path)
    return hist

def get_sim_path(game_case, sim_case):
    folder_path = './' + GAME_CASES[game_case]["folder_name"] + '/' + SIM_CASES[sim_case]["folder_name"] + '/sim/'
    return folder_path

def get_train_path(game_case, train_case):
    folder_train_path = './' + GAME_CASES[game_case]["folder_name"] + '/' + TRAIN_CASES[train_case]["folder_name"] + '/train/'
    return folder_train_path

def calculate_winning_ratio(hist):
    tiger_wins = np.array(hist['tiger_wins'])
    deer_wins = np.array(hist['deer_wins'])
    num_games = np.array(hist['num_games'])
    tiger_win_percentage = 100 * tiger_wins / num_games
    final_tiger_win_percentage = np.average(tiger_win_percentage[-100:])
    return tiger_win_percentage, num_games, final_tiger_win_percentage

def get_q_history(hist):
    q_sum = np.array(hist['q_sum'])
    states_visited_tiger = np.array(hist['states_visited_tiger'])
    states_visited_deer = np.array(hist['states_visited_deer'])
    neps = np.array(hist["num_games"])
    return q_sum, states_visited_tiger, states_visited_deer, neps

def calculate_angle(sprite1, sprite2):
    # Get the center positions of the sprites
    x1, y1 = sprite1.rect.center
    x2, y2 = sprite2.rect.center

    # Calculate the difference in positions
    dx = x2 - x1
    dy = y2 - y1

    # Calculate the angle using atan2
    # atan2 returns the angle in radians, so we convert it to degrees
    angle = math.atan2(dy, dx)
    angle_degrees = math.degrees(angle)

    return angle_degrees

def is_sufficiently_different(angles, threshold=85):
    """
    Check if all angles in the list are at least 'threshold' degrees apart from each other.

    :param angles: List of angles (in degrees).
    :param threshold: Minimum difference in degrees required between any two angles.
    :return: True if all angles are sufficiently different, False otherwise.
    """
    for i in range(len(angles)):
        for j in range(i + 1, len(angles)):
            angle_diff = abs(angles[i] - angles[j])
            # Adjust for angles crossing the 360-degree line
            angle_diff = min(angle_diff, 360 - angle_diff)
            if angle_diff < threshold:
                return False
    return True



if __name__=="__main__":
    angles = [30, 30, 270]  # Example list of angles
    if is_sufficiently_different(angles):
        print("Angles are sufficiently different.")
    else:
        print("Angles are not sufficiently different.")