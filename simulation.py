from environment import *


# Initialization Code
pygame.init()


# Specify the game_case number
game_case = '2tiger2deer30steps'
sim_case = 'none'

# Extract parameters based on the chosen game_case
n_tigers = GAME_CASES[game_case]["n_tigers"]
n_deers = GAME_CASES[game_case]["n_deers"]
n_steps = GAME_CASES[game_case]["n_steps"]

# Train Cases
deer_epsilon = SIM_CASES[sim_case]['deer_epsilon']
tiger_epsilon = SIM_CASES[sim_case]['tiger_epsilon']
case_name = SIM_CASES[sim_case]['case_name']

folder_path = get_sim_path(game_case,sim_case)
folder_train_path = get_train_path(game_case,sim_case)

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
env.set_n_steps(n_steps)
env.set_deer_epsilon(deer_epsilon=deer_epsilon)
env.set_tiger_epsilon(tiger_epsilon=tiger_epsilon)

# Simulation
# env.load(tiger_q_file='tq.pkl', deer_q_file='dq.pkl', path=folder_train_path)
tiger_wr, deer_wr = env.simulate(num_games=5000, path=folder_path)
print(f'final winning ratio: {tiger_wr} : {deer_wr}')
