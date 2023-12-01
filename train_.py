from environment import *
from cases import *
import itertools


def run_simulation(case, num_episodes):
    pygame.init()

    makedir(folder_path=case.path)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Predator Prey RL")
    ground = Background('ground.jpg', width=WIDTH, height=HEIGHT)

    env = Env(ground=ground)
    env.add(case.n_tigers, case.n_deers)

    # Training setup
    env.set_n_steps(case.n_steps)
    env.tiger_not_learning = not case.train_tiger
    env.deer_not_learning = not case.train_deer
    env.set_deer_epsilon(deer_epsilon=case.deer_epsilon)
    env.set_tiger_epsilon(tiger_epsilon=case.tiger_epsilon)

    # Training
    env.training(num_episodes, train_condition=case.train_condition, path=case.path)
    env.save(path=case.path)
    env.set_deer_epsilon(deer_epsilon=0.001)
    env.set_tiger_epsilon(tiger_epsilon=0.001)
    env.load(path=case.path)


# case = Case(n_tigers=2,
#             n_deers=1,
#             n_steps=23,
#             train_tiger=False,
#             train_deer=False)
# print(case)
# run_simulation(case, num_episodes=10_000)

cases = [(2, 1, 23, True, True),
         (2, 1, 23, True, False),
         (2, 1, 23, False, True),
         (2, 1, 23, False, False),
         (2, 2, 40, True, True),
         (2, 2, 40, True, False),
         (2, 2, 40, False, True),
         (2, 2, 40, False, False),
         (2, 2, 10, True, True),
         (2, 2, 10, True, False),
         (2, 2, 10, False, True),
         (2, 2, 10, False, False)
         ]

for case_tuple in cases:
    case = Case(*case_tuple)
    print(case)
    run_simulation(case, num_episodes=100)
