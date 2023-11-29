WIDTH, HEIGHT = 500, 500

# Cases
CASES = {
    1: {"n_tigers": 2, "n_deers": 1, "n_steps": 50, "folder_name":'2t1d50'},
    2: {"n_tigers": 2, "n_deers": 1, "n_steps": 30, "folder_name":'2t1d30'},
    3: {"n_tigers": 2, "n_deers": 2, "n_steps": 50, "folder_name":'2t2d50'},
    4: {"n_tigers": 2, "n_deers": 2, "n_steps": 30, "folder_name":'2t2d30'}
}

TRAIN_CASES={
    1: {'case_name':'only tiger',    'deer_epsilon':1, 'tiger_epsilon':0.4, 'folder_name':'ttud'},
    2: {'case_name':'only deer',     'deer_epsilon':0.4, 'tiger_epsilon':1,  'folder_name':'uttd'},
    3: {'case_name': 'both',        'deer_epsilon': 0.4,   'tiger_epsilon': 0.4,  'folder_name':'tttd'},
    4: {'case_name': 'none',        'deer_epsilon': 1,   'tiger_epsilon': 1,  'folder_name':'utud'},
}

SIM_CASES = TRAIN_CASES.copy()
SIM_CASES[1]['tiger_epsilon']=0.01
SIM_CASES[2]['deer_epsilon']=0.01
SIM_CASES[3]['tiger_epsilon']=0.01
SIM_CASES[3]['deer_epsilon']=0.01

# Constants


PREDATOR_COST_PER_MOVE = -1
COORDINATION_BONUS = 10
NOT_COORDINATION_PENALTY = -20
TEAMWORK_BONUS = 10
PREY_REWARD_SURVIVAL = 10
PREY_REWARD_MOVE = 1
PREY_COST_CAPTURED = -11
PREDATOR_REWARD_CAPTURE = 11
CAPTURE_RADIUS = 150
MINIMUM_PREDATOR_DISTANCE = 100
MAXIMUM_PREDATOR_DISTANCE = 200