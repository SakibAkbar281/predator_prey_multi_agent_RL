WIDTH, HEIGHT = 500, 500

# Cases
GAME_CASES = {
    '2tiger1deer50steps': {"n_tigers": 2, "n_deers": 1, "n_steps": 50, "folder_name":'2t1d50'},
    '2tiger1deer30steps': {"n_tigers": 2, "n_deers": 1, "n_steps": 30, "folder_name":'2t1d30'},
    '2tiger2deer50steps': {"n_tigers": 2, "n_deers": 2, "n_steps": 50, "folder_name":'2t2d50'},
    '2tiger2deer30steps': {"n_tigers": 2, "n_deers": 2, "n_steps": 30, "folder_name":'2t2d30'}
}

TRAIN_CASES={
    'only_tiger': {'case_name':'only tiger',    'deer_epsilon':1, 'tiger_epsilon':0.4, 'folder_name':'ttud'},
    'only_deer': {'case_name':'only deer',     'deer_epsilon':0.4, 'tiger_epsilon':1,  'folder_name':'uttd'},
    'both': {'case_name': 'both',        'deer_epsilon': 0.4,   'tiger_epsilon': 0.4,  'folder_name':'tttd'},
    'none': {'case_name': 'none',        'deer_epsilon': 1,   'tiger_epsilon': 1,  'folder_name':'utud'},
}

SIM_CASES = TRAIN_CASES.copy()
SIM_CASES['only_tiger']['tiger_epsilon']=0.01
SIM_CASES['only_deer']['deer_epsilon']=0.01
SIM_CASES['both']['tiger_epsilon']=0.01
SIM_CASES['both']['deer_epsilon']=0.01

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