import random
import pygame
from pygame.math import Vector2
from sys import exit


# Initialization Code
pygame.init()
WIDTH ,HEIGHT = 612, 612
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Predator Prey RL")

# Constants
N_STEPS = 20
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
    def __init__(self, tigers, deers):
        self.tigers = tigers
        self.deers = deers
    def transition(self):
        for tiger in self.tigers:
            action = tiger.decide_action() # todo
            tiger.move(action) # todo
            tiger.update_rewards() #todo
        for deer in self.deers:
            action = deer.decide_action() # todo
            deer.move(action) # todo
            deer.update_rewards() #todo

        self.check_captures_and_assign_rewards()
    def check_captures_and_assign_rewards(self):
        pass

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


class Tiger(Agent):
    def __init__(self):
        super().__init__('tiger.png', width=100, height=100)
        self.speed = 20
        self.allowable_actions = [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1)]
    def get_reward(self):
        pass #todo


class Deer(Agent):
    def __init__(self):
        super().__init__('deer.png', width=100, height=100)
        self.speed = 40
        self.allowable_actions = [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1),
                                  Vector2(1, 1), Vector2(-1, -1), Vector2(1, -1), Vector2(-1, 1)]

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

def is_within_boundaries(rect):
    return screen.get_rect().contains(rect)


# Background
ground = Background('ground.jpg', width=WIDTH, height=HEIGHT)

# Creating agents
n_tigers = 3
n_deers = 3
tigers = create_agents(Tiger, n_tigers, offset_from_center=300, all_sprites=all_sprites, specific_group=tiger_group)
deers = create_agents(Deer, n_deers, offset_from_center=400, all_sprites=all_sprites, specific_group=deer_group)

prey_win_text = Text("Preys win")
predator_win_text = Text("Predators win")

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

    # Update game state
    for tiger in tigers:
        tiger_move = random.choice(tiger.allowable_actions)
        tiger.update(tiger_move, all_sprites)
        tiger_score += PREDATOR_COST_PER_MOVE

    for deer in deers:
        deer_move = random.choice(deer.allowable_actions)
        deer.update(deer_move, all_sprites)
        deer_score += PREY_REWARD_MOVE
        if deer.check_surrounded(tiger_group):
            deer_score += PREY_COST_CAPTURED
            for tiger in pygame.sprite.spritecollide(deer, tiger_group, False):
                tiger_score += PREDATOR_REWARD_CAPTURE
            deer.kill()



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
    clock.tick(5)
