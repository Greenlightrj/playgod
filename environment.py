"""
Classes for the environmental features
and associated group class
"""

import pygame


class Nature(pygame.sprite.Sprite):
    """
    base class for all environment objects
    """
    def __init__(self, x, y, window):
        """
        initializes position and sprite
        inherits draw method and group joining from pygame sprite parent class
        """
        pygame.sprite.Sprite.__init__(self, window.model.environ)
        self.x = x
        self.y = y
        self.image = pygame.image.load("Images/genericgrass.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def effect(self, window):
        """
        method for inheriting classes to modify
        determines the effect an environment object has on the environment
        """
        pass

class DesertDune(Nature):
    """
    Desert sand dune object
    """
    def __init__(self, x, y, window):
        """
        replaces the default image with the desert dune image
        """
        Nature.__init__(self, x, y, window)
        self.image = pygame.image.load("Images/desertdune.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def effect(self, window):
        """
        makes the enrivonment hotter and drier
        """
        if window.model.heat < 255:
            window.model.heat += 0.01
        if window.model.wet > 0:
            window.model.wet -= 0.01

class RainforestTree(Nature):
    """
    Rainforest Tree object
    """
    def __init__(self, x, y, window):
        """
        replaces the default image with the rainforest tree image
        """
        Nature.__init__(self, x, y, window)
        self.image = pygame.image.load("Images/rainforesttree.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def effect(self, window):
        """
        makes the environment friendlier and wetter
        """
        if window.model.green < 255:
            window.model.green += 0.01
        if window.model.wet < 255:
            window.model.wet += 0.01


class DesertPalmTree(Nature):
    """
    Desert palm tree object
    """
    def __init__(self, x, y, window):
        """
        replaces the default image with the desert palm tree image
        """
        Nature.__init__(self, x, y, window)
        self.image = pygame.image.load("Images/desertpalmtree.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def effect(self, window):
        """
        makes the environment hotter and wetter
        """
        if window.model.heat < 255:
            window.model.heat += 0.01
        if window.model.wet > 0:
            window.model.wet -= 0.01


class DesertHill(Nature):
    """
    Desert hill object
    """
    def __init__(self, x, y, window):
        """
        replaces the default image with the desert hill image
        """
        Nature.__init__(self, x, y, window)
        self.image = pygame.image.load("Images/deserthill.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def effect(self, window):
        """
        makes the environment hotter and drier
        """
        if window.model.heat < 255:
            window.model.heat += 0.01
        if window.model.wet > 0:
            window.model.wet -= 0.01


class ArcticDesertDune(Nature):
    """
    Arctic Desert dune object
    """
    def __init__(self, x, y, window):
        """
        replaces the default image with the arctic desert dune image
        """
        Nature.__init__(self, x, y, window)
        self.image = pygame.image.load("Images/arcticdune.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def effect(self, window):
        """
        makes the environment colder and drier
        """
        if window.model.heat > 0:
            window.model.heat -= 0.01
        if window.model.wet > 0:
            window.model.wet -= 0.01


class Environ(pygame.sprite.Group):
    """
    list of all environment objects
    """

