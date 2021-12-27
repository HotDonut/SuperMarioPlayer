import matplotlib.pyplot as plt


class SuperMarioPlot:

    def __init__(self):
        self.count = 5
        self.count2 = 0
        self.macroList = []
        self.deathList = []
        self.xlabel = 'x-Achse'
        self.ylabel = 'y-Achse'

    def printPlot(self):
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.show()

    def bestRunPlot(self):
        return

    def sessionPlot(self, macroCycleCount, deathCount):

        self.macroList.append(macroCycleCount)
        self.deathList.append(deathCount)
        self.count2 += 1
        if self.count2 >= self.count:
            self.count2 = 0
            plt.bar(self.macroList, self.deathList)
            self.xlabel = 'Macro Cycle Count'
            self.ylabel = 'Death Count per Cycle'
            self.printPlot()
