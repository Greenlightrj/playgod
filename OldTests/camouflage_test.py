"""this is to see if I can implement camouflage with DIFFERENT backgrounds!"""

import random

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

enviroColor = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]


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
        self.environ = environment.Environ()
        self.buttons = buttons.Buttons()
        
        #buttons to press
        self.bugbutton = buttons.BugButton((0, 0), self.buttons)
        

    def update(self, window):
        """
        general update function
        will contain list of other model update methods in proper order
        probably our evolutionary algorithms and stuff
        like view.redraw
        """

        for bug in self.buglist:
            bug.update(window)


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
        self.colorBG = enviroColor


    def redraw(self):
        """
        calls all other methods that update the view
        """
        #fill background first
        self.screen.fill(self.colorBG)
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
        	bg = self.colorBG
        	bugColor = [bg[0], bg[1], bg[2]]
        	bugColor[0] = int(round(bg[0] + max(bug.sexiness)*(255 - bg[0])))
        	bugColor[1] = int(round(bg[1] - max(bug.sexiness)*(bg[1])))
        	bugColor[2] = int(round(bg[2] - max(bug.sexiness)*(bg[2])))
        	bug.color = bugColor
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


if __name__ == "__main__":
    m = Main()
    m.mainLoop()
