import random
from pygame.math import Vector2
from config import *
from utils import *


class Agent(pygame.sprite.Sprite):
    def __init__(self, image_path, width, height, ground):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.size = Vector2(width, height)
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()
        self.pos = Vector2(0, 0)
        self.speed = 1
        self.allowable_actions = [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1)]
        self.action_indices = range(len(self.allowable_actions))
        self.Q = {(-1, -1): 0}
        self.prev_state = -1
        self.prev_action_idx = -1
        self.alpha = 0.7
        self.gamma = GAMMA
        self.epsilon = 0.05  # when trained
        self.reward = 0
        self.ground = ground

    def set_Q(self, Q):
        self.Q.update(Q)

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
        result = (not self.ground.rect.contains(rect)) \
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

    def choose(self, state, reward):
        for index_action, action in enumerate(self.allowable_actions):
            if (state, index_action) not in self.Q:
                self.Q[state, index_action] = random.random() * 0.00001

        best_reward = max(self.Q[state, idx] for idx in self.action_indices)
        self.Q[self.prev_state, self.prev_action_idx] += self.alpha * (
                reward + self.gamma * best_reward - self.Q[self.prev_state, self.prev_action_idx])

        action_idx = ((max(self.action_indices, key=lambda idx: self.Q[state, idx]))
                      if random.random() > self.epsilon
                      else random.choice(self.action_indices))

        self.prev_state = state
        self.prev_action_idx = action_idx
        action = self.allowable_actions[action_idx]
        return action

    def choose_without_learning(self, state):

        if self.is_state_in_Q(state):
            action_idx = ((max(self.action_indices, key=lambda idx: self.Q[state, idx]))
                          if random.random() > self.epsilon
                          else random.choice(self.action_indices))
        else:
            action_idx = random.choice(self.action_indices)

        action = self.allowable_actions[action_idx]
        return action

    def get_distance(self, other):
        x_1, y_1 = self.rect.center
        x_2, y_2 = other.rect.center
        x_diff = x_1 - x_2
        y_diff = y_1 - y_2
        return math.sqrt(x_diff ** 2 + y_diff ** 2)

    def is_close(self, other):
        result = self.get_distance(other) <= CAPTURE_RADIUS
        return result

    def is_state_in_Q(self, state_to_check):
        for (state, action) in self.Q.keys():
            if state == state_to_check:
                return True
        return False


class Tiger(Agent):
    def __init__(self, ground):
        super().__init__('tiger.png', width=100, height=100, ground=ground)
        self.speed = 100
        self.allowable_actions = [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1)]
        self.action_indices = range(len(self.allowable_actions))
        self.alpha = ALPHA_TIGER

class Deer(Agent):
    def __init__(self, ground):
        super().__init__('deer.png', width=100, height=100, ground=ground)
        self.speed = 100
        self.allowable_actions = [Vector2(1, 0), Vector2(-1, 0),
                                  Vector2(0, 1), Vector2(0, -1)]
        # self.allowable_actions = [Vector2(1, 0), Vector2(-1, 0),
        #                           Vector2(0, 1), Vector2(0, -1),
        #                           Vector2(1, 1), Vector2(-1, -1),
        #                           Vector2(1, -1), Vector2(-1, 1),
        #                           Vector2(2, 0), Vector2(-2, 0),
        #                           Vector2(0, 2), Vector2(0, -2),
        #                           Vector2(2, 2), Vector2(-2, -2),
        #                           Vector2(2, -2), Vector2(-2, 2)
        #                           ]
        self.action_indices = range(len(self.allowable_actions))
        self.got_caught = False
        self.alpha = ALPHA_DEER
        self.prev_closest_tiger_distance = -1

    def check_captured(self, tiger_group):
        n_close_tigers = 0
        for tiger in tiger_group:
            if self.is_close(tiger):
                n_close_tigers += 1

        return n_close_tigers >= 2

    def is_close_to_be_captured(self, tiger_group):
        n_close_tigers = 0
        for tiger in tiger_group:
            if self.get_distance(tiger) <= 250:
                n_close_tigers += 1

        return n_close_tigers >= 2


class TigerGroup(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def is_coordinated(self, deer_group):

        for deer in deer_group:
            # Calculate angles or positions relative to the deer for each tiger
            # Example: Check if tigers are approaching from different angles
            angles = []
            for tiger in self.sprites():
                angle = calculate_angle(tiger, deer)  # Define this function
                angles.append(angle)
            # print(angles)
            # Check if the angles are sufficiently different (e.g., more than 90 degrees apart)
            if not is_sufficiently_different(angles):  # Define this function
                return False
        return True

    def is_well_spaced(self):
        optimal_min_distance = MINIMUM_PREDATOR_DISTANCE  # Minimum optimal distance
        optimal_max_distance = MAXIMUM_PREDATOR_DISTANCE  # Maximum optimal distance

        for tiger1 in self.sprites():
            for tiger2 in self.sprites():
                if tiger1 != tiger2:
                    distance = tiger1.get_distance(tiger2)
                    if distance > optimal_max_distance:  # or distance < optimal_min_distance
                        return False
        return True


class DeerGroup(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)
