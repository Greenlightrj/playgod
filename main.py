"""
main program for Playgod game
contains model, view, controller classes and main loop

I'm trying to add lots of helpful comments, delete them if they're redundant
"""
# modules
import pygame
from pygame.locals import RESIZABLE
import random

# other files
import bugs
import noms
import rawrs
import environment
import buttons
import puddles

class Main():

    """
    The Main Class-: handles initialization and main game loop
    """

    def __init__(self):
        """
        initializes pygame and creates other classes
        """
        # initialize pygame
        pygame.init()
        # we use this to tick time forward at a constant rate
        self.clock = pygame.time.Clock()
        # create model, view, controller classes
        self.model = Model()
        self.controller = Controller()
        self.view = View()
        # initialize end condition
        self.done = False

    def mainLoop(self):
        """
        The main game loop
        """
        # runs until player closes program
        while not self.done:
            self.controller.checkinput(self)
            self.model.update(self)
            self.view.redraw(self)
            # tick time forward at a constant rate
            self.clock.tick(60)
        # if loop is exited, quit game
        pygame.quit()


class Model():

    """
    Contains and updates the current state of the game
    """

    def __init__(self):
        # creates our list of bugs
        self.buglist = bugs.BugList()
        self.nomlist = noms.NomList()
        self.rawrlist = rawrs.RawrList()
        self.environ = environment.Environ()
        self.buttons = buttons.Buttons()
        self.puddlelist = puddles.PuddleList()
        #environmental factors
        self.heat = 125
        self.green = 255
        self.wet = 125
        # these rates are the number of milliseconds between automatic spawning
        self.nomrate = (self.green/255.0)*500**3
        self.nomtime = 0
        self.rawrrate = 7500
        self.rawrtime = 0
        self.puddlerate = 5000/(self.wet/255.0)
        self.puddletime = 0
        #buttons to press
        self.bugbutton = buttons.BugButton((0, 0), self.buttons)
        self.nombutton = buttons.NomButton((50, 0), self.buttons)
        self.rawrbutton = buttons.RawrButton((100, 0), self.buttons)
        self.desertdunebutton = buttons.DesertDuneButton((150, 0), self.buttons)
        self.rainforesttreebutton = buttons.RainforestTreeButton((200, 0), self.buttons)
        self.puddlebutton = buttons.PuddleButton((250,0), self.buttons)
        

    def eating(self, window):
        """
        checks for collisions between bugs and noms, and rawrs and noms
        """
        for bug in self.buglist:
            prey = pygame.sprite.spritecollide(bug, self.nomlist, 0, collided = None)
            for nom in prey:
                if max(bug.hunting) < nom.toughness:
                    bug.kill()
                else:
                    if bug.hunger > 30:
                        bug.hunger -= 30
                    else:
                        bug.hunger = 1
                    nom.kill()

        for rawr in self.rawrlist:
            prey = pygame.sprite.spritecollide(rawr, self.buglist, 0, collided = None)
            for bug in prey:
                if max(bug.hunting) > 0.9 and random.random() > 0.5:
                    rawr.kill()
                else:
                    if rawr.hunger > 30:
                        rawr.hunger -= 30
                    else:
                        rawr.hunger = 1
                    bug.kill()

    def drinking (self, window):
        """
        checks for collisions between bugs and puddles
        """
        for bug in self.buglist:
            prey = pygame.sprite.spritecollide(bug, self.puddlelist, 0, collided = None)
            for puddle in prey:
                if bug.thirst > 30:
                        bug.thirst -= 30
                        puddle.get_drunk()
                        bug.angle += 314
                elif random.random()<0.25:
                        bug.kill()
                else:
                    bug.angle += 314

    def mating(self, window):
        for bug in self.buglist:
            #remove the bug so it doesn't mate with itself
            self.buglist.remove(bug)
            mate = pygame.sprite.spritecollide(bug, self.buglist, 0, collided = None)
            if mate == []:
                self.buglist.add(bug)
            else:
                if bug.readyToMate == 1 and mate[0].readyToMate == 1:
                    willTheyWontThey = abs(bug.sexiness - mate[0].sexiness)
                    if willTheyWontThey < random.random():
                        newBug = bug.breed(mate[0], m)
                        self.buglist.add(newBug)
                        #set hunger lower or else bugs create infinite energy by having babies
                        newBug.hunger = max(bug.hunger, mate[0].hunger)
                        newBug.mutate()
                        bug.readyToMate = 0.0
                        mate[0].readyToMate = 0.0
                self.buglist.add(bug)
    

    def spawning(self, window):
        #nomtime is the time at which a nom last spawned. if currently it is nomrate past nomtime, spawn again.
        if pygame.time.get_ticks() - self.nomtime > (self.nomrate/(window.view.width*window.view.height)) and len(window.model.nomlist) < 100:
            noms.Nom(random.randint(0, window.view.width), random.randint(0, window.view.height), window)
            self.nomtime = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.rawrtime > self.rawrrate and len(window.model.rawrlist) < 10:
            rawrs.Rawr(random.randint(0, window.view.width), random.randint(0, window.view.height), window)
            self.rawrtime = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.puddletime > self.puddlerate and len(window.model.puddlelist) < 20:
            puddles.Puddle(random.randint(0, window.view.width - 60), random.randint(50, window.view.height), window)
            self.puddletime = pygame.time.get_ticks()

    def climatechange(self, window):
        for element in self.environ:
            element.effect(window)
        window.view.colorBG[0] = self.heat
        window.view.colorBG[1] = self.green
        window.view.colorBG[2] = self.wet

    def update(self, window):
        """
        general update function
        will contain list of other model update methods in proper order
        probably our evolutionary algorithms and stuff
        like view.redraw
        """
        for nom in self.nomlist:
            nom.update(window)
        for rawr in self.rawrlist:
            rawr.update(window)
        for bug in self.buglist:
            bug.update(window)
        self.eating(window)
        self.drinking(window)
        self.mating(window)
        self.spawning(window)
        self.climatechange(window)


