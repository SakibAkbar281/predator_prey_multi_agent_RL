from environment import *

# Initialization Code
pygame.init()

# Specify the game_case number
# game_case = '2tiger1deer50steps'
# train_case = 'both'

for game_case in ['2tiger1deer50steps']:
    for train_case in ['only_deer']:
        # Extract parameters based on the chosen game_case
        n_tigers = GAME_CASES[game_case]["n_tigers"]
        n_deers = GAME_CASES[game_case]["n_deers"]
        n_steps = GAME_CASES[game_case]["n_steps"]

        # Train Cases
        deer_epsilon = TRAIN_CASES[train_case]['deer_epsilon']
        tiger_epsilon = TRAIN_CASES[train_case]['tiger_epsilon']
        case_name = TRAIN_CASES[train_case]['case_name']

        folder_path = get_train_path(game_case,train_case)
        print(folder_path)
        makedir(folder_path=folder_path)


        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Predator Prey RL")
        clock = pygame.time.Clock()
        ground = Background('ground.jpg', width=WIDTH, height=HEIGHT)

        env = Env(ground=ground)
        env.add(n_tigers, n_deers)

        # Training
        num_episodes = 5000
        env.set_n_steps(n_steps)
        env.tiger_not_learning = not TRAIN_CASES[train_case]['train_tiger']
        env.deer_not_learning = not TRAIN_CASES[train_case]['train_deer']
        env.set_deer_epsilon(deer_epsilon=deer_epsilon)
        env.set_tiger_epsilon(tiger_epsilon=tiger_epsilon)
        env.training(num_episodes, train_condition=case_name, path=folder_path)
        env.save(tiger_q_file='tq.pkl', deer_q_file='dq.pkl', path=folder_path)
