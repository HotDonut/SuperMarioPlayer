import numpy as np
import SuperMarioDisplay

class Mario2DMap():
    marioNotFound = 0

    def __init__(self):
        self.environment = np.array([[" "] * 16] * 16)

    def printEnvironment(self, niceConsoleOutput):
        erg = "#" * (len(self.environment)+2)
        erg += "\n"
        for x in self.environment:
            erg += "#"
            for y in x:
                erg += y
            erg += "#\n"
        erg += "#" * (len(self.environment)+2)
        erg += "\n"
        if niceConsoleOutput:
            SuperMarioDisplay.print_nice(erg)
        else:
            print(erg)

    def reloadEnvironment(self):
        self.environment = np.array([[" "] * 16] * 16)

    def changeEnvironment(self, loc, symbol):
        i = 0

        for pt in zip(*loc[::-1]):
            x = int(np.floor(pt[0] / 16))
            y = int(np.floor((pt[1] / 16)+1))
            self.environment[y][x] = symbol
            if symbol == "P":
                for i in range(y, 15, 1):
                    self.environment[i][x] = symbol
                    if x < 15:
                        self.environment[i][x+1] = symbol

        if (i == 0):
            self.marioNotFound = self.marioNotFound + 1
