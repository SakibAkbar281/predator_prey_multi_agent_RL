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
n_deers = 1
n_steps = 30

env = Env(ground=ground)
env.add(n_tigers, n_deers)
env.set_n_steps(n_steps)
train_path = get_train_path(game_case='2tiger1deer50steps',train_case='only_tiger')
env.load(tiger_q_file='tq.pkl', deer_q_file='dq.pkl', path=train_path)
env.set_deer_epsilon(1)
env.set_tiger_epsilon(0)
env.run_game(screen, fps=1)
