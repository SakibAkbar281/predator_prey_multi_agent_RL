
from sys import exit
from background import *
from environment import *


# Initialization Code
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Predator Prey RL")

# Background
ground = Background('ground.jpg', width=WIDTH, height=HEIGHT)

# Time
clock = pygame.time.Clock()

# Creating agents
n_tigers = 2
n_deers = 2
env = Env(ground=ground)
env.add(n_tigers, n_deers)
env.load(tiger_q_file='tiger_q.pkl',deer_q_file='deer_q.pkl')

# Texts
deer_win_text = Text("Deer win")
tiger_win_text = Text("Tigers win")

# Training
num_episodes = 100
num_steps = N_STEPS

env.training(num_episodes, num_steps)
env.save()
tiger_scores = 0
deer_scores = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.blit(ground(), dest=(0, 0))
    tiger_reward_list, deer_reward_list = env.transition()
    # print(tiger_reward_list, deer_reward_list)
    tiger_scores += sum(tiger_reward_list)
    deer_scores += sum(deer_reward_list)

    score_tigers = Text(f'Tiger Score: {tiger_scores}')
    score_deers = Text(f'Deer Score: {deer_scores}')
    steps_text = Text(f"Steps: {env.steps}")
    screen.blit(score_tigers(), dest=(10, 10))
    screen.blit(score_deers(), dest=(10, 50))
    screen.blit(steps_text(), dest=(WIDTH - steps_text.get_size().x - 10, 10))

    env.all_sprites.draw(screen)  # Draw all sprites

    # Check for game end conditions
    if env.game_over():
        if env.tiger_wins():
            screen.blit(tiger_win_text(), dest=tiger_win_text.center_of(ground.rect))
        else:
            screen.blit(deer_win_text(), dest=deer_win_text.center_of(ground.rect))
        pygame.display.update()
        pygame.time.delay(5000)
        pygame.quit()
        exit()

    pygame.display.update()
    clock.tick(1)
