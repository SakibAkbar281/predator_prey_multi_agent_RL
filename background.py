import pygame
from pygame.math import Vector2

class Background:
    def __init__(self, image_path, width, height):
        self.original_image = pygame.image.load(image_path).convert()
        self.size = Vector2(width, height)
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()

    def __call__(self):
        return self.image


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

