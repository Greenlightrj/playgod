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

    def mainLoop(self, window):
        """
        The main game loop
        """
        # runs until player closes program
        while not self.done:
            self.controller.checkinput(window)
            self.model.update(window)
            self.view.redraw()
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
        # these rates are the number of milliseconds between automatic spawning
        self.nomrate = 500**3
        self.nomtime = 0
        self.rawrrate = 15000
        self.rawrtime = 0

    def eating(self, window):
        """
        checks for collisions between bugs and noms, and rawrs and noms
        """
        for bug in self.buglist:
            prey = pygame.sprite.spritecollide(bug, self.nomlist, 0, collided = None)
            for nom in prey:
                if bug.hunting < nom.toughness and random.random() < 0.5:
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
                if rawr.hunger > 30:
                    rawr.hunger -= 30
                else:
                    rawr.hunger = 1
                bug.kill()

    def mating(self, window):
        for bug in self.buglist:
            #remove the bug so it doesn't mate with itself
            self.buglist.remove(bug)
            mate = pygame.sprite.spritecollide(bug, self.buglist, 0, collided = None)
            if mate == []:
                self.buglist.add(bug)
            else:
                if bug.readyToMate == 1 and mate[0].readyToMate == 1:
                    willTheyWontThey = abs(max(bug.sexiness) - max(mate[0].sexiness))
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
        self.mating(window)
        self.spawning(window)



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
        self.black = [0, 0, 0]

    def redraw(self):
        """
        calls all other methods that update the view
        """
        #fill background first
        self.screen.fill(self.black)
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
            # user left-clicking creates an instance of the bug class where clicked
            # right click creates food
            # center click creates predator
            # later, implement a button-press to place these.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    bugs.Bug(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], m)
                elif pygame.mouse.get_pressed()[1]:
                    rawrs.Rawr(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], m)
                elif pygame.mouse.get_pressed()[2]:
                    noms.Nom(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], m)
            elif event.type == pygame.locals.VIDEORESIZE:
                window.view.screen = pygame.display.set_mode((event.w, event.h), RESIZABLE)
                window.view.width = event.w
                window.view.height = event.h

if __name__ == "__main__":
    m = Main()
    m.mainLoop(m)
