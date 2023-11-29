from environment import *

# Initialization Code
pygame.init()


# Specify the case number
case = 1
sim_case = 1

# Extract parameters based on the chosen case
n_tigers = CASES[case]["n_tigers"]
n_deers = CASES[case]["n_deers"]
n_steps = CASES[case]["n_steps"]

# Train Cases
deer_epsilon = SIM_CASES[sim_case]['deer_epsilon']
tiger_epsilon = SIM_CASES[sim_case]['tiger_epsilon']
case_name = SIM_CASES[sim_case]['case_name']

folder_path = './' + CASES[case]["folder_name"] + '/' + SIM_CASES[sim_case]["folder_name"] + '/sim/'
folder_train_path = './' + CASES[case]["folder_name"] + '/' + SIM_CASES[sim_case]["folder_name"] + '/train/'
makedir(folder_path=folder_path)
makedir(folder_path=folder_train_path)



screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Predator Prey RL")
clock = pygame.time.Clock()


# Background
ground = Background('ground.jpg', width=WIDTH, height=HEIGHT)

# Creating agents
env = Env(ground=ground)
env.add(n_tigers, n_deers)
env.set_deer_epsilon(deer_epsilon=deer_epsilon)
env.set_tiger_epsilon(tiger_epsilon=tiger_epsilon)

# Simulation
env.load(tiger_q_file='tq.pkl', deer_q_file='dq.pkl', path=folder_train_path)
tiger_wr, deer_wr = env.simulate(num_games=10, path=folder_path)
print(f'final winning ratio: {tiger_wr} : {deer_wr}')
