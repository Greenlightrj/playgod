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
    _.update() (see below)
    _.kill() (removes from all groups)
    _.alive()  (checks to see if belonging to any groups)
    """
    def __init__(self, x, y, window):
        """
        dinos start alive with 1 hunger
        """
        pygame.sprite.Sprite.__init__(self, window.model.rawrlist) #puts dino in list of dinos
        self.image = pygame.image.load("bugeater.png")
        self.rect = self.image.get_rect()
        self.width = self.rect.size[0]
        self.height = self.rect.size[1]
        self.rect.x = x
        self.rect.y = y
        self.x = x  #actual position, can be float
        self.y = y
        self.rect.x = x     #integer position for drawing
        self.rect.y = y
        self.living = True
        self.hunger = 1
        self.angle = random.randrange(-314, 314)
        self.xspeed = 1
        self.yspeed = 1
        self.speed = random.random()*3


    def draw(self, window):
        pygame.draw.rect(window.view.screen, [250, 250, 0], [self.x, self.y, 10, 10])


    def hunt(self, window):
        """
        lets rawr track toward bugs within range
        range is based on hunger and sexiness of bug
        """
        dist = 600
        nearest = False
        for bug in window.model.buglist:
            far = hypot(self.x - bug.x, self.y - bug.y)*max(bug.sexiness)*2
            if far < dist:
                nearest = bug
                dist = far
        if nearest:
            self.angle = 100*atan2(nearest.y - self.y, nearest.x - self.x)

    def walk(self, window):
        """
        updates position of rawr based on speed
        makes rawr bounce off walls
        """
        if self.x > window.view.width - self.width:             # bounce off right edge
            self.angle = random.randrange(157,471)
        elif self.x < 1:                    # bounce off left edge
            self.angle = random.randrange(-157,157)
        if self.y < 1:                      # bounce off top edge
            self.angle = random.randrange(0, 314)
        elif self.y > window.view.height - self.height:         # bounce off bottom edge
            self.angle = random.randrange(-314,0)
        self.yspeed = sin(self.angle/100.0)*self.speed  # update speed
        self.xspeed = cos(self.angle/100.0)*self.speed  # update speed
        self.x = self.x + self.xspeed
        self.y = self.y + self.yspeed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def starve(self, window):
        """
        updates rawr hunger
        """
        if self.hunger < 100:
            self.hunger += 0.1
        else:
            self.living = False

    def reaper(self, window):
        """
        gets rid of dead rawrs
        """
        if self.living is False:
            self.kill()


    def update(self, window):
        self.hunt(window)
        self.walk(window)
        self.starve(window)
        self.reaper(window)


class RawrList(pygame.sprite.Group):
    """
    all inherited
    """