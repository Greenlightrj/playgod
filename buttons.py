"""
Buttons classes
"""
import pygame
import random
import bugs
import noms
import rawrs
import environment

class Button (pygame.sprite.Sprite):
    """
    parent class for Buttons
    """
    def __init__(self, position, buttonlist):
        pygame.sprite.Sprite.__init__(self, buttonlist)
        self.x = position[0]
        self.y = position[1]
        self.image = pygame.image.load("button.png")
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.pressed = False

    def draw_icon(self, window):
        self.icon.blit(window.view.screen, (self.x + 5, self.y + 5))

    def get_pressed(self):
        pass

class BugButton(Button):
    """
    button that creates a bug at a random point onscreen
    """
    def __init__(self, position, buttonlist):
        Button.__init__(self, position, buttonlist)
        self.image = pygame.image.load("bugbutton.png")
        #self.rect = self.image.get_rect()

    def get_pressed(self, window):
        bugs.Bug(random.random()*window.view.width, random.random()*window.view.height, window)

class NomButton(Button):
    """
    button that creates a nom at a random point onscreen
    """
    def __init__(self, position, buttonlist):
        Button.__init__(self, position, buttonlist)
        #replace bugbutton with nombutton
        self.image = pygame.image.load("bugbutton.png")
        #self.rect = self.image.get_rect()

    def get_pressed(self, window):
        noms.Nom(random.random()*window.view.width, random.random()*window.view.height, window)

class RawrButton(Button):
    """
    button that creates a rawr at a random point onscreen
    """
    def __init__(self, position, buttonlist):
        Button.__init__(self, position, buttonlist)
        #replace bugbutton with rawrbutton
        self.image = pygame.image.load("bugbutton.png")
        #self.rect = self.image.get_rect()

    def get_pressed(self, window):
        rawrs.Rawr(random.random()*window.view.width, random.random()*window.view.height, window)

class DesertDuneButton(Button):
    """
    button that creates a rawr at a random point onscreen
    """
    def __init__(self, position, buttonlist):
        Button.__init__(self, position, buttonlist)
        #replace bugbutton with rawrbutton
        self.image = pygame.image.load("desertdune_button.png")
        #self.rect = self.image.get_rect()

    def get_pressed(self, window):
        environment.DesertDune(random.random()*window.view.width, random.random()*window.view.height, window)

class RainforestTreeButton(Button):
    """
    button that creates a rawr at a random point onscreen
    """
    def __init__(self, position, buttonlist):
        Button.__init__(self, position, buttonlist)
        #replace bugbutton with rawrbutton
        self.image = pygame.image.load("rainforesttree_button.png")
        #self.rect = self.image.get_rect()

    def get_pressed(self, window):
        environment.RainforestTree(random.random()*window.view.width, random.random()*window.view.height, window)

class Buttons (pygame.sprite.Group):
    """
    list of all buttons for drawing/updates
    """
