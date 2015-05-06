"""
Puddle Class and associated group.
Handles the water for the bugs.
"""

import pygame
import random


class Puddle(pygame.sprite.Sprite):
    """
    The blue rectangles of water.
    inherited methods:
    .update (redefined, see below)
    .kill (removes from all groups)
    """

    def __init__(self, x, y, window):
        """
        inherits draw and grouping methods from pygame sprite parent class
        initializes position and stats
        determines possible size of puddle based on environment's wetness
        """
        pygame.sprite.Sprite.__init__(self, window.model.puddlelist)
        self.x = x
        self.y = y
        if window.model.wet > 200:
            self.depth = random.randint(1,4)
        elif window.model.wet < 50:
            self.depth = random.randint(1,2)
        else:
            self.depth = random.randint(1,3)
        self.width = self.depth*15
        self.height = self.depth*8
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        """
        draws puddle
        """
        pygame.draw.rect(window.view.screen, (0, 0, 255), self.rect)

    def get_drunk(self):
        """
        reduces depth/size of puddle because a bug drank from it
        """
        if self.depth > 1: 
            self.depth -= 1
            self.width = self.depth*15
            self.height = self.depth*8
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        else: 
            self.kill()

    def update(self, window):
        """
        calls methods in the proper order
        """
        self.flee(window)
        self.run(window)


class PuddleList(pygame.sprite.Group):
    """
    group list of all existing puddles
    all methods inherited from pygame sprite group parent class
    """
