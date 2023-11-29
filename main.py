from environment import *

# Initialization Code
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multi-agent RL Predator Prey")
clock = pygame.time.Clock()
# Background
ground = Background('ground.jpg', width=WIDTH, height=HEIGHT)

# Creating agents
n_tigers = 2
n_deers = 2
env = Env(ground=ground)
env.add(n_tigers, n_deers)

# Training
num_episodes = 5000
num_steps = N_STEPS
# env.load(tiger_q_file='tiger_q.pkl',deer_q_file='deer_q.pkl')
env.load(tiger_q_file='tiger_q_trained.pkl', deer_q_file='deer_q_untrained.pkl')
# env.training(num_episodes, num_steps, deer_epsilon=1, tiger_epsilon=0.01)
# env.save(tiger_q_file='tiger_q_trained.pkl', deer_q_file='deer_q_untrained.pkl')
tiger_wr, deer_wr = env.simulate(num_games=10_000)
print(f'final winning ratio: {tiger_wr} : {deer_wr}')
env.update_epsilon(deer_epsilon=1, tiger_epsilon=0)
env.run_game(screen, fps=10)
