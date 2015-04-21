"""
Noms Class and associated group.
Handles the food for the bugs.
"""

import pygame
import random
from math import sin, cos, hypot, atan2

class Nom(pygame.sprite.Sprite):
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
        pygame.sprite.Sprite.__init__(self, window.model.nomlist)
        #self.image = window.food
        #self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.angle = random.randint(-314, 314)
        self.speed = random.random()*3
        self.xspeed = 1
        self.yspeed = 1
        self.toughness = 0.1*random.randint(0, 8)
        self.image = pygame.image.load("Images/fly.png")
        self.rect = self.image.get_rect()
        self.width = self.rect.size[0]
        self.height = self.rect.size[1]
        self.rect.x = x
        self.rect.y = y


    def flee(self, window):
        """
        prey runs from nearest bug
        """
        if len(window.model.buglist) > 0:     #if there are any bugs
            dist = 100
            nearest = 0
            for bug in window.model.buglist:
                if hypot(bug.x - self.x, bug.y - self.y) < dist:
                    if bug.sexiness > 0.2:
                        dist = 3*bug.sexiness*hypot(bug.x - self.x, bug.y - self.y)
                        nearest = bug
            if nearest:
                self.angle = 100*atan2(self.y - nearest.y, self.x - nearest.x)


    def run(self, window):
        """
        noms walk around randomly if there are no bugs
        noms wrap around the edges.
        """
        if self.x > window.view.width:
            self.x = 10
        elif self.x < 1:
            self.x = window.view.width-10
        if self.y < 50:
            self.y = window.view.height-10
        elif self.y > window.view.height:
            self.y = 60
        self.yspeed = sin(self.angle/100.0)*self.speed  # update speed
        self.xspeed = cos(self.angle/100.0)*self.speed  # update speed
        self.x = self.x + self.xspeed
        self.y = self.y + self.yspeed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    #def multiply(self, window):
    #    if len(window.model.nomlist) < 100:
    #        if random.random() < 0.005:
    #            Nom(random.randint(0, window.view.width), random.randint(0, window.view.height), window)


    def update(self, window):
        self.flee(window)
        self.run(window)

class NomList(pygame.sprite.Group):    
    """
    all inherited
    """
