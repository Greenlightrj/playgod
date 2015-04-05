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
        self.sexiness = [random.random(), random.random()]
        self.fleeing = [random.random(), random.random()]
        self.hunting = [random.random(), random.random()]

        #this will make it so bugs that are colliding don't mate a MILLION TIMES
        self.readyToMate = 0.0

        # derivative stats
        # brighter color means more sexiness
        self.color = [255 * max(self.sexiness), 0, 0]
        # longer legs mean better fleeing
        self.leglength = 30 * max(self.fleeing)
        # longer fangs mean better hunting
        self.toothlength = 10 * max(self.hunting)

        # initial position and angle of motion
        self.x = x
        self.y = y
        self.angle = random.randrange(-314, 314)
        # the collision requires a sprite for a hitbox.
        # bughitbox.png is an empty transparent image the same size as the bug body.
        self.hitbox = pygame.image.load("bughitbox.png")
        self.rect = self.hitbox.get_rect()
        self.width = self.rect.size[0]
        self.height = self.rect.size[1]
        self.rect.x = x
        self.rect.y = y
        # motion stats
        self.xspeed = 1
        self.yspeed = 1
        self.speed = max(self.fleeing)*3
        # status
        self.hunger = 1
        self.living = True


    def draw(self, window):
        # draw body
        # the location is [x from left , y from top, width, height]
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
        bug tracks toward noms within range.
        """
        dist = 100
        nearest = False
        for nom in window.model.nomlist:
            far = hypot(self.x - nom.x, self.y - nom.y)
            if far < dist:
                nearest = nom
                dist = far
        if nearest:
            self.angle = 100*atan2(nearest.y - self.y, nearest.x - self.x)


    def flee(self, window):
        """
        bug runs from the nearest predator
        """
        if len(window.model.rawrlist) > 0:     #if there are any rawrs
            dist = 100
            nearest = 0
            for rawr in window.model.rawrlist:
                if hypot(rawr.x - self.x, rawr.y - self.y) < dist:
                    dist = hypot(rawr.x - self.x, rawr.y - self.y)
                    nearest = rawr
            if nearest:
                self.angle = 100*atan2(self.y - nearest.y, self.x - nearest.x)


    def walk(self, window):
        """
        Bug moves around and bounces off edges
        """
        if self.x > window.view.width:
            self.x = 10
        elif self.x < 1:
            self.x = window.view.width-10
        if self.y < 1:
            self.y = window.view.height-10
        elif self.y > window.view.height:
            self.y = 10
        self.yspeed = sin(self.angle/100.0)*self.speed  # update speed
        self.xspeed = cos(self.angle/100.0)*self.speed  # update speed
        self.x = self.x + self.xspeed
        self.y = self.y + self.yspeed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def starve(self, window):
        """
        updates bug hunger
        """
        if self.hunger < 100:
            self.hunger += 0.1
        else:
            self.living = False

    def reaper(self, window):
        """
        gets rid of dead bugs
        potentially add a small indication of what the bug died of
        """
        if self.living is False:
            self.kill()

    def update(self, window):
        """
        calls all bug-updating methods in the proper order
        """
        self.hunt(window)
        self.flee(window)
        self.walk(window)
        self.starve(window)
        self.reaper(window)
        if self.readyToMate >= 1:
            self.readyToMate = 1
        else:
             self.readyToMate = self.readyToMate + 0.005

    def getGenes(self):
        """
        gets a random one of each the Animal's genes and returns them as a list [sexiness, fleeing, hunting]
        """
        geneList = []

        if random.random() < 0.5:
            geneList.append(self.sexiness[0])
        else:
            geneList.append(self.sexiness[1])
        if random.random() < 0.5:
            geneList.append(self.fleeing[0])
        else:
            geneList.append(self.fleeing[1])
        if random.random() < 0.5:
            geneList.append(self.hunting[0])
        else:
            geneList.append(self.hunting[1])

        return geneList


    def breed(self, mate, window):
        """
        Combines the genes of parent bugs and produces a baby bug
        """
        newBug = Bug(self.x, self.y, window)

        momGenes1 = self.getGenes()
        momGenes2 = mate.getGenes()

        newBug.sexiness = [momGenes1[0], momGenes2[0]]
        newBug.fleeing = [momGenes1[1], momGenes2[1]]
        newBug.hunting = [momGenes1[2], momGenes2[2]]
        
        return newBug



class BugList(pygame.sprite.Group):

    """
    Doesn't need any code, it's built in.
    For reference, these are some inherited methods:
    _.add() adds a sprite to group
    _.remove() removes a sprite from group
    _.update() runs update method of every sprite in group
    _.draw() blits the image of every sprite in group
    """
