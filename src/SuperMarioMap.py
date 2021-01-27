import numpy as np

##
# This class deals with everything related to the simplification and its corresponding representation of the game.
#
# @author Wolfgang Mair, Lukas Geyrhofer
# @version 18. January 2021
##
class Mario2DMap():

    ##
    # Constructor that creates an empty 15x16 array
    #
    # @author Wolfgang Mair
    ##
    def __init__(self):
        self.resetMap(True)

    ##
    # This method prints the simplified version of the game which is saved in a 15x16 array
    #
    # @author Wolfgang Mair, Lukas Geyrhofer
    # @param niceConsoleOutput A boolean parameter which makes the output prettier for windows systems
    ##
    def toString(self):

        # Preparing the upper-border of the output
        result = "#" * (len(self.environment)+2)
        result += "\n"
        
        # Looping through the 15x16 array and printing its symbols while also creating a border with # symbols around it
        for x in self.environment:
            result += "#"
            for y in x:
                result += y
            result += "#\n"
        
        # Preparing the lower-border of the output
        result += "#" * (len(self.environment)+2)
        result += "\n"

        return result

    ##
    # This method resets the simplified version of the game by overwriting it with an empty 15x16 array
    #
    # @author Wolfgang Mair
    ##
    def resetMap(self, shouldCreateAnArray=False):
        # https://stackoverflow.com/questions/31498784/performance-difference-between-filling-existing-numpy-array-and-creating-a-new-o
        if(shouldCreateAnArray):
            self.environment = np.array([[" "] * 16] * 15)
        else:
            #self.environment[:] = " "
            self.environment.fill(" ")
            

    ##
    # This method changes specific places of the the simplified version of the game which is saved as a 15x16 array
    #
    # @author Wolfgang Mair, Lukas Geyrhofer
    # @param loc A tupel which holds x and y coordinates of elements to be saved into the simplified version of the game
    # @param symbol A char parameter that defines the symbol in which the elements should be represented
    ##
    def changeMap(self, location, symbol):

        # iterate through every x and y coordinates saved in the tuple loc
        for pt in zip(*location[::-1]):

            # make the coordinates fit in a 15x16 array
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
