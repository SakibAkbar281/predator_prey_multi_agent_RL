from environment import *
from cases import *
import itertools


def run_simulation(case):
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
    env.load(path=case.path)
    env.training(case.num_episodes, train_condition=case.train_condition, path=case.path)
    env.save(path=case.path)


# n_t, n_d, n_s, tt, td, neps
# cases = [(2, 1, 23, True, True, 10_000),
#          (2, 1, 23, True, False, 10_000),
#          (2, 1, 23, False, True, 10_000),
#          (2, 1, 23, False, False, 5_000),
#          (2, 2, 40, True, True, 20_000),
#          (2, 2, 40, True, False, 20_000),
#          (2, 2, 40, False, True, 20_000),
#          (2, 2, 40, False, False, 5_000)]
#
# cases = [(2, 2, 40, True, True, 10_000),
#          (2, 2, 40, True, False, 20_000),
#          (2, 2, 40, False, True, 20_000),
#          (2, 2, 40, False, False, 5_000)]
# cases = [(2, 1, 23, False, False, 100),
#          (2, 1, 23, True, False, 100),
#          (2, 1, 23, False, True, 100),
#          (2, 1, 23, True, True, 100)]

# cases = [(2, 1, 23, False, False, 100000),
#          (2, 2, 40, False, False, 100000)]

cases = [(2, 1, 23, False, True, 10_000)]

for case_tuple in cases:
    case = Case(*case_tuple)
    print(case)
    run_simulation(case)
