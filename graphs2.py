import pygame


class graphs():
    """
    handles all the stats and graphing
    """

    def __init__(self):
        #counts the number of times this has been called
        self.times = 0
        self.population = [0] * 18
        self.pointlist = [(0,0)] * 18
        print self.pointlist
        for i in range(0, 18):
            self.pointlist[i] = (814 + 10*i, 0)

    def writestats(self, window):
        """
        displays currency amount, number of living bugs, time used, and time until win
        """
        ccounter = window.view.font.render('Money: $' + str(window.model.money), 1, (255, 255, 255))
        window.view.screen.blit(ccounter, (window.view.width + 14, 10))
        bcounter = window.view.font.render('Living Bugs: ' + str(len(window.model.buglist)), 1, (255, 255, 255))
        window.view.screen.blit(bcounter, (window.view.width + 14, 25))
        #environment stats

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
        #text
        self.writestats(window)