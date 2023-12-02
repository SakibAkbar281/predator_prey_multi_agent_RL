from environment import *

# Initialization Code
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multi-agent RL Predator Prey")
ground = Background('ground.jpg', width=WIDTH, height=HEIGHT)

case = Case(n_tigers=2,
            n_deers=1,
            n_steps=23,
            train_tiger=True,
            train_deer=False)
env = Env(ground=ground)
env.add(case.n_tigers, case.n_deers)
env.set_n_steps(case.n_steps)
env.load(path=case.path)
env.set_tiger_epsilon(0.01 if case.train_tiger else 1.0)
env.set_deer_epsilon(0.01 if case.train_deer else 1.0)
env.run_game(screen, fps=1)
