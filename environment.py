"""
environment classes
"""

import pygame

class Nature(pygame.sprite.Sprite):
    """
    base class for all environment objects
    """
    def __init__(self, x, y, window):
        pygame.sprite.Sprite.__init__(self, window.model.environ)
        self.x = x
        self.y = y
        self.image = pygame.image.load("Images/genericgrass.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def effect(self, window):
        pass

class DesertDune(Nature):
    """
    Desert sand dune object
    in the future, will make the environment hotter and drier?
    """
    def __init__(self, x, y, window):
        Nature.__init__(self, x, y, window)
        self.image = pygame.image.load("Images/desertdune.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def effect(self, window):
        if window.model.heat < 255:
            window.model.heat += 0.01
        if window.model.wet > 0:
            window.model.wet -= 0.01

class RainforestTree(Nature):
    """
    Rainforest Tree object
    in the future, will make the environment hotter and wetter?
    """
    def __init__(self, x, y, window):
        Nature.__init__(self, x, y, window)
        self.image = pygame.image.load("Images/rainforesttree.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def effect(self, window):
        if window.model.green < 255:
            window.model.green += 0.01
        if window.model.wet < 255:
            window.model.wet += 0.01


class DesertPalmTree(Nature):
    """
    Desert palm tree object
    in the future, will make the environment hotter and drier?
    """
    def __init__(self, x, y, window):
        Nature.__init__(self, x, y, window)
        self.image = pygame.image.load("Images/desertpalmtree.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def effect(self, window):
        if window.model.heat < 255:
            window.model.heat += 0.01
        if window.model.wet > 0:
            window.model.wet -= 0.01


class DesertHill(Nature):
    """
    Desert hill object
    in the future, will make the environment hotter and drier?
    """
    def __init__(self, x, y, window):
        Nature.__init__(self, x, y, window)
        self.image = pygame.image.load("Images/deserthill.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def effect(self, window):
        if window.model.heat < 255:
            window.model.heat += 0.01
        if window.model.wet > 0:
            window.model.wet -= 0.01


class ArcticDesertDune(Nature):
    """
    Arctic Desert dune object
    will make the environment colder and drier?
    """
    def __init__(self, x, y, window):
        Nature.__init__(self, x, y, window)
        self.image = pygame.image.load("Images/arcticdune.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def effect(self, window):
        if window.model.heat > 0:
            window.model.heat -= 0.01
        if window.model.wet > 0:
            window.model.wet -= 0.01


class Environ(pygame.sprite.Group):
    """
    list of all environment objects
    """

