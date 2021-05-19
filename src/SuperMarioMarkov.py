import numpy as np
import ast
import json

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
    def __init__(self, theMap, filePath):
        self.map = theMap
        self.markovStateDictionary = {}
        self.markovStateArraySize = 0
        self.readMarkovFile(filePath)

    ##
    # A method that reads all the states and its corresponding movement action into the class from a file
    # @author Wolfgang Mair
    ##
    def readMarkovFile(self, filePath):

        fileRead = open(filePath, "r")
        fileContents = fileRead.read()

        self.markovStateDictionary = ast.literal_eval(fileContents)

        '''
        #Prototype test successful
        
        state = np.array([[" "," "," "],
        [" ","M"," "],
        ["@","@","@"]])

        state2 = np.array([[" ", " ", " "],
                          [" ", "M", "G"],
                          ["@", "@", "@"]])

        stateString = np.array2string(state)
        stateString2 = np.array2string(state2)

        self.markovStateDictionary[stateString] = 1
        self.markovStateDictionary[stateString2] = 2

        file = open("Markov_States.txt","w")
        file.write(json.dumps(self.markovStateDictionary))
        file.close()

        fileRead = open("Markov_States.txt","r")
        fileContents = fileRead.read()
        fileDict = ast.literal_eval(fileContents)

        diff = np.array([[" ", " ", " "],
                          [" ", "M", "G"],
                          ["@", "@", "@"]])

        print(self.markovStateDictionary.get(np.array2string(diff)))
        print(self.markovStateDictionary)
        print(fileDict.get(np.array2string(diff)))
        print(fileDict)

        '''

    ##
    # A method that uses the state and its stateDictionary to return its corresponding movement action.
    # @author Wolfgang Mair
    #
    # @param state The current State of the game to be compared to the state Dictionary
    # @return The movement action that should be used in form of its corresponding index number
    ##
    def decision(self, state):
        keyState = np.array2string(state)
        return self.markovStateDictionary[keyState]

    ##
    # A method that slices the current state in the map and prepares it for the decision method and returns the corresponding movement action.
    # @author Wolfgang Mair
    #
    # @return The movement action that should be used in form of its corresponding index number
    ##
    def nextStep(self):
        #Get Mario coordinates
        findMario = np.where(self.map.environment == 'M')
        #Slice the state around mario into a 3x3 state
        state3x3 = self.map.environment[findMario[0][0]-1:findMario[0][0]+2,findMario[1][0]-1:findMario[1][0]+2]

        #sliced array in string form print
        #print(np.array2string(state3x3))

        #print corresponding movement if found
        #print(self.markovStateDictionary.get(np.array2string(state3x3)))

        #Search for state in dictionary or return default if not
        if(self.markovStateDictionary.get(np.array2string(state3x3)) != None):
            return self.markovStateDictionary.get(np.array2string(state3x3))
        else:
            #Set to 0 to find unknown states
            return 1