import pygame
"""
Yes, I could have used a lot more loops and functions to reduce the copypasted stuff in this.
"""

class graphs():
    """
    handles all the stats and graphing
    """

    def __init__(self):
        #counts the number of times this has been called
        self.times = 0
        self.population = [0] * 18
        self.pointlist = [(0,0)] * 18
        for i in range(0, 18):
            self.pointlist[i] = (814 + 10*i, 0)
        self.colorspread = [0] * 30
        self.speedspread = [0] * 10
        self.toothspread = [0] * 10
        self.furspread = [0] * 10
        self.camelspread = [0] * 10


    def writestats(self, window):
        """
        displays currency amount, number of living bugs, time used, and time until win
        """
        ccounter = window.view.font.render('Money: $' + str(window.model.money), 1, (255, 255, 255))
        window.view.screen.blit(ccounter, (window.view.width + 14, 10))
        bcounter = window.view.font.render('Living Bugs: ' + str(len(window.model.buglist)), 1, (255, 255, 255))
        window.view.screen.blit(bcounter, (window.view.width + 14, 25))
        #environment stats
        #average stats

    def poptracker(self, window):
        """
        keeps track of previous population
        """
        self.times += 1
        if self.times >= 80:
            self.times = 0
            self.population.append(len(window.model.buglist))
            self.population.pop(0)
            for i in range(0, 18):
                self.pointlist[i] = (window.view.width + 14 + 10*i, 150 - self.population[i])

    def stattracker(self, window):
        self.colorspread = [0] * 30
        self.colorlist = 0
        self.speedspread = [0] * 9
        self.speedlist = [(0,0)] * 9
        self.toothspread = [0] * 9
        self.toothlist = [(0,0)] * 9
        self.furspread = [0] * 9
        self.furlist = [(0,0)] * 9
        self.camelspread = [0] * 9
        self.camellist = [(0,0)] * 9
        self.redspread = [0] * 9
        self.redlist = [(0,0)] * 9
        self.greenspread = [0] * 9
        self.greenlist = [(0,0)] * 9
        self.bluespread = [0] * 9
        self.bluelist = [(0,0)] * 9

        for bug in window.model.buglist:
            for (listy, stat) in [(self.speedspread,bug.fleeing), (self.toothspread,bug.hunting), (self.furspread,bug.fuzz), (self.camelspread,bug.camelfactor)]:
                for i in range(0, 9):
                    if max(stat)*10 >i and max(stat)*10 <= i+1:
                        listy[i] += 1
            for (num, listy) in [(0, self.redspread), (1, self.greenspread), (2, self.bluespread)]:
                for i in range(0, 9):
                    if bug.color[num]/25.5 > i and bug.color[num]/25.5 <= i+1:
                        print bug.color[num]/255.0
                        listy[i] += 1
        for i in range(0,9):
            self.speedlist[i] = (window.view.width + 14 + 20 * i, 220 -  2* self.speedspread[i])
            self.toothlist[i] = (window.view.width + 14 + 20 * i, 300 - 2 * self.toothspread[i])
            self.furlist[i] = (window.view.width + 14 + 20 * i, 380 - 2 * self.furspread[i])
            self.camellist[i] = (window.view.width + 14 + 20 * i, 460 - 2 * self.camelspread[i])
            self.redlist[i] = (window.view.width + 14 + 20 * i, 540 - 2 * self.redspread[i])
            self.greenlist[i] = (window.view.width + 14 + 20 * i, 540 - 2 * self.greenspread[i])
            self.bluelist[i] = (window.view.width + 14 + 20 * i, 540 - 2 * self.bluespread[i])

    def redraw(self, window):
        """
        draws the elements of the graph box
        """
        #draw background box
        pygame.draw.rect(window.view.screen, (69, 69, 69), [window.view.width, 0, window.view.graphwidth, window.view.height])
        pygame.draw.line(window.view.screen, (113, 113, 113), (window.view.width, 0), (window.view.width, window.view.height), 4)
        #population graph
        self.poptracker(window)
        pygame.draw.lines(window.view.screen, (255, 255, 255), False, self.pointlist, 2)
        pygame.draw.line(window.view.screen, (0, 0, 0), (window.view.width + 14, 150), (window.view.drawwidth - 10, 150), 2)
        #deaths bar graph
        #average stats graphs
        self.stattracker(window)
            #speed
        speedname = window.view.font.render(('Speed:'), 1, (255, 255, 255))
        window.view.screen.blit(speedname, (window.view.width + 14, 175))
        pygame.draw.lines(window.view.screen, (255, 255, 255), False, self.speedlist, 2)
        pygame.draw.line(window.view.screen, (0, 0, 0), (window.view.width + 14, 220), (window.view.drawwidth - 10, 220), 2)
            #teeth
        toothname = window.view.font.render(("Attack/Defense:"), 1, (255, 255, 255))
        window.view.screen.blit(toothname, (window.view.width + 14, 245))
        pygame.draw.lines(window.view.screen, (255, 255, 255), False, self.toothlist, 2)
        pygame.draw.line(window.view.screen, (0, 0, 0), (window.view.width + 14, 300), (window.view.drawwidth - 10, 300), 2)
            #fur
        furname = window.view.font.render(("Fur:"), 1, (255, 255, 255))
        window.view.screen.blit(furname, (window.view.width + 14, 325))
        pygame.draw.lines(window.view.screen, (255, 255, 255), False, self.furlist, 2)
        pygame.draw.line(window.view.screen, (0, 0, 0), (window.view.width + 14, 380), (window.view.drawwidth - 10, 380), 2)
            #camel
        camelname = window.view.font.render(("Drought Resistance:"), 1, (255, 255, 255))
        window.view.screen.blit(camelname, (window.view.width + 14, 405))
        pygame.draw.lines(window.view.screen, (255, 255, 255), False, self.camellist, 2)
        pygame.draw.line(window.view.screen, (0, 0, 0), (window.view.width + 14, 460), (window.view.drawwidth - 10, 460), 2)
            #color
        colorname = window.view.font.render(("Color:"), 1, (255, 255, 255))
        window.view.screen.blit(colorname, (window.view.width + 14, 485))
        pygame.draw.lines(window.view.screen, (255, 0, 0), False, self.redlist, 2)
        pygame.draw.lines(window.view.screen, (0, 255, 0), False, self.greenlist, 2)
        pygame.draw.lines(window.view.screen, (0, 0, 255), False, self.bluelist, 2)
        pygame.draw.line(window.view.screen, (0, 0, 0), (window.view.width + 14, 540), (window.view.drawwidth - 10, 540), 2)
        #text
        self.writestats(window)