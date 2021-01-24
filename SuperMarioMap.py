import numpy as np
import SuperMarioDisplay

##
# This class deals with everything related to the simplification and its corresponding representation of the game.
#
# @author Wolfgang Mair, Lukas Geyrhofer
# @version 18. January 2021
##
class Mario2DMap():

    ##
    # Constructor that creates an empty 16x16 array
    #
    # @author Wolfgang Mair
    ##
    def __init__(self):
        self.environment = np.array([[" "] * 16] * 15)

    ##
    # This method prints the simplified version of the game which is saved in a 16x15 array
    #
    # @author Wolfgang Mair, Lukas Geyrhofer
    # @param niceConsoleOutput A boolean parameter which makes the output prettier for windows systems
    ##
    def printEnvironment(self, niceConsoleOutput):
        # Preparing the upper-border of the output
        erg = "#" * (len(self.environment)+2)
        erg += "\n"
        # Looping through the 16x16 array and printing its symbols while also creating a border with # symbols around it
        for x in self.environment:
            erg += "#"
            for y in x:
                erg += y
            erg += "#\n"
        erg += "#" * (len(self.environment)+2)
        erg += "\n"

        # when true use another display method more suitable for windows systems
        if niceConsoleOutput:
            SuperMarioDisplay.print_nice(erg)
        else:
            print(erg)

    ##
    # This method resets the simplified version of the game by overwriting it with an empty 16x15 array
    #
    # @author Wolfgang Mair
    ##
    def reloadEnvironment(self):
        self.environment = np.array([[" "] * 16] * 15)

    ##
    # This method changes specific places of the the simplified version of the game which is saved as a 16x15 array
    #
    # @author Wolfgang Mair, Lukas Geyrhofer
    # @param loc A tupel which holds x and y coordinates of elements to be saved into the simplified version of the game
    # @param symbol A char parameter that defines the symbol in which the elements should be represented
    ##
    def changeEnvironment(self, loc, symbol):

        # iterate through every x and y coordinates saved in the tuple loc
        for pt in zip(*loc[::-1]):
            # make the coordinates fit in a 16x15 array
            x = int(np.floor(pt[0] / 16))
            y = int(np.floor((pt[1] / 16)))
            # save on the corresponding array-slot the symbol character
            self.environment[y][x] = symbol
            # if it happens to be a pipe add extra symbols (since only the top-left part gets recognized)
            if symbol == "P":
                # add more pipe symbols until you reach the lowest part of the array
                for i in range(y, 15, 1):
                    self.environment[i][x] = symbol
                    # make the pipe 2 paces wide
                    if x < 15:
                        self.environment[i][x+1] = symbol
