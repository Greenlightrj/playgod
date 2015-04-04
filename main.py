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
            self.controller.checkinput()
            self.model.update(m)
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
            #may return list??
            mate = pygame.sprite.spritecollide(bug, self.buglist, 0, collided = None)
            bug.breed(mate)

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

    def checkinput(self):
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

if __name__ == "__main__":
    m = Main()
    m.mainLoop(m)
