from environment import *

# Initialization Code
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Predator Prey RL")
clock = pygame.time.Clock()
# Background
ground = Background('ground.jpg', width=WIDTH, height=HEIGHT)

# Creating agents
n_tigers = 2
n_deers = 2
env = Env(ground=ground)
env.add(n_tigers, n_deers)

# Simulation
env.load(tiger_q_file='tiger_q_trained.pkl', deer_q_file='deer_q_untrained.pkl')
tiger_wr, deer_wr = env.simulate(num_games=10_000)
print(f'final winning ratio: {tiger_wr} : {deer_wr}')
env.update_epsilon(deer_epsilon=1, tiger_epsilon=0)
env.run_game(screen, fps=10)
