"""
Bug Class and the associated group, just to keep things neat

Notes on what i'm doing: 
these take a "window" input so the main function can pass in the current window.
The ninjas told me to do it last time, makes it applicable to code other than our one specific program i guess.
"""
# yes, I've checked, these need to be here as well as in main
import pygame
import random
from math import sin, cos, hypot, atan2


class Bug(pygame.sprite.Sprite):

    def __init__(self, x, y, window):
        """
        init with some random values to test drawing function
        """
        # init method inherited from pygame sprite class
        # add bug to list of bugs
        pygame.sprite.Sprite.__init__(self, window.model.buglist)


        # base stats/genome (may want to package this as a tuple)
        self.sexiness = random.random()
        self.fleeing = random.random()
        self.hunting = random.random()

        # derivative stats
        # brighter color means more sexiness
        self.color = [255 * self.sexiness, 0, 0]
        # longer legs mean better fleeing
        self.leglength = 30 * self.fleeing
        # longer fangs mean better hunting
        self.toothlength = 10 * self.hunting

        # initial position and angle of motion
        self.x = x
        self.y = y
        self.angle = random.randrange(-314, 314)
        # integer position for walk function and collision detection
        self.width = 35
        self.height = 30
        self.intx = x
        self.inty = y
        self.xspeed = 1
        self.yspeed = 1
        self.speed = 1


    def draw(self, window):
        # draw body
        # the location is [ x from left , y from top, width, height]
        pygame.draw.rect(window.view.screen, self.color, [self.x, self.y, self.width, self.height])
        # draw four eyes
        pygame.draw.rect(window.view.screen, [0, 0, 0], [self.x + 5, self.y + 5, 2, 2])
        pygame.draw.rect(window.view.screen, [0, 0, 0], [self.x + 10, self.y + 8, 4, 4])
        pygame.draw.rect(window.view.screen, [0, 0, 0], [self.x + 18, self.y + 8, 4, 4])
        pygame.draw.rect(window.view.screen, [0, 0, 0], [self.x + 25, self.y + 5, 2, 2])
        # draw four legs
        pygame.draw.rect(window.view.screen, self.color, [self.x, self.y + 30, 5, self.leglength])
        pygame.draw.rect(window.view.screen, self.color, [self.x + 10, self.y + 30, 5, self.leglength])
        pygame.draw.rect(window.view.screen, self.color, [self.x + 20, self.y + 30, 5, self.leglength])
        pygame.draw.rect(window.view.screen, self.color, [self.x + 30, self.y + 30, 5, self.leglength])
        # draw two teeth
        pygame.draw.rect(window.view.screen, [255, 255, 255], [self.x + 10, self.y + 15, 2, self.toothlength])
        pygame.draw.rect(window.view.screen, [255, 255, 255], [self.x + 20, self.y + 15, 2, self.toothlength])


    def hunt(self, window):
        """
        lets dino track toward humans within range
        range is based on hunger
        """
        for nom in window.model.nomlist:
            if hypot(self.x - nom.x, self.y - nom.y) < self.hunger*5:
                self.angle = 100*atan2(nom.y - self.y, nom.x - self.x)

    def walk(self, window):
        """
        Bug moves around and bounces off edges
        """
        if self.x > window.view.width - self.width:             # bounce off right edge
            self.angle = random.randrange(157, 471)
        elif self.x < 1:                    # bounce off left edge
            self.angle = random.randrange(-157, 157)
        if self.y < 1:                      # bounce off top edge
            self.angle = random.randrange(0, 314)
        elif self.y > window.view.height - self.height:         # bounce off bottom edge
            self.angle = random.randrange(-314, 0)
        self.yspeed = sin(self.angle/100.0)*self.speed  # update speed
        self.xspeed = cos(self.angle/100.0)*self.speed  # update speed
        self.x = self.x + self.xspeed
        self.y = self.y + self.yspeed
        self.intx = int(self.x)
        self.inty = int(self.y)

    def breed (self, mate):
        """
        Combines the genes of parent bugs and produces a baby bug
        """
        pass

    def reaper(self, window):
        """
        gets rid of dead bugs
        potentially add a small indication of what the bug died of
        """
        if self.living is False:
            self.kill()

    def update(self, window):
        #self.rush()                            # determines speed
        #self.hunt(window)
        self.walk(window)                      # updates its position
        #self.starve(window)
        #self.reaper(window)
        #self.age += 1


class BugList(pygame.sprite.Group):

    """
    Doesn't need any code, it's built in.
    For reference, these are some inherited methods:
    .add adds a sprite to group
    .remove removes a sprite from group
    .update runs update method of every sprite in group
    .draw blits the image of every sprite in group
    """
