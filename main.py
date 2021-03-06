"""
main program for Playgod game
contains model, view, controller classes and main loop
"""
# external modules
import pygame
from pygame.locals import RESIZABLE
import random

# Playgod modules
import bugs
import noms
import rawrs
import environment
import buttons
import puddles
import graphs2


class Main():

    """
    The Main Class: handles initialization and main game loop
    """

    def __init__(self):
        """
        initializes pygame and creates other classes
        """
        pygame.init()
        # we use this to tick time forward at a constant rate
        self.clock = pygame.time.Clock()
        # create model, view, controller classes
        self.model = Model()
        self.controller = Controller()
        self.view = View()
        # starts with 15 bugs and 3 puddles
        for i in range(0, 15):
            bugs.Bug(random.random() * self.view.width,
                     random.random() * self.view.height, self)
        for i in range(0, 3):
            puddles.Puddle(random.randint(
                0, self.view.width - 60), random.randint(50, self.view.height - 40), self)
        # initialize start screen, win screen, and end condition
        self.done = False
        self.started = False
        self.won = False
        self.winCondition = [255, 255, 0]

    def mainLoop(self):
        """
        The main game loop. Runs until player closes the program.
        """
        while not self.done:
            self.controller.checkinput(self)
            self.model.update(self)
            self.view.redraw(self)
            # prevents the game from running at more than 60 FPS
            self.clock.tick(60)
        # if loop is exited, quit game
        pygame.quit()


class Model():

    """
    Contains and updates the current state of the game
    """

    def __init__(self):
        """
        Initializes lists of objects, 
        """
        # creates our lists of objects
        self.buglist = bugs.BugList()
        self.nomlist = noms.NomList()
        self.rawrlist = rawrs.RawrList()
        self.environ = environment.Environ()
        self.buttons = buttons.Buttons()
        self.puddlelist = puddles.PuddleList()
        # environmental factors
        self.heat = 125
        self.green = 255
        self.wet = 125
        # begins counting when win condition is met to create delay
        self.counter = 0
        # money tally
        self.money = 0
        # counter of how many bugs have died of what
        self.starves = 0
        self.thirsts = 0
        self.rawrdeaths = 0
        self.nomdeaths = 0
        self.drowns = 0
        self.tempdeaths = 0
        # these rates are the approximate number of milliseconds between automatic spawning
        self.nomrate = (self.green / 255.0) * 500**3
        self.nomtime = 0
        self.rawrrate = 7500
        self.rawrtime = 0
        self.puddlerate = 1000 / (self.wet / 255.0)**2
        self.puddletime = 0
        # initialize an object from each button class to create pressable buttons
        self.bugbutton = buttons.BugButton((0, 0), self.buttons)
        self.nombutton = buttons.NomButton((50, 0), self.buttons)
        self.rawrbutton = buttons.RawrButton((100, 0), self.buttons)
        self.desertdunebutton = buttons.DesertDuneButton((150, 0), self.buttons)
        self.desertpalmtreebutton = buttons.DesertPalmTreeButton((200, 0), self.buttons)
        self.deserthillbutton = buttons.DesertHillButton((250, 0), self.buttons)
        self.rainforesttreebutton = buttons.RainforestTreeButton((300, 0), self.buttons)
        self.arcticdesertdunebutton = buttons.ArcticDesertDuneButton((350,0), self.buttons)
        self.puddlebutton = buttons.PuddleButton((400,0), self.buttons)

    def eating(self, window):
        """
        checks for collisions between bugs and noms, and rawrs and noms
        kills the loser of the encounter
        keeps track of hunger and number of starvation deaths
        """
        for bug in self.buglist:
            prey = pygame.sprite.spritecollide(
                bug, self.nomlist, 0, collided=None)
            for nom in prey:
                if max(bug.hunting) < nom.toughness:
                    self.nomdeaths += 1
                    bug.kill()
                else:
                    if bug.hunger > 30:
                        bug.hunger -= 30
                    else:
                        bug.hunger = 1
                    nom.kill()

        for rawr in self.rawrlist:
            prey = pygame.sprite.spritecollide(
                rawr, self.buglist, 0, collided=None)
            for bug in prey:
                if max(bug.hunting) > 0.9 and random.random() > 0.5:
                    rawr.kill()
                else:
                    if rawr.hunger > 30:
                        rawr.hunger -= 30
                    else:
                        rawr.hunger = 1
                    self.rawrdeaths += 1
                    bug.kill()

    def drinking(self, window):
        """
        checks for collisions between bugs and puddles
        bugs drink and lose thirst
        bugs bounce off puddles if not thirsty
        bugs drown if too drought-resistant
        """
        for bug in self.buglist:
            prey = pygame.sprite.spritecollide(
                bug, self.puddlelist, 0, collided=None)
            for puddle in prey:
                if max(bug.camelfactor) > 2 * random.random() + 105:
                    self.drowns += 1
                    bug.kill()
                elif bug.thirst > 30:
                    bug.thirst -= 30
                    puddle.get_drunk()
                    bug.angle += 314
                else:
                    bug.angle += 314

    def mating(self, window):
        """
        checks for collisions between bugs
        if they are ready to mate and pass a probability check, 
        creates a new bug with traits inherited from parents
        parents lose hunger to avoid creating infinite energy.
        """
        for bug in self.buglist:
            # remove the bug so it doesn't mate with itself
            self.buglist.remove(bug)
            mate = pygame.sprite.spritecollide(
                bug, self.buglist, 0, collided=None)
            if mate == []:
                self.buglist.add(bug)
            else:
                if bug.readyToMate == 1 and mate[0].readyToMate == 1:
                    willTheyWontThey = 0
                    if willTheyWontThey < random.random():
                        newBug = bug.breed(mate[0], m)
                        self.buglist.add(newBug)
                        newBug.hunger = 50
                        bug.hunger += 25
                        mate[0].hunger += 25
                        newBug.mutate()
                        bug.readyToMate = 0.0
                        mate[0].readyToMate = 0.0
                        self.money += 5
                self.buglist.add(bug)

    def spawning(self, window):
        """
        checks the amount of time since a nom, a rawr, and a puddle last spawned
        if the time is greater than the amount of time that should pass between spawns, 
        creates the relevant object.
        """
        # nomtime is the time at which a nom last spawned. if currently it is
        # nomrate past nomtime, spawn again.
        if pygame.time.get_ticks() - self.nomtime > (self.nomrate / (window.view.width * window.view.height)) and len(window.model.nomlist) < 100:
            noms.Nom(random.randint(0, window.view.width),
                     random.randint(0, window.view.height), window)
            self.nomtime = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.rawrtime > self.rawrrate and len(window.model.rawrlist) < 10:
            rawrs.Rawr(random.randint(0, window.view.width),
                       random.randint(0, window.view.height), window)
            self.rawrtime = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.puddletime > self.puddlerate and len(window.model.puddlelist) < 10:
            puddles.Puddle(random.randint(
                0, window.view.width - 60), random.randint(50, window.view.height), window)
            self.puddletime = pygame.time.get_ticks()

    def climatechange(self, window):
        """
        checks the values of the environmental attributes
        changes background color accordingly
        """
        for element in self.environ:
            element.effect(window)
        window.view.colorBG[0] = self.heat
        window.view.colorBG[1] = self.green
        window.view.colorBG[2] = self.wet

    def wincheck(self, window):
        """
        if the environment fulfills the win condition and there are enough bugs,
        increments counter toward victory;
        if either condition becomes false the counter is zeroed
        """
        colors = [int(window.view.colorBG[0]), int(
            window.view.colorBG[1]), int(window.view.colorBG[2])]

        if colors == window.winCondition and len(self.buglist) > 9 and self.counter <= 3000:
            self.counter += 1
        else:
            self.counter = 0

        if self.counter >= 3000:
            window.won = True

    def update(self, window):
        """
        general update function
        calls other model update methods in proper order
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
        self.wincheck(window)

class View():

    """
    The View Class: creates the image on the screen
    """

    def __init__(self, width=1000, height=800):
        """
        sets default screen size and creates screen object
        initializes font and background color
        creates instance of graphs class
        """
        # set screen size
        self.drawwidth = width
        self.graphwidth = 200
        #the width of the window in which the game objects bounce around
        self.width = width - self.graphwidth
        self.height = height
        self.screensize = (self.drawwidth, self.height)
        # initialize font
        self.font = pygame.font.SysFont('monospace', 15)
        # create screen object
        self.screen = pygame.display.set_mode(self.screensize, RESIZABLE)
        # initialize graphs class
        self.graphs = graphs2.graphs()
        # define initial background color
        self.colorBG = [125, 255, 125]

    def redraw(self, window):
        """
        draws beginning or win screen
        calls all other methods that update the view
        """
        if m.won:
            screen = pygame.display.set_mode((self.width, self.height))
            self.screen.fill((33, 0, 127))
            image = pygame.image.load("Images/winscreen.png")
            screen.blit(image, (self.width / 2 - 70, self.height / 2 - 100))
        elif m.started:
            screen = pygame.display.set_mode(
                (self.drawwidth, self.height), RESIZABLE)
            # fill background first
            self.screen.fill(self.colorBG)
            for puddle in window.model.puddlelist:
                puddles.Puddle.draw(puddle, window)
            m.model.environ.draw(self.screen)
            m.model.buttons.draw(self.screen)
            # draw bugs on top
            self.drawbugs(m)
            self.graphs.redraw(window)
        else:
            screen = pygame.display.set_mode(
                (self.width, self.height), RESIZABLE)
            image = pygame.image.load("Images/startscreen.png")
            screen.blit(image, (0, 0))
        # actually show all that stuff
        pygame.display.flip()

    def drawbugs(self, window):
        """
        draws bugs according to their genome
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
        """
        unused
        """
        pass

    def checkinput(self, window):
        """
        checks for any user input and calls the correct function
        """
        for event in pygame.event.get():
            # user clicking 'x' button in corner of window ends the main loop
            if event.type == pygame.QUIT:
                m.done = True
            # user hitting 'esc' key also ends the main loop
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    m.done = True
                elif event.key == pygame.K_SEMICOLON:
                    window.model.money = 100000

            elif event.type == pygame.MOUSEBUTTONDOWN:
                m.started = True
                # pressing any button makes the appropriate object
                if pygame.mouse.get_pressed()[0]:
                    for button in window.model.buttons:
                        if button.rect.collidepoint(event.pos):
                            button.get_pressed(window)
                # right clicking deletes objects
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
            # resizing the window changes some of the spawn rates
            elif event.type == pygame.locals.VIDEORESIZE:
                window.view.screen = pygame.display.set_mode((event.w, event.h), RESIZABLE)
                window.view.drawwidth = event.w
                window.view.width = window.view.drawwidth - \
                    window.view.graphwidth
                window.view.height = event.h
                window.model.puddlerate = window.model.puddlerate * \
                    (event.w * event.h / 800**2)

if __name__ == "__main__":
    m = Main()
    m.mainLoop()
