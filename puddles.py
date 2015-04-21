"""
Puddle Class and associated group.
Handles the water for the bugs.
"""

import pygame
import random

class Puddle(pygame.sprite.Sprite):
    """
    The food items.
    They spawn at a rate (either determined by the amount of food onscreen or a constant amount)
    They run away from bugs at a rate 
    inherited methods:
    .update (see below)
    .kill (removes from all groups)
    .alive  (checks to see if belonging to any groups)
    """

    def __init__(self, x, y, window):
        pygame.sprite.Sprite.__init__(self, window.model.puddlelist)
        #self.image = window.food
        #self.rect = self.image.get_rect()
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
        reduces depth of puddle because a bug drank from it
        """
        if self.depth > 1: 
            self.depth -= 1
            self.width = self.depth*15
            self.height = self.depth*8
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        else: 
            self.kill()


    #def rain(self, window):
    #    """
    #    adds more puddles at regular intervals
    #    """
    #    if len(window.model.puddlelist) < 20:
    #        if random.random() < 0.005:
    #            Puddle(random.randint(0, window.view.width - 60), random.randint(50, window.view.height), window)


    def update(self, window):
        self.flee(window)
        self.run(window)

class PuddleList(pygame.sprite.Group):    
    """
    all inherited
    """
