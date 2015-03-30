"""
This is a test of drawing creatures based on their genetic attributes.
click to create a randomly generated bug with three attributes
Everything is super messy but it's just a proof of concept
don't copypaste this into the actual project
"""

import pygame
import random

pygame.init()
screen = pygame.display.set_mode([500,500])
buglist = []

class Bug():

    def __init__(self):
        """
        init with some random values to test drawing function
        """
        self.sexiness = random.random()
        self.fleeing = random.random()
        self.hunting = random.random()
        self.x = random.randint(0,500)
        self.y = random.randint(0,500)
        buglist.append(self)

    def draw(self):
        # brighter color for more sexiness
        color = [255*self.sexiness, 0, 0]
        # body
        pygame.draw.rect(screen, color, [self.x, self.y, 35, 30]) # the location is [ x from left , y from top, width, height]
        #eyes
        pygame.draw.rect(screen, [0,0,0], [self.x + 5, self.y + 5, 2, 2])
        pygame.draw.rect(screen, [0,0,0], [self.x + 10, self.y + 8, 4, 4])
        pygame.draw.rect(screen, [0,0,0], [self.x + 18, self.y + 8, 4, 4])
        pygame.draw.rect(screen, [0,0,0], [self.x + 25, self.y + 5, 2, 2])
        # longer legs for better fleeing
        leglength = 30*self.fleeing
        pygame.draw.rect(screen, color, [self.x, self.y + 30, 5, leglength])
        pygame.draw.rect(screen, color, [self.x + 10, self.y + 30, 5, leglength])
        pygame.draw.rect(screen, color, [self.x + 20, self.y + 30, 5, leglength])
        pygame.draw.rect(screen, color, [self.x + 30, self.y + 30, 5, leglength])
        # bigger teeth for better hunting
        toothlength = 10*self.hunting
        pygame.draw.rect(screen, [255,255,255], [self.x + 10, self.y + 15, 2, toothlength])
        pygame.draw.rect(screen, [255,255,255], [self.x + 20, self.y + 15, 2, toothlength])
        

        

# this stuff is super messy just to get it to run and test the concept don't use this in the actual project
running = True
while running == True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:               # If user clicked close
                running = False
            elif event.type == pygame.KEYDOWN:          # If user pressed a key
                if event.key == pygame.K_ESCAPE:        # escape key is an escape   
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # when mouse button is clicked
                if pygame.mouse.get_pressed()[0]:     # left mouse button click
                    Bug()
    screen.fill([0,0,0])        # makes background first
    for bug in buglist:
        bug.draw()
    pygame.display.flip() 