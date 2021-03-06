"""
Class to handle all the statistics graphing pane
"""

import pygame


class graphs():
    """
    handles all the stats and graphing
    """
    def __init__(self):
        """
        initializes counters and lists
        """
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
        self.textlist = []

    def write(self, window, text, position):
        """
        writes the text string to the window at the given position in white, preloaded font
        """
        x = window.view.font.render(str(text), 1, (255, 255, 255))
        window.view.screen.blit(x, (position))

    def writestats(self, window):
        """
        displays currency amount, number of living bugs, and environment stats
        in the top right corner
        """
        stats = ['Money: $' + str(window.model.money), 'Living Bugs: ' + str(len(window.model.buglist)), 'Heat: ' + str(int(window.model.heat/2.55)) + '%', 'Moisture: ' + str(int(window.model.wet/2.55)) + '%']
        heights = [10, 55, 25, 40]
        for (stat, height) in zip(stats, heights):
            self.write(window, stat, (window.view.width + 14, height))

    def poptracker(self, window):
        """
        keeps track of previous population
        draws population graph
        """
        self.times += 1
        if self.times >= 80:
            self.times = 0
            self.population.append(len(window.model.buglist))
            self.population.pop(0)
        for i in range(0, 18):
            self.pointlist[i] = (window.view.width + 14 + 10*i, 150 - self.population[i])
        pygame.draw.lines(window.view.screen, (255, 255, 255), False, self.pointlist, 2)
        pygame.draw.line(window.view.screen, (0, 0, 0), (window.view.width + 14, 150), (window.view.drawwidth - 10, 150), 2)

    def getstat(self, bug, statname):
        """
        takes the stat name for a given bug and returns the tuple value of that stat
        """
        statdict = {'Speed:': bug.fleeing, 'Attack/Defense:': bug.hunting, 'Fur:': bug.fuzz, 'Drought Resistance:': bug.camelfactor}
        return statdict[statname]

    def statplot(self, window, statname, height):
        """
        takes bug stat, and distance from top of screen
        draws graph in window
        """
        self.write(window, statname, (window.view.width + 14, height - 55))
        statspread = [0] * 9
        pointlist = [(0,0)] * 9
        for bug in window.model.buglist:
            for i in range(0, 9):
                stat = self.getstat(bug, statname)
                if max(stat)*10 > i and max(stat)* 10 <= i+1:
                    statspread[i] += 1
        for i in range(0,9):
            pointlist[i] = (window.view.width + 14 + 20*i, height - 2*statspread[i])
        pygame.draw.lines(window.view.screen, (255, 255, 255), False, pointlist, 2)
        pygame.draw.line(window.view.screen, (0, 0, 0), (window.view.width + 14, height), (window.view.drawwidth - 10, height), 2)


    def colorplot(self, window):
        """
        draws graph of the prevalence of color saturation stats
        """
        self.redspread = [0] * 9
        self.redlist = [(0,0)] * 9
        self.greenspread = [0] * 9
        self.greenlist = [(0,0)] * 9
        self.bluespread = [0] * 9
        self.bluelist = [(0,0)] * 9

        self.write(window,'Color', (window.view.width + 14, 485))

        for bug in window.model.buglist:
            for (num, listy) in [(0, self.redspread), (1, self.greenspread), (2, self.bluespread)]:
                for i in range(0, 9):
                    if bug.color[num]/25.5 > i and bug.color[num]/25.5 <= i+1:
                        listy[i] += 1
        for i in range(0,9):
            self.redlist[i] = (window.view.width + 14 + 20 * i, 540 - 2 * self.redspread[i])
            self.greenlist[i] = (window.view.width + 14 + 20 * i, 540 - 2 * self.greenspread[i])
            self.bluelist[i] = (window.view.width + 14 + 20 * i, 540 - 2 * self.bluespread[i])

        pygame.draw.lines(window.view.screen, (255, 0, 0), False, self.redlist, 2)
        pygame.draw.lines(window.view.screen, (0, 255, 0), False, self.greenlist, 2)
        pygame.draw.lines(window.view.screen, (0, 0, 255), False, self.bluelist, 2)
        pygame.draw.line(window.view.screen, (0, 0, 0), (window.view.width + 14, 540), (window.view.drawwidth - 10, 540), 2)

    def deathtracker(self, window):
        """
        calculations for bar graph of cause of bug death
        returns total number of deaths that have occurred if less than 18
        """
        totaldeath = window.model.starves + window.model.thirsts + window.model.rawrdeaths + window.model.nomdeaths + window.model.drowns + window.model.tempdeaths
        if totaldeath < 18:
            return 18
        else:
            return totaldeath

    def backgroundbox(self, window): 
        """
        draws the background box for the graphs pane
        """
        pygame.draw.rect(window.view.screen, (69, 69, 69), [window.view.width, 0, window.view.graphwidth, window.view.height])
        pygame.draw.line(window.view.screen, (113, 113, 113), (window.view.width, 0), (window.view.width, window.view.height), 4)

    def drawbar(self, deathindex, window):
        """
        takes cause of death and draws labeled graph bar in window
        """
        deaths = self.deathtracker(window)
        (color, title, length) = self.deathcolor(deathindex, window)
        height = 587 + 32*deathindex
        pygame.draw.rect(window.view.screen, color, [window.view.width + 14, height, length*180.0/deaths, 25])
        self.write(window, title, (window.view.width + 14, height))
        if deathindex == 0:
            self.write(window, 'Causes of Death', (window.view.width + 14, 565))

    def deathcolor(self, deathindex, window):
        """
        takes number of cause of death and returns color, title, and bar length as a tuple
        """
        deathbook = {2:((0, 170, 0), 'Thirst', window.model.thirsts), 3: ((100, 100, 100)), 4: ((0, 0, 250)), 5: ((250, 0, 0))}
        deathbook[0] = ((0, 0, 0), 'Starvation', window.model.starves)
        deathbook[1] = ((170, 170, 0), 'Thirst', window.model.thirsts)
        deathbook[2] = ((0, 170, 0), 'Rawr', window.model.rawrdeaths)
        deathbook[3] = ((100, 100, 100), 'Nom', window.model.nomdeaths)
        deathbook[4] = ((0, 0, 250), "Drowning", window.model.drowns)
        deathbook[5] = ((250, 0, 0), "Heat", window.model.tempdeaths)
        return deathbook[deathindex]

    def redraw(self, window):
        """
        draws the elements of the graph box
        """
        self.backgroundbox(window)
        self.poptracker(window)

        statnames= ['Speed:', "Attack/Defense:", "Fur:", "Drought Resistance:"]
        heights = [220, 300, 380, 460]
        for (statname, height) in zip(statnames, heights):
            self.statplot(window, statname, height)

        self.colorplot(window)

        for i in range(0, 6):
            self.drawbar(i, window)
        
        self.writestats(window)