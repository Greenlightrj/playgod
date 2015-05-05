
import pygame
import random
import bugs
import noms
import rawrs
import environment
import puddles


class Button (pygame.sprite.Sprite):
    """
    parent class for Buttons
    """
    def __init__(self, position, buttonlist):
        """
        calls init method for a pygame sprite object
        initializes position and sprite
        the basic button class's sprite is a blank button
        """
        pygame.sprite.Sprite.__init__(self, buttonlist)
        self.x = position[0]
        self.y = position[1]
        self.image = pygame.image.load("Images/button.png")
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.pressed = False

    def draw_icon(self, window):
        """
        draws the button's sprite at the button's position
        """
        self.icon.blit(window.view.screen, (self.x + 5, self.y + 5))

    def get_pressed(self):
        """
        method for inheriting classes to modify
        to change what a button press does
        """
        pass


class BugButton(Button):
    """
    button that creates a bug at a random point onscreen
    """
    def __init__(self, position, buttonlist):
        """
        replaces the default button image with the bug button image
        """
        Button.__init__(self, position, buttonlist)
        self.image = pygame.image.load("Images/bugbutton.png")

    def get_pressed(self, window):

        """
        if player has enough money,
        creates an instance of the bug class at a random point onscreen
        reduces money by 10
        """
        if window.model.money >= 10:
            bugs.Bug(random.random()*window.view.width, random.random()*window.view.height, window)
            window.model.money -= 10


class NomButton(Button):
    """
    button that creates a nom at a random point onscreen
    """
    def __init__(self, position, buttonlist):
        """
        replaces the default button image with the nom button image
        """
        Button.__init__(self, position, buttonlist)
        self.image = pygame.image.load("Images/nombutton.png")

    def get_pressed(self, window):
        """
        if player has enough money,
        creates an instance of the nom class at a random point onscreen
        reduces money by 10
        """
        if window.model.money >= 10:
            noms.Nom(random.random()*window.view.width, random.random()*window.view.height, window)
            window.model.money -= 10


class RawrButton(Button):
    """
    button that creates a rawr at a random point onscreen
    """
    def __init__(self, position, buttonlist):
        """
        replaces the default button image with the rawr button image
        """
        Button.__init__(self, position, buttonlist)
        self.image = pygame.image.load("Images/rawrbutton.png")

    def get_pressed(self, window):

        """
        if player has enough money,
        creates an instance of the rawr class at a random point onscreen
        reduces money by 10
        """
        if window.model.money >= 10:
            rawrs.Rawr(random.random()*window.view.width, random.random()*window.view.height, window)
            window.model.money -= 10


class DesertDuneButton(Button):
    """
    button that creates a Desert Dune at a random point onscreen
    """
    def __init__(self, position, buttonlist):
        """
        replaces the default button image with the desert dune button image
        """
        Button.__init__(self, position, buttonlist)
        self.image = pygame.image.load("Images/desertdune_button.png")

    def get_pressed(self, window):
        """
        if player has enough money,
        creates an instance of the desert dune class at a random point onscreen
        reduces money by 5
        """
        if window.model.money >= 5:
            environment.DesertDune(random.randint(0, window.view.width - 94), random.randint(50, window.view.height - 50), window)
            window.model.money -= 5


class RainforestTreeButton(Button):
    """
    button that creates a rainforest tree at a random point onscreen
    """
    def __init__(self, position, buttonlist):
        """
        replaces the default button image with the rainforest tree button image
        """
        Button.__init__(self, position, buttonlist)
        self.image = pygame.image.load("Images/rainforesttree_button.png")

    def get_pressed(self, window):
        """
        if player has enough money,
        creates an instance of the rainforest tree class at a random point onscreen
        reduces money by 5
        """
        if window.model.money >= 5:
            environment.RainforestTree(random.randint(0, window.view.width - 100), random.randint(50, window.view.height - 150), window)
            window.model.money -= 5


class PuddleButton(Button):
    """
    button that creates a random-sized puddle at a random point onscreen
    """
    def __init__(self, position, buttonlist):
        """
        replaces the default button image with the puddle button image
        """
        Button.__init__(self, position, buttonlist)
        self.image = pygame.image.load("Images/waterbutton.png")

    def get_pressed(self, window):
        """
        if player has enough money,
        creates an instance of the puddle class at a random point onscreen
        reduces money by 5
        """
        if window.model.money >= 5:
            puddles.Puddle(random.randint(0, window.view.width - 60), random.randint(50, window.view.height - 40), window)
            window.model.money -= 5


class DesertPalmTreeButton(Button):
    """
    button that creates a desert palm tree at a random point onscreen
    """
    def __init__(self, position, buttonlist):
        """
        replaces the default button image with the desert palm tree button image
        """
        Button.__init__(self, position, buttonlist)
        self.image = pygame.image.load("Images/desertpalmtreebutton.png")

    def get_pressed(self, window):
        """
        if player has enough money,
        creates an instance of the desert palm tree class at a random point onscreen
        reduces money by 5
        """
        if window.model.money > 5:
            environment.DesertPalmTree(random.randint(0, window.view.width - 100), random.randint(50, window.view.height - 150), window)
            window.model.money -= 5


class DesertHillButton(Button):
    """
    button that creates a desert hill at a random point onscreen
    """
    def __init__(self, position, buttonlist):
        """
        replaces the default button image with the desert hill button image
        """
        Button.__init__(self, position, buttonlist)
        self.image = pygame.image.load("Images/deserthillbutton.png")

    def get_pressed(self, window):
        """
        if player has enough money,
        creates an instance of the desert hill class at a random point onscreen
        reduces money by 5
        """
        if window.model.money >= 5:
            environment.DesertHill(random.randint(0, window.view.width - 100), random.randint(50, window.view.height - 150), window)
            window.model.money -= 5


class ArcticDesertDuneButton(Button):
    """
    button that creates an arctic dune at a random point onscreen
    """
    def __init__(self, position, buttonlist):
        """
        replaces the default button image with the arctic dune button image
        """
        Button.__init__(self, position, buttonlist)
        self.image = pygame.image.load("Images/arcticdesertdunebutton.png")

    def get_pressed(self, window):
        """
        if player has enough money,
        creates an instance of the arctic desert dune class at a random point onscreen
        reduces money by 5
        """
        if window.model.money >= 5:
            environment.ArcticDesertDune(random.randint(0, window.view.width - 94), random.randint(50, window.view.height - 50), window)
            window.model.money -= 5

class Buttons (pygame.sprite.Group):
    """
    list of all buttons for drawing/updates
    """
