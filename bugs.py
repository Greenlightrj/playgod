"""
Bug Class and the associated group, just to keep things neat

Notes on what i'm doing: 
these take a "window" input so the main function can pass in the current window.
The ninjas told me to do it last time, makes it applicable to code other than our one specific program i guess.
"""
#yes, I've checked, these need to be here as well as in main
import pygame
import random

class Bug(pygame.sprite.Sprite):

    def __init__(self, window):
        """
        init with some random values to test drawing function
        """
        # init method inherited from pygame sprite class
        pygame.sprite.Sprite.__init__(self)

        # base stats/genome (may want to package this as a tuple)
        self.sexiness = random.random()
        self.fleeing = random.random()
        self.hunting = random.random()

        # derivative stats
        # brighter color means more sexiness
        self.color = [255*self.sexiness, 0, 0]
        # longer legs mean better fleeing
        self.leglength = 30*self.fleeing
        # longer fangs mean better hunting
        self.toothlength = 10*self.hunting

        # position, random and constant for now
        self.x = random.randint(0,window.view.width)
        self.y = random.randint(0,window.view.height)

        # add bug to list of bugs
        window.model.buglist.add(self)
        

    def drawbug(self, window):
        # draw body
        pygame.draw.rect(window.view.screen, self.color, [self.x, self.y, 35, 30]) # the location is [ x from left , y from top, width, height]
        # draw four eyes
        pygame.draw.rect(window.view.screen, [0,0,0], [self.x + 5, self.y + 5, 2, 2])
        pygame.draw.rect(window.view.screen, [0,0,0], [self.x + 10, self.y + 8, 4, 4])
        pygame.draw.rect(window.view.screen, [0,0,0], [self.x + 18, self.y + 8, 4, 4])
        pygame.draw.rect(window.view.screen, [0,0,0], [self.x + 25, self.y + 5, 2, 2])
        # draw four legs        
        pygame.draw.rect(window.view.screen, self.color, [self.x, self.y + 30, 5, self.leglength])
        pygame.draw.rect(window.view.screen, self.color, [self.x + 10, self.y + 30, 5, self.leglength])
        pygame.draw.rect(window.view.screen, self.color, [self.x + 20, self.y + 30, 5, self.leglength])
        pygame.draw.rect(window.view.screen, self.color, [self.x + 30, self.y + 30, 5, self.leglength])
        # draw two teeth
        pygame.draw.rect(window.view.screen, [255,255,255], [self.x + 10, self.y + 15, 2, self.toothlength])
        pygame.draw.rect(window.view.screen, [255,255,255], [self.x + 20, self.y + 15, 2, self.toothlength])

class BugList(pygame.sprite.Group):
    """
    Doesn't need any code, it's built in.
    For reference, these are some inherited methods:
    .add adds a sprite to group
    .remove removes a sprite from group
    .update runs update method of every sprite in group
    .draw blits the image of every sprite in group
    """
    