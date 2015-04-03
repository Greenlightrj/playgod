"""
Noms Class and associated group.
Handles the food for the bugs.
"""

import pygame
import random
from math import sin, cos, hypot, atan2

class Nom(pygame.sprite.Sprite):
    """The food items.
    inherited methods:
    .update (see below)
    .kill (removes from all groups)
    .alive  (checks to see if belonging to any groups)"""

    def __init__(self, x, y, window):
        pygame.sprite.Sprite.__init__(self, window.model.food)  #puts human in list of humans
        #self.image = window.food
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.angle = random.randint(-314, 314)
        self.speed = random.random()
        self.xspeed = 1
        self.yspeed = 1

    def draw(self, window):
        pygame.draw.rect(window.view.screen, [0, 250, 0], [self.x, self.y, 5, 5])

    def flee(self, window):
        """
        humans run from nearest adult dinosaur
        """
        if len(window.model.bugs.sprites()) > 0:     #if there are any dinos
            dist = 1000000
            for bug in window.model.bugs:
                if hypot(bug.x - self.x, bug.y - self.y) < dist:
                    dist = hypot(bug.x - self.x, bug.y - self.y)
                    nearest = bug
            self.angle = 100*atan2(self.y - nearest.y, self.x - nearest.x)


    def run(self, window):
        """
        humans walk around randomly if there are no dinos
        humans can escape via the edges
        """
        if self.x > window.view.width:
            self.kill()
        elif self.x < 1:
            self.kill()
        if self.y < 1:
            self.kill()
        elif self.y > window.view.height:
            self.kill()
        self.yspeed = sin(self.angle/100.0)*self.speed  # update speed
        self.xspeed = cos(self.angle/100.0)*self.speed  # update speed
        self.x = self.x + self.xspeed
        self.y = self.y + self.yspeed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)


    def update(self, window):
        self.flee(window)
        self.run(window)

class NomList(pygame.sprite.Group):    
    """
    all inherited
    """