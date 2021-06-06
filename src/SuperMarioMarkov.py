import numpy as np
import textwrap
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
        self.markovStringOld = ""
        self.noMovementFrameCount = 0

    ##
    # A method that reads all the states and its corresponding movement action into the class from a file
    # @author Wolfgang Mair, Lukas Geyrhofer
    ##
    def readMarkovFile(self, filePath):

        with open(filePath) as fileRead:
            lines = (line.rstrip() for line in fileRead)
            lines = list(line for line in lines if line)

        markovStateString = ""
        action = 0

        for line in lines:
            print(line)
            if "#" in line:
                if self.markovStateDictionary.get(markovStateString) != None:
                    raise Exception("Duplicated Markov State detected:", markovStateString)
                self.markovStateDictionary[markovStateString] = action
                print(markovStateString)
                print(action)
                markovStateString = ""
            else:
                if "Action" in line:
                    action = str(line).replace("Action: ", "")
                    action = int(action)
                else:
                    markovStateString += str(line).replace("-", " ")

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
    # A method that slices the current state in the map and prepares it for the decision method and returns the corresponding movement action.
    # @author Wolfgang Mair, Lukas Geyrhofer
    #
    # @return The movement action that should be used in form of its corresponding index number
    ##
    def nextStep(self):
        # Get Mario coordinates
        findMario = np.where(self.map.environment == 'M')

        if len(findMario) == 0:
            return 0

        # Slice the state around mario into a 3x3 state
        state3x3 = self.map.environment[findMario[0][0] - 1:findMario[0][0] + 2,
                   findMario[1][0] - 1:findMario[1][0] + 2]

        markovString = ""

        for array in state3x3:
            for character in array:
                markovString += character

        # check if Mario is stuck and release jump if he is
        if self.holdingJumpDirtyFix(markovString):
            return 1

        self.markovStringOld = markovString

        # print(markovString)
        # sliced array in string form print
        # print(np.array2string(state3x3))

        # print corresponding movement if found
        # print(self.markovStateDictionary.get(np.array2string(state3x3)))

        # Search for state in dictionary or return default if not
        if (self.markovStateDictionary.get(markovString) != None):
            return self.markovStateDictionary.get(markovString)
        else:
            # Set to 0 to find unknown states
            if len(markovString) % 3 == 0:
                self.printUnknownState(3, markovString)

            if len(markovString) % 5 == 0:
                self.printUnknownState(5, markovString)

            if len(markovString) % 7 == 0:
                self.printUnknownState(7, markovString)

            return 1

    ##
    # nicer Debug message for unknown State for different length of strings
    # @author Florian Weiskirchner
    #
    # @param length Length of each line which should be printed
    # @param markovString String of the unknown State
    ##
    def printUnknownState(self, length, markovString):
        markovString = str(markovString).replace(" ", "-")
        print("unknown state:")
        print(textwrap.fill(markovString, length))

    ##
    # Dirty Fix for the "Holding Jump when on the Ground" Problem
    # @author Lukas Geyrhofer
    #
    # @param String of the current sliced state
    # @return Boolean if Mario is stuck
    ##
    def holdingJumpDirtyFix(self, markovString):
        # print(self.noMovementFrameCount)
        if markovString == self.markovStringOld:
            self.noMovementFrameCount += 1
            if self.noMovementFrameCount == 20:
                self.noMovementFrameCount = 0
                return True
            else:
                return False
        else:
            self.noMovementFrameCount = 0
            return False
