"""
Rawr class. 
Handles the predators of the bugs.
"""

import pygame
import random
from math import sin, cos, hypot, atan2


class Rawr(pygame.sprite.Sprite):
    """
    The ambulatory plants that serve as predators.
    inherited methods:
    _.update() (see below)
    _.kill() (removes from all groups)
    _.alive()  (checks to see if belonging to any groups)
    """
    def __init__(self, x, y, window):
        """
        initializes position, attributes, and sprite
        rawrs start alive with 1 hunger
        """
        pygame.sprite.Sprite.__init__(self, window.model.rawrlist) #puts rawr in list of rawrs
        self.image = pygame.image.load("Images/bugeater.png")
        self.rect = self.image.get_rect()
        self.width = self.rect.size[0]
        self.height = self.rect.size[1]
        self.rect.x = x
        self.rect.y = y
        self.x = x  #actual position, can be float
        self.y = y
        self.rect.x = x     #integer position for drawing
        self.rect.y = y
        self.hunger = 1
        self.angle = random.randrange(-314, 314)
        self.xspeed = 1
        self.yspeed = 1
        self.speed = 0.03*(1.3*window.model.heat/255.0)*random.randint(40, 100)


    def draw(self, window):
        """
        draws the rawr in its position on the screen
        """
        pygame.draw.rect(window.view.screen, [250, 250, 0], [self.x, self.y, 10, 10])


    def hunt(self, window):
        """
        lets rawr track toward bugs within range
        range is based on hunger and sexiness of bug
        """
        dist = 200
        nearest = False
        for bug in window.model.buglist:
            if bug.sexiness > 0.25:
                far = hypot(self.x - bug.x, self.y - bug.y)/(bug.sexiness*2)
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
        if self.y < 50:                      # bounce off top edge
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
            self.kill()

    def update(self, window):
        """
        calls methods in the proper order
        """
        self.hunt(window)
        self.walk(window)
        self.starve(window)


class RawrList(pygame.sprite.Group):
    """
    group list of all living rawrs
    all methods inherited from pygame sprite group parent class inherited
    """