"""
main program for Playgod game
requires other files:
"""
import pygame
import bugdrawer.py

class Main():
    """
    The Main Class-: handles initialization and main game loop
    """
    def __init__(self):
        """
        initializes pygame and creates other classes
        """
        pygame.init()
        self.clock = pygame.time.Clock()
        self.controller = Controller()
        self.model = Model()
        self.view = View()
        self.done = False 

    def mainLoop(self):
        """
        The main game loop
        """
        while not self.done:
            self.controller.checkinput()
            self.view.redraw()
        pygame.quit()


class Model():
    """
    Contains and updates the current state of the game
    """
    def __init__(self):
        pass

    def update(self):
        pass

class View():
    """
    The View Class: creates the view on the screen
    """
    def __init__(self):
        self.width = width
        self.height = height
        size = (self.width, self.height)
        self.screen = pygame.display.set_mode(size)
        self.black = [0,0,0]

    def redraw(self):
        self.screen.fill(self.black)
        pygame.display.flip()

class Controller():
    """
    The Controller Class: takes input from the user
    """
    def __init__(self):
        pass

    def checkinput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                MainWindow.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    MainWindow.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # when mouse button is clicked
                if pygame.mouse.get_pressed()[0]:     # left mouse button click
                    Bug()

if __name__ == "__main__":
    MainWindow = Main()
    MainWindow.mainLoop()
