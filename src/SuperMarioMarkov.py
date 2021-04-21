
##
# This class deals with everything related to the simplification and its corresponding representation of the game.
#
# @author Wolfgang Mair, Florian Weiskirchner
# @version 21. April 2021
##
class SuperMarioMarkov():

    ##
    # A constructor that initializes the 2DMap, the state dictionary and the State array size
    # @author Wolfgang Mair
    #
    # @param theMap A SuperMarioMap object used for the decision method
    ##
    def __init__(self, theMap):
        self.map = theMap
        self.markovStateDictionary = {}
        self.markovStateArraySize = 0

    ##
    # A method that reads all the states and its corresponding movement action into the class from a file
    # @author
    ##
    def readMarkovFile(self):
        # TODO
        # Delete the return
        return False

    ##
    # A method that uses the current state and its stateDictionary to return its corresponding movement action.
    # @author
    #
    # @param state The current State of the game to be compared to the state Dictionary
    # @return The movement action that should be used in form of its corresponding index number
    ##
    def decision(self, state):
        #TODO
        return 0