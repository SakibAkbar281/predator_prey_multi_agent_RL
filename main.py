import random
import pygame
from pygame.math import Vector2
from sys import exit


# Initialization Code
pygame.init()
WIDTH ,HEIGHT = 612, 612


# Constants
N_STEPS = 2000
PREDATOR_COST_PER_MOVE = -2
PREY_REWARD_SURVIVAL = 10
PREY_REWARD_MOVE = 1
PREY_COST_CAPTURED = -10
PREDATOR_REWARD_CAPTURE = 10

# Scores
tiger_score = 0
deer_score = 0
steps = 0

# Sprite groups
all_sprites = pygame.sprite.Group()
tiger_group = pygame.sprite.Group()
deer_group = pygame.sprite.Group()

# Other global variables
clock = pygame.time.Clock()

# Classes

class Env:
    def __init__(self, tigers, deers, all_sprites):
        self.tigers = tigers
        self.deers = deers
        self.all_sprites = all_sprites
    def transition(self):
        state = self.get_state()
        tiger_rewards, deer_rewards = self.reward_of()
        for tiger_index, tiger in enumerate(self.tigers):
            tiger_move = tiger.choose(state, tiger_rewards[tiger_index])
            tiger.update(tiger_move, all_sprites)
        for deer_index, deer in enumerate(self.deers):
            deer_move = deer.choose(state, deer_rewards[deer_index])
            deer.update(deer_move, all_sprites)
            if deer.check_surrounded(self.tigers):
                deer.kill()

        # for tiger in self.tigers:
        #     action = tiger.decide_action() # todo
        #     tiger.move(action) # todo
        #     tiger.update_rewards() #todo
        # for deer in self.deers:
        #     action = deer.decide_action() # todo
        #     deer.move(action) # todo
        #     deer.update_rewards() #todo
        #
        # self.check_captures_and_assign_rewards()
    # def check_captures_and_assign_rewards(self):
    #     pass
    def reward_of(self):
        tiger_rewards = []
        deer_rewards = []
        for tiger in self.tigers:
            tiger.reward = PREDATOR_COST_PER_MOVE

        for deer in self.deers:
            deer.reward = PREY_REWARD_MOVE
            if deer.check_surrounded(self.tigers):
                deer.reward += PREY_COST_CAPTURED
                for tiger in pygame.sprite.spritecollide(deer, self.tigers, False):
                    tiger.reward += PREDATOR_REWARD_CAPTURE
                # deer.kill()

        for tiger in self.tigers:
            tiger_rewards.append(tiger.reward)
        for deer in self.deers:
            deer_rewards.append(deer.reward)

        return tiger_rewards, deer_rewards
    def get_state(self):
        sprite_positions = tuple([tuple(sprite.pos) for sprite in self.all_sprites])
        return hash(sprite_positions)

class Background:
    def __init__(self, image_path, width, height):
        self.original_image = pygame.image.load(image_path).convert()
        self.size = Vector2(width, height)
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()

    def __call__(self):
        return self.image


class Agent(pygame.sprite.Sprite):
    def __init__(self, image_path, width, height):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.size = Vector2(width, height)
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()
        self.pos = Vector2(0, 0)
        self.speed = 1
        self.allowable_actions = [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1)]
        self.action_indices = range(len(self.allowable_actions))
        self.Q = {(-1, -1) : 0}
        self.prev_state = -1
        self.prev_action_idx = -1
        self.alpha = 0.7
        self.gamma = 0.618
        self.epsilon = 0.05 # todo: change epsilon value based of episode
        self.reward =0

    def set_pos(self, pos: tuple):
        self.pos = Vector2(pos)
        self.rect.center = self.pos

    def update(self, displacement, all_sprites):
        # Calculate the next position
        next_rect = self.get_next_rect(displacement)

        if self.is_obstructed(next_rect, all_sprites):
            return
        self.move(displacement)

    def is_obstructed(self, rect, all_sprites):
        result = (not is_within_boundaries(rect)) \
                 or any(
            sprite != self and sprite.rect.colliderect(rect) for sprite in all_sprites)  # Collision with other sprites
        return result

    def move(self, displacement):
        self.pos += self.speed * displacement
        self.rect.center = self.pos

    def get_next_rect(self, displacement):
        next_pos = self.pos + self.speed * displacement
        next_rect = self.rect.copy()
        next_rect.center = next_pos
        return next_rect

    def check_surrounded(self, other_group):
        # Check if this agent is surrounded by agents from the other group
        return len(pygame.sprite.spritecollide(self, other_group, False)) >= 2
    def choose(self, state, reward):
        for index_action, action in enumerate(self.allowable_actions):
            if (state,index_action) not in self.Q:
                self.Q[state,index_action] = random.random() * 0.00001

        best_reward = max(self.Q[state,idx] for idx in self.action_indices)
        self.Q[self.prev_state,self.prev_action_idx] += self.alpha * (reward + self.gamma * best_reward - self.Q[self.prev_state,self.prev_action_idx])

        action_idx = ((max(self.action_indices, key= lambda idx: self.Q[state, idx]))
                      if random.random() > self.epsilon
                      else random.choice(self.action_indices))

        self.prev_state = state
        self.prev_action_idx = action_idx
        action = self.allowable_actions[action_idx]
        return action


