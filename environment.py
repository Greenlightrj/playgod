"""
environment classes
"""

import pygame


class DesertDune(pygame.sprite.Sprite):
    """
    Desert sand dune object
    in the future, will make the environment hotter and drier?
    """
    def __init__(self, x, y, window):
        pygame.sprite.Sprite.__init__(self, window.model.environ)
        self.x = x
        self.y = y
        self.image = pygame.image.load("desertdune.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class RainforestTree(pygame.sprite.Sprite):
    """
    Desert sand dune object
    in the future, will make the environment hotter and drier?
    """
    def __init__(self, x, y, window):
        pygame.sprite.Sprite.__init__(self, window.model.environ)
        self.x = x
        self.y = y
        self.image = pygame.image.load("rainforesttree.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Environ(pygame.sprite.Group):
    """
    list of all environment objects
    """

