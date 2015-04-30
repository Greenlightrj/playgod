import pygame


class graphs():
    """
    handles all the stats and graphing
    """

    def __init__(self):
        pass

    def writestats(self, window):
        """
        displays currency amount, number of living bugs, time used, and time until win
        """
        ccounter = window.view.font.render('Money: $' + str(window.model.money), 1, (255, 255, 255))
        window.view.screen.blit(ccounter, (window.view.width + 14, 10))
        bcounter = window.view.font.render('Living Bugs: ' + str(len(window.model.buglist)), 1, (255, 255, 255))
        window.view.screen.blit(bcounter, (window.view.width + 14, 25))

    def redraw(self, window):
        #draw background box
        pygame.draw.rect(window.view.screen, (69, 69, 69), [window.view.width, 0, window.view.graphwidth, window.view.height])
        pygame.draw.line(window.view.screen, (113, 113, 113), (window.view.width, 0), (window.view.width, window.view.height), 4)
        self.writestats(window)