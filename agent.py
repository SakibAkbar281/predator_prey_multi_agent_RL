import random
import pygame
from pygame.math import Vector2
import math
from config import *
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
        self.gamma = 0.618
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

    def get_distance(self, other):
        x_1, y_1 = self.rect.center
        x_2, y_2 = other.rect.center
        x_diff = x_1 - x_2
        y_diff = y_1 - y_2
        return math.sqrt(x_diff ** 2 + y_diff ** 2)

    def is_close(self, other):
        result = self.get_distance(other) <= CAPTURE_RADIUS
        return result

class Tiger(Agent):
    def __init__(self,ground):
        super().__init__('tiger.png', width=100, height=100,ground=ground)
        self.speed = 100
        self.allowable_actions = [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1)]
        self.action_indices = range(len(self.allowable_actions))

class Deer(Agent):
    def __init__(self,ground):
        super().__init__('deer.png', width=100, height=100,ground=ground)
        self.speed = 200
        self.allowable_actions = [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1),
                                  Vector2(1, 1), Vector2(-1, -1), Vector2(1, -1), Vector2(-1, 1)]
        self.action_indices = range(len(self.allowable_actions))
        self.got_caught = False
    def check_captured(self, tiger_group):
        n_close_tigers = 0
        for tiger in tiger_group:
            if self.is_close(tiger):
                n_close_tigers += 1
        # if n_close_tigers >= 2:
        #     self.got_caught = True
        return n_close_tigers >= 2