class Tiger(Agent):
    def __init__(self):
        super().__init__('tiger.png', width=100, height=100)
        self.speed = 20
        self.allowable_actions = [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1)]
        self.action_indices = range(len(self.allowable_actions))
    def get_reward(self):
        pass #todo


class Deer(Agent):
    def __init__(self):
        super().__init__('deer.png', width=100, height=100)
        self.speed = 40
        self.allowable_actions = [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1),
                                  Vector2(1, 1), Vector2(-1, -1), Vector2(1, -1), Vector2(-1, 1)]
        self.action_indices = range(len(self.allowable_actions))

    def get_reward(self):
        pass #todo



class Text:
    def __init__(self, text, font_path=None, font_size=50, color='black', AA=False):
        font = pygame.font.Font(font_path, font_size)
        self.image = font.render(text, AA, color)
        self.rect = self.image.get_rect()
    def __call__(self):
        return self.image

    def get_size(self):
        return Vector2(self.image.get_size())
    def center_of(self, other_rect):
        self.rect.center = other_rect.center
        return self.rect



# Functions
def create_agents(agent_class, count, offset_from_center, all_sprites, specific_group):
    agents = []
    for _ in range(count):
        agent = agent_class()
        while True:
            init_pos = ground.rect.center + Vector2(random.randint(-offset_from_center, offset_from_center),
                                                    random.randint(-offset_from_center, offset_from_center))
            agent.set_pos(init_pos)
            if not agent.is_obstructed(agent.rect, all_sprites):
                break

        all_sprites.add(agent)
        specific_group.add(agent)
        agents.append(agent)
    return agents


# Background
ground = Background('ground.jpg', width=WIDTH, height=HEIGHT)


def is_within_boundaries(rect):
    return ground.rect.contains(rect)




# Creating agents
n_tigers = 3
n_deers = 3
tigers = create_agents(Tiger, n_tigers, offset_from_center=300, all_sprites=all_sprites, specific_group=tiger_group)
deers = create_agents(Deer, n_deers, offset_from_center=400, all_sprites=all_sprites, specific_group=deer_group)

prey_win_text = Text("Preys win")
predator_win_text = Text("Predators win")
env = Env(tiger_group,deer_group,all_sprites)

# Training
num_episodes = 1000_0000
# num_steps = 2
for episode in range(num_episodes):
    # for steps in range(num_steps):
    env.transition()
    if episode % 100 ==0:
        print(f'Completed {episode}/ {num_episodes}')

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Predator Prey RL")
# Training is finished
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.blit(ground(), dest=(0, 0))

    score_tigers = Text(f'Tiger Score: {tiger_score}')
    score_deers = Text(f'Deer Score: {deer_score}')
    steps_text = Text(f"Steps: {steps}")
    screen.blit(score_tigers(), dest=(10, 10))
    screen.blit(score_deers(), dest=(10, 50))
    screen.blit(steps_text(), dest=(WIDTH-steps_text.get_size().x-10, 10))
    env.transition()

    all_sprites.draw(screen)  # Draw all sprites

    # Check for game end conditions
    steps += 1
    if len(deer_group) == 0 or steps >= N_STEPS:
        if len(deer_group) == 0:
            screen.blit(predator_win_text(), dest=predator_win_text.center_of(ground.rect))
        else:
            deer_score += len(deer_group) * PREY_REWARD_SURVIVAL
            screen.blit(prey_win_text(), dest=prey_win_text.center_of(ground.rect))
        pygame.display.update()
        pygame.time.delay(5000)
        pygame.quit()
        exit()

    pygame.display.update()
    clock.tick(10)
