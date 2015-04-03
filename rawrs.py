"""
Rawr class. 
Handles the predators of the bugs.
"""

import pygame
import random
from math import sin, cos, hypot, atan2

class Rawr(pygame.sprite.Sprite):
    """
    inherited methods:
    .update (see below)
    .kill (removes from all groups)
    .alive  (checks to see if belonging to any groups)
    """
    def __init__(self, x, y, window):
        """
        dinos start alive with 1 hunger
        """
        pygame.sprite.Sprite.__init__(self, window.model.predators) #puts dino in list of dinos
        #self.image = window.longneck
        #self.size= self.image.get_rect().size[1]
        #self.rect = self.image.get_rect()
        self.x = x  #actual position, can be float
        self.y = y
        self.rect.x = x     #integer position for drawing
        self.rect.y = y
        #self.living = True
        self.hunger = 1
        #self.health = window.view.dkgrn
        self.angle = random.randrange(-314, 314)
        self.xspeed = 1
        self.yspeed = 1
        self.speed = 1
        #self.age = 0 #age doesn't matter anymore because it's already an adult.

    def draw(self, window):
        pygame.draw.rect(window.view.screen, [250, 250, 0], [self.x, self.y, 10, 10])


    def rush(self):
        """
        updates dinosaur speed based on hunger level
        """
        self.speed = self.hunger/30.0 + 0.5

    def hunt(self, window):
        """
        lets dino track toward humans within range
        range is based on hunger
        """
        for bug in window.model.bugs:
            if hypot(self.x - bug.x, self.y - bug.y) < self.hunger*5:
                self.angle = 100*atan2(bug.y - self.y, bug.x - self.x)

    def walk(self, window):
        """
        updates position of dinosaur based on speed
        makes dinosaur bounce off walls
        """
        if self.x > window.view.width - self.dino_size:             # bounce off right edge
            self.angle = random.randrange(157,471)
        elif self.x < 1:                    # bounce off left edge
            self.angle = random.randrange(-157,157)
        if self.y < 1:                      # bounce off top edge
            self.angle = random.randrange(0, 314)
        elif self.y > window.view.height - 40:         # bounce off bottom edge
            self.angle = random.randrange(-314,0)
        self.yspeed = sin(self.angle/100.0)*self.speed  # update speed
        self.xspeed = cos(self.angle/100.0)*self.speed  # update speed
        self.x = self.x + self.xspeed
        self.y = self.y + self.yspeed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def starve(self, window):
        """
        updates dinosaur hunger
        """
        if self.hunger < 30:
            #self.health = window.view.dkgrn
            self.hunger += 0.03
        elif self.hunger < 75:
            #self.health = window.view.orange
            self.hunger += 0.03
        elif self.hunger < 100:
            #self.health = window.view.red
            self.hunger += 0.03
        else:
            self.living = False

    def reaper(self, window):
        """
        gets rid of dead dinosaurs
        """
        if self.living is False:
            self.kill()


    def update(self, window):
        self.rush()                            # determines speed
        self.hunt(window)
        self.walk(window)                      # updates its position
        self.starve(window)
        self.reaper(window)
        #self.age += 1

class RawrList(pygame.sprite.Group):
    """
    all inherited
    """