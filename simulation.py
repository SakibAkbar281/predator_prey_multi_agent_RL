from environment import *


# Initialization Code
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Predator Prey RL")
clock = pygame.time.Clock()


# Background
ground = Background('ground.jpg', width=WIDTH, height=HEIGHT)
case = Case(2,1,23,True,False)
# Creating agents
env = Env(ground=ground)
env.add(case.n_tigers, case.n_deers)
env.set_n_steps(case.n_steps)
env.set_deer_epsilon(deer_epsilon=case.deer_epsilon)
env.set_tiger_epsilon(tiger_epsilon=case.tiger_epsilon)

# Simulation
env.load(path=case.path)
tiger_wr, deer_wr = env.simulate(num_games=5000)
print(f'final winning ratio: {tiger_wr} : {deer_wr}')
