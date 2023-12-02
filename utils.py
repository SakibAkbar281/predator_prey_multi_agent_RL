import math
import os
import pygame
import pickle
from config import *
import numpy as np
import re
from cases import *
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

def list_folders_in_directory(directory_path):
    # List all the folders in the specified directory
    return [item for item in os.listdir(directory_path)
            if os.path.isdir(os.path.join(directory_path, item))]

def extract_numbers(s):
    return tuple(map(int, re.findall(r'\d+', s)))

def get_all_trained_cases(data_path='./data/'):
    game_case_folders = list_folders_in_directory(data_path)
    game_cases= []
    for game_case_folder in game_case_folders:
        n_tigers, n_deers, n_steps = extract_numbers(game_case_folder)
        game_case_path = os.path.join(data_path, game_case_folder)
        train_case_folders = list_folders_in_directory(game_case_path)
        cases =[]
        for train_case_folder in train_case_folders:
            train_tiger, train_deer = extract_numbers(train_case_folder)
            train_tiger = bool(train_tiger)
            train_deer = bool(train_deer)
            train_case_path = os.path.join(game_case_path, train_case_folder)
            case = Case(n_tigers, n_deers, n_steps, train_tiger, train_deer)
            cases.append(case)
            # if train_tiger or train_deer:
            #     case = Case(n_tigers, n_deers, n_steps, train_tiger, train_deer)
            #     train_cases.append(case)
            # else:
            #     case = Case(n_tigers, n_deers, n_steps, train_tiger, train_deer)
            #     base_cases.append(case)
        game_cases.append(cases)
    return game_cases

def get_base_cases(game_cases):
    base_cases = []
    for train_cases in game_cases:
        for train_case in train_cases:
            if train_case.is_base_case():
                base_cases.append(train_case)
    return base_cases



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

def get_moving_avg_and_std_error(hist):
    cumulative_wins = np.array(hist['tiger_wins'])
    incremental_wins = np.diff(cumulative_wins, prepend=0)

    # Define the window size for the moving average (e.g., last 100 games)
    window_size = 100

    # Calculate the moving average of the winning probability for the last `window_size` games
    # Ensure the window does not go out of bounds
    start_index = max(0, len(incremental_wins) - window_size)
    end_index = len(incremental_wins)
    windowed_wins = incremental_wins[start_index:end_index]
    moving_avg_win_prob = np.mean(windowed_wins)

    # Calculate standard error for the moving average
    # Use the standard deviation of the windowed wins and divide by the square root of the window size
    standard_error = np.std(windowed_wins) / np.sqrt(window_size)
    return moving_avg_win_prob, standard_error


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