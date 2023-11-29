from environment import *

# Initialization Code
pygame.init()

cases = {
    1: {"n_tigers": 2, "n_deers": 1, "n_steps": 50, "folder_name":'2t1d50'},
    2: {"n_tigers": 2, "n_deers": 1, "n_steps": 30, "folder_name":'2t1d30'},
    3: {"n_tigers": 2, "n_deers": 2, "n_steps": 50, "folder_name":'2t2d50'},
    4: {"n_tigers": 2, "n_deers": 2, "n_steps": 30, "folder_name":'2t2d30'}
}

train_cases={
    1: {'case_name':'only tiger',    'deer_epsilon':1, 'tiger_epsilon':0.4, 'folder_name':'ttud'},
    2: {'case_name':'only deer',     'deer_epsilon':0.4, 'tiger_epsilon':1,  'folder_name':'uttd'},
    3: {'case_name': 'both',        'deer_epsilon': 0.4,   'tiger_epsilon': 0.4,  'folder_name':'tttd'},
}

# Specify the case number
case = 1
train_case = 1

# Extract parameters based on the chosen case
n_tigers = cases[case]["n_tigers"]
n_deers = cases[case]["n_deers"]
n_steps = cases[case]["n_steps"]

# Train Cases
deer_epsilon = train_cases[train_case]['deer_epsilon']
tiger_epsilon = train_cases[train_case]['tiger_epsilon']
case_name = train_cases[train_case]['case_name']

folder_path = './'+ cases[case]["folder_name"] + '/' + train_cases[train_case]["folder_name"]
makedir(folder_path=folder_path)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Predator Prey RL")
clock = pygame.time.Clock()
ground = Background('ground.jpg', width=WIDTH, height=HEIGHT)

env = Env(ground=ground)
env.add(n_tigers, n_deers)

# Training
num_episodes = 2000
env.set_n_steps(n_steps)

env.set_deer_epsilon(deer_epsilon=deer_epsilon)
env.set_tiger_epsilon(tiger_epsilon=tiger_epsilon)
env.training(num_episodes, case=case_name)
env.save(tiger_q_file='tq.pkl', deer_q_file='dq.pkl', path=folder_path)
