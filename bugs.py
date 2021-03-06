"""
Bug Class and the associated group, just to keep things neat
Most methods take a "window" input so the main function can pass in the current window.
"""

import pygame
import random
from math import sin, cos, hypot, atan2


class Bug(pygame.sprite.Sprite):

    def __init__(self, x, y, window):
        """
        init method inherited from pygame sprite class
        initializes the genome, position, sprite, and status of the bug
        """
        # add bug to list of bugs
        pygame.sprite.Sprite.__init__(self, window.model.buglist)

        # base stats/genome
        self.color = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
        self.fleeing = [random.random(), random.random()]
        self.hunting = [random.random(), random.random()]
        self.fuzz = [random.random(), random.random()]
        self.camelfactor = [random.random(), random.random()]

        # derivative stats
        # brighter color means more sexiness
        reddiff = abs(window.view.colorBG[0] - self.color[0])
        grndiff = abs(window.view.colorBG[1] - self.color[1])
        bludiff = abs(window.view.colorBG[2] - self.color[2])
        self.sexiness = (reddiff + grndiff + bludiff)/765.0
        # longer legs mean better fleeing
        self.leglength = 15 * max(self.fleeing)
        # longer fangs mean better hunting
        self.toothlength = 6 * max(self.hunting)
        # more fuzz and shorter legs make for a warmer bug
        self.furlength = 3 * max(self.fuzz)
        self.warmth = (max(self.fuzz) - 0.2*max(self.fleeing))
        if self.warmth < 0:
            self.warmth = 0
        # higher camel factor gives bigger tum and more drought resistance
        self.tumlength = 3 *max(self.camelfactor)

        # initial position and angle of motion
        self.x = x
        self.y = y
        self.angle = random.randrange(-314, 314)

        # the collision requires a sprite for a hitbox.
        # bughitbox.png is an empty transparent image the same size as the bug body.
        self.hitbox = pygame.image.load("Images/bughitbox2.png")
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
        self.thirst = 1
        self.readyToMate = 0.0

    def draw(self, window):
        """
        draws the bug according to its genome
        """
        # draw body
        pygame.draw.rect(window.view.screen, self.color, [self.x, self.y, self.width, self.height])
        # draw fuzz
        pygame.draw.rect(window.view.screen, self.color, [self.x, self.y - self.furlength + 1, 5, self.furlength])
        pygame.draw.rect(window.view.screen, self.color, [self.x + self.width - 5, self.y - self.furlength + 1, 5, self.furlength])
        pygame.draw.rect(window.view.screen, self.color, [self. x - self.furlength + 1, self.y + 7, self.furlength, 9])
        pygame.draw.rect(window.view.screen, self.color, [self. x + self.width - 1, self.y + 7, self.furlength, 9])
        # draw tum
        pygame.draw.rect(window.view.screen, self.color, [self.x + 6, self.y + self.height - 2, 6, self.tumlength + 2])
        # draw four eyes
        pygame.draw.rect(window.view.screen, [0, 0, 0], [self.x + 3, self.y + 2, 2, 2])
        pygame.draw.rect(window.view.screen, [0, 0, 0], [self.x + 6, self.y + 5, 3, 3])
        pygame.draw.rect(window.view.screen, [0, 0, 0], [self.x + 12, self.y + 5, 3, 3])
        pygame.draw.rect(window.view.screen, [0, 0, 0], [self.x + 15, self.y + 2, 2, 2])
        # draw four legs
        pygame.draw.rect(window.view.screen, self.color, [self.x, self.y + 17, 3, self.leglength])
        pygame.draw.rect(window.view.screen, self.color, [self.x + 6, self.y + 17, 3, self.leglength])
        pygame.draw.rect(window.view.screen, self.color, [self.x + 11, self.y + 17, 3, self.leglength])
        pygame.draw.rect(window.view.screen, self.color, [self.x + 17, self.y + 17, 3, self.leglength])
        # draw two teeth
        pygame.draw.rect(window.view.screen, [255, 255, 255], [self.x + 6, self.y + 10, 1, self.toothlength])
        pygame.draw.rect(window.view.screen, [255, 255, 255], [self.x + 12, self.y + 10, 1, self.toothlength])


    def hunt(self, window):
        """
        bug tracks toward noms within range, or puddles if it is thirsty.
        """
        
        nearest = False
        if self.thirst > 30 and self.thirst > self.hunger:
            dist = 1000
            for puddle in window.model.puddlelist:
                far = hypot(self.x - puddle.x, self.y - puddle.y)
                if far < dist:
                    nearest = puddle
                    dist = far
        else:
            dist = 100
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
        if len(window.model.rawrlist) > 0:
            dist = 100
            nearest = 0
            for rawr in window.model.rawrlist:
                if hypot(rawr.x - self.x, rawr.y - self.y) < dist:
                    dist = hypot(rawr.x - self.x, rawr.y - self.y)
                    nearest = rawr
            if nearest:
                self.angle = 100*atan2(self.y - nearest.y, self.x - nearest.x) + random.randint(-20,20)


    def walk(self, window):
        """
        Bug moves around and bounces off edges
        """
        if self.x > window.view.width:
            self.x = 10
        elif self.x < 1:
            self.x = window.view.width-10
        if self.y < 50:
            self.y = window.view.height-10
        elif self.y > window.view.height:
            self.y = 60
        self.yspeed = sin(self.angle/100.0)*self.speed
        self.xspeed = cos(self.angle/100.0)*self.speed
        self.x = self.x + self.xspeed
        self.y = self.y + self.yspeed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def freeze(self, window):
        """
        Checks environmental temperature
        bugs have a higher chance of dying if their fur length is too long or too short for the temperature
        """
        if 0.07*random.random() > abs(window.model.heat/255 - 1 + self.warmth):
            window.model.tempdeaths += 1
            self.kill()

    def starve(self, window):
        """
        updates bug hunger and thirst
        """
        if self.hunger < 100:
            self.hunger += 0.05
        else:
            window.model.starves += 1
            self.kill()

        if self.thirst < 100:
            self.thirst += 0.03/max(self.camelfactor)
        else:
            window.model.thirsts += 1
            self.kill()

    def update(self, window):
        """
        calls all bug-updating methods in the proper order
        """
        self.hunt(window)
        self.flee(window)
        self.walk(window)
        self.starve(window)
        self.freeze(window)
        if self.readyToMate >= 1:
            self.readyToMate = 1
        else:
             self.readyToMate = self.readyToMate + 0.005

    def getGenes(self):
        """
        gets a random one of each the Animal's genes and returns them as a list [sexiness, fleeing, hunting]
        """
        geneList = []

        geneList.append(self.color)
        if random.random() < 0.5:
            geneList.append(self.fleeing[0])
        else:
            geneList.append(self.fleeing[1])
        if random.random() < 0.5:
            geneList.append(self.hunting[0])
        else:
            geneList.append(self.hunting[1])
        if random.random() < 0.5:
            geneList.append(self.fuzz[0])
        else:
            geneList.append(self.fuzz[1])

        return geneList


    def colormix (self, mate, n):
        """
        determines the color of the offspring of a bug and its mate
        color can
        """
        if self.color[n] == mate.color[n]:
            babycolor = self.color[n]
        elif self.color[n] > mate.color[n]:
            babycolor = random.randint(mate.color[n], self.color[n])
        else:
            babycolor = random.randint(self.color[n], mate.color[n])
        if random.random < 0.1:
            babycolor += random.randint(-25, 25)
        if babycolor > 255:
            babycolor = 255
        elif babycolor < 0:
            babycolor = 0

        return babycolor

    def breed(self, mate, window):
        """
        Combines the genes of parent bugs and produces a baby bug
        """
        newBug = Bug(self.x, self.y, window)

        momGenes1 = self.getGenes()
        momGenes2 = mate.getGenes()

        red = self.colormix(mate, 0)
        green = self.colormix(mate, 1)
        blue = self.colormix(mate, 2)
        newBug.color = [red, green, blue]
        newBug.fleeing = [momGenes1[1], momGenes2[1]]
        newBug.hunting = [momGenes1[2], momGenes2[2]]
        newBug.fuzz = [momGenes1[3], momGenes2[3]]

        return newBug


    def zerocheck(self, floatVal):
        """
        if value is less than zero or more than one it is set to zero or one respectively
        """
        if floatVal < 0:
            floatVal = 0
        elif floatVal > 1:
            floatVal = 1

        return floatVal

    def mutate(self):
        """
        has a 0.1 chance of shifting a gene value by 0.1
        """
        rand1 = random.random() #whether to mutate
        rand2 = random.randint(0, 2) #which stat to mutate
        rand3 = random.randint(0, 1) #which chromosome to mutate
        rand4 = 0.2*(0.5 - random.randint(0, 1)) #which direction and how much

        if rand1 < 0.1:
            if rand2 == 0:
                self.fleeing[rand3] += rand4
                self.fleeing[rand3] = self.zerocheck(self.fleeing[rand3])
            elif rand2 == 1:
                self.hunting[rand3] += rand4
                self.hunting[rand3] = self.zerocheck(self.hunting[rand3])
            elif rand2 == 2:
                self.fuzz[rand3] += rand4
                self.fuzz[rand3] = self.zerocheck(self.fuzz[rand3])   


class BugList(pygame.sprite.Group):

    """
    Doesn't need any code, it's built in.
    For reference, these are some inherited methods:
    _.add() adds a sprite to group
    _.remove() removes a sprite from group
    _.update() runs update method of every sprite in group
    _.draw() blits the image of every sprite in group
    """
