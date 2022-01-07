import matplotlib.pyplot as plt
import numpy as np


class SuperMarioPlot:

    def __init__(self):
        self.count = 1
        self.count2 = 0
        self.xValueList = []
        self.yValueList = []
        self.xlabel = 'x-Achse'
        self.ylabel = 'y-Achse'
        self.path = './plot/foo.png'

    def printPlot(self):
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.savefig(self.path)
        #plt.show()

    def bestRunPlot(self):
        return

    def sessionPlot(self, xValue, yValue, color):
        self.xValueList.append(xValue)
        self.yValueList.append(yValue)
        self.count2 += 1
        if self.count2 >= self.count:
            self.count2 = 0
            plt.figure()
            plt.bar(self.xValueList, self.yValueList, color=color)
            self.printPlot()

    def deathCountPlot(self, xValue, yValue):
        self.xlabel = 'Macro Cycle Count'
        self.ylabel = 'Death Count per Cycle'
        self.path = './plot/DeathCount.png'
        self.sessionPlot(xValue, yValue, 'green')


    def bestXPlot(self, xValue, yValue):
        self.xlabel = 'Macro Cycle Count'
        self.ylabel = 'Best X per Cycle'
        self.path = './plot/bestXperCycle.png'
        self.sessionPlot(xValue, yValue, 'red')


