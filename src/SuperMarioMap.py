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
    # @param result, array of chars which represents the map
    #
    # @return result array
    ##
    def toString(self):

        # Preparing the upper-border of the output
        result = "#" * (len(self.environment) + 2)
        result += "\n"

        # Looping through the 15x16 array and printing its symbols while also creating a border with # symbols around it
        for x in self.environment:
            result += "#"
            for y in x:
                result += y
            result += "#\n"

        # Preparing the lower-border of the output
        result += "#" * (len(self.environment) + 2)
        result += "\n"

        return result

    ##
    # This method resets the simplified version of the game by overwriting it with an empty 15x16 array
    #
    # @author Wolfgang Mair
    ##
    def resetMap(self, shouldCreateAnArray=False):
        # https://stackoverflow.com/questions/31498784/performance-difference-between-filling-existing-numpy-array-and-creating-a-new-o
        if (shouldCreateAnArray):
            self.environment = np.array([[" "] * 16] * 15)
        else:
            # self.environment[:] = " "
            self.environment.fill(" ")


    ##
    # This method receives a dictionary with characters as Key and Locations as value. It sets the character
    # at the specified location in the string map.
    # @author Lukas Geyrhofer
    # @param detectedAssetsAndCorrespondingSymbol
    ##
    def changeMapAll(self, detectedAssetsAndCorrespondingSymbol):
        for detectionSymbol, location in detectedAssetsAndCorrespondingSymbol.items():
            for pt in zip(*location[::-1]):

                x = int(np.floor(pt[0] / 16))
                y = int(np.floor(pt[1] / 16))

                self.environment[y][x] = detectionSymbol

                if detectionSymbol == "P":
                    for i in range(y, 15, 1):
                        self.environment[i][x] = detectionSymbol

                        if x < 15:
                            self.environment[i][x + 1] = detectionSymbol

                if detectionSymbol == "L":
                    for i in range(1, 4):
                        if x + i < 15:
                            self.environment[y][x + i] = detectionSymbol