class View():

    """
    The View Class: creates the view on the screen
    """

    def __init__(self, width = 500, height = 500):
        # set screen size
        self.width = width
        self.height = height 
        self.screensize = (self.width, self.height)
        # create screen object
        self.screen = pygame.display.set_mode(self.screensize, RESIZABLE)
        # define colors for later use in drawing
        self.colorBG = [125, 255, 125]


    def redraw(self, window):
        """
        calls all other methods that update the view
        """
        #fill background first
        self.screen.fill(self.colorBG)
        for puddle in window.model.puddlelist:
            puddles.Puddle.draw(puddle, window)
        m.model.environ.draw(self.screen)
        m.model.buttons.draw(self.screen)
        #draw bugs on top
        self.drawbugs(m)
        #actually show all that stuff
        pygame.display.flip()

    def drawbugs(self, window):
        """
        draws bugs according to their genome
        imported from bugs.py
        """
        window.model.nomlist.draw(self.screen)
        window.model.rawrlist.draw(self.screen)
        for bug in window.model.buglist:
            bugs.Bug.draw(bug, window)


class Controller():

    """
    The Controller Class: takes input from the user
    """

    def __init__(self):
        #unused so far
        pass

    def checkinput(self, window):
        for event in pygame.event.get():
            # user clicking 'x' button in corner of window ends the main loop
            if event.type == pygame.QUIT:
                m.done = True
            # user hitting 'esc' key also ends the main loop
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    m.done = True
                if event.key == pygame.K_e:
                    environment.Dune(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], m)
            # pressing any button makes the appropriate animal
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    for button in window.model.buttons:
                        if button.rect.collidepoint(event.pos):
                            button.get_pressed(window)
                elif pygame.mouse.get_pressed()[2]:
                    donedead = False
                    for element in window.model.environ:
                        if element.rect.collidepoint(event.pos):
                            element.kill()
                            donedead = True
                    for puddle in window.model.puddlelist:
                        if puddle.rect.collidepoint(event.pos):
                            puddle.kill()
                            donedead = True
                    if not donedead:
                        for creature in window.model.buglist: 
                            if creature.rect.collidepoint(event.pos):
                                creature.kill()
                                donedead = True
                    if not donedead:
                        for creature in window.model.rawrlist:
                            if creature.rect.collidepoint(event.pos):
                                creature.kill()

            elif event.type == pygame.locals.VIDEORESIZE:
                window.view.screen = pygame.display.set_mode((event.w, event.h), RESIZABLE)
                window.view.width = event.w
                window.view.height = event.h

if __name__ == "__main__":
    m = Main()
    m.mainLoop()
