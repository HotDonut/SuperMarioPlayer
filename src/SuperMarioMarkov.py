import numpy as np


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
    def __init__(self, theMap, markovStatesPath, markovStateDimensions):
        self.map = theMap
        self.markovStateDictionary = {}
        self.markovStateArraySize = 0
        self.markovStateDimensions = markovStateDimensions
        self.readMarkovFile(markovStatesPath)
        self.markovStringOld = ""
        self.noMovementFrameCount = 0
        self.marioJumpStatus = 0
        self.marioHeight = 0

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

    ##
    # A method that slices the current state in the map and prepares it
    # for the decision method and returns the corresponding movement action.
    #
    # @author Wolfgang Mair, Lukas Geyrhofer
    #
    # @param currentHeight The current height (y_pos) of Mario
    # @return The movement action that should be used in form of its corresponding index number
    ##
    def nextStep(self, currentHeight):
        # Needs to be called for jump converter to work, Checks if Mario is currently jumping
        self.updateJumpStatus(currentHeight)

        #Get Mario coordinates
        marioCoord = self.getMarioCoordinates()

        #if no mario was found return default movement 0 (Movement: NOOP)
        if marioCoord.size == 0:
            return 0

        # Prepare variables
        markovString = ""

        for stateSize in self.markovStateDimensions:
            # Slice the state around mario
            stateSliced = self.sliceState(self.getMarioCoordinates(), stateSize)
            # Generate the markovString that can be used for the StateDictionary and is generated from the sliced array
            markovString = self.convertArrayToDictionaryString(stateSliced)
            # If
            if self.markovStateDictionary.get(markovString) != None:
                # Return the found MovementAction
                return self.jumpConverter(self.markovStateDictionary.get(markovString), self.marioJumpStatus)

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
        print('\n'.join(markovString[i:i+length] for i in range(0, len(markovString), length)))

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

    ##
    # Method that updates Marios jumping status to 0, 1 or 2 if he is currently jumping, falling or on the floor.
    # This method does not work properly if there is an actual slope in the game or if it is not called for
    # every frame exactly once!
    # (since there are only steps in Super Mario Bros. this method should work fine)
    #
    # 0 ... Mario is on the floor
    # 1 ... Mario is jumping up
    # 2 ... Mario is falling
    #
    # @author Wolfgang Mair
    ##
    def updateJumpStatus(self, currentHeight):
        if currentHeight == self.marioHeight and self.marioJumpStatus == 2:
            self.marioJumpStatus = 0
        if currentHeight < self.marioHeight:
            self.marioJumpStatus = 2
        if currentHeight > self.marioHeight:
            self.marioJumpStatus = 1
        self.marioHeight = currentHeight
        #print("Mario Jump status: {}".format(self.marioJumpStatus))

    ##
    # Method that converts currently move method depending on the current jump status of Mario
    # This Method prevents the Bug that Mario can't jump again while holding the jump button
    # By transforming all jump actions to their corresponding non jump action while falling it solves this problem
    #
    # @author Wolfgang Mair
    #
    # @param integer of the current movement action
    # @param integer of the current jump status
    # @return   The converted movement action
    ##
    def jumpConverter(self, movementAction, jumpStatus):
        # Mario is currently falling
        if jumpStatus == 2:
            #Mario tries currently to jump
            if movementAction == 2 or movementAction == 4 or movementAction == 7 or movementAction == 9:
                #return same Movementinput without jump
                return movementAction-1
            #Mario only wants to jump without additional movement
            if movementAction == 5:
                #return no movement at all
                return 0
        # Mario is currently not falling so any movement may be executed
        return movementAction

    ##
    # Method that returns the current index coordinates of mario in the map grid
    # This method returns empty array if no Mario was found
    #
    # @author Wolfgang Mair
    #
    # @return   An array with x and y grid-index values
    ##
    def getMarioCoordinates(self):

        marioTuple = np.where(self.map.environment == 'M')

        if len(marioTuple[0]) == 0:
            return np.array([])

        coord = np.array([marioTuple[0][0] , marioTuple[1][0]])
        return coord

    ##
    # Method that returns the a sliced version of the map array
    # Returns an empty array when the slice values exceed the possible grid-index values of the map
    #
    # @author Wolfgang Mair
    #
    # @param startValues An array with x and y values that represent the center index from which the state should be cut
    # @param stateSizeValues An array with x and y size of the new state with x on index 0 and y on index 1
    # @return   An array with x and y grid-index values
    ##
    def sliceState(self, startValues, stateSizeValues):

        # Calculate the shift values for the slice
        smallX = bigX = int(stateSizeValues[0]/2)
        smallY = bigY = int(stateSizeValues[1]/2)

        # Increase the bigger shiftValues by 1 when size is uneven
        if stateSizeValues[0] % 2 == 1:
            bigX += 1

        if stateSizeValues[1] % 2 == 1:
            bigY += 1

        # Check if sliced state would be out of bounds of the map
        if startValues[0]-smallX < 0 or startValues[1]-smallY < 0 or startValues[0]+bigX > 14 or startValues[1]+bigY > 15:
            return np.array([])

        # Slice the state around the startValues and return the new sliced map-array
        state = self.map.environment[startValues[0]-smallX : startValues[0]+bigX, startValues[1]-smallY:startValues[1]+bigY]
        return state

    ##
    # Method that converts an array to a string that can be used by the StateDictionary as a key
    #
    # @author Wolfgang Mair, Lukas Geyrhofer
    #
    # @param arrayInput An array with symbols
    # @return   A string consisting only of the symbols of the array
    ##
    def convertArrayToDictionaryString(self, arrayInput):
        markovString = ""

        for arrayRow in arrayInput:
            for character in arrayRow:
                markovString += character

        return markovString