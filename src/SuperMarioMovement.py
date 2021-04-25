import numpy as np
from enum import Enum

##
# Enum class, helps to improve the readability from the code.
# Same moves like COMPLEX_MOVEMENT.
# can be referenced with ControllerMovement.NOOP.value to get the value from the Enum.
# @author Florian Weiskirchner
##


class ControllerMovement(Enum):
    NOOP = 0
    right = 1
    rightA = 2
    rightB = 3
    rightAB = 4
    A = 5
    left = 6
    leftA = 7
    leftB = 8
    leftAB = 9
    down = 10
    up = 11

##
# This class is responsible for every kind of movement the player makes. It also implements different
# movement strategies.
#
# @author Wolfgang Mair, Florian Weiskirchner, Emmanuel Najfar
# @version 18. January 2021
##


class Movement:

    # List of all possible (rational) inputs the player can make
    COMPLEX_MOVEMENT = [
        ['NOOP'],
        ['right'],
        ['right', 'A'],
        ['right', 'B'],
        ['right', 'A', 'B'],
        ['A'],
        ['left'],
        ['left', 'A'],
        ['left', 'B'],
        ['left', 'A', 'B'],
        ['down'],
        ['up'],
    ]
    
    def __init__(self, theMap):
        self.map = theMap

        self.reset()

    def reset(self):
        # The players X/Y coordinate
        self.positionMarioRow = 1000 # down there
        self.positionMarioCol = 1000 # down there

        # parameters which are late used at the movement
        self.jumpingStarted = False     # Mario started a jump
        self.jumpingLong = False        # Mario does a long jump
        self.leftTheFloorOnce = False   # Mario jumped

    ##
    # Based on the position of Mario, this method looks around him and tries too find other objects
    # @author Florian Weiskirchner
    #
    # @param oldYPositionMario is the Y Position from Mario in the last Move
    # @param ControllerMovement.[].value Which move should be used from the ControllerMovement(Enum)
    # @param isFalling is a bool which is true when Mario is falling and false when he is jumping or running
    # @param positionMario is a np array with the position from Mario in the map
    # @param positionMarioRow Y coordinate from Mario
    # @param positionMarioCol X coordinate from Mario
    # @param backOnTheFloorAfterJump this bool shows if Mario jumped an is back on the floor
    #
    # @return ControllerMovement.[].value as an int gets returned.
    ##

    def move(self):
        self.oldYPositionMario = self.positionMarioRow
        positionMario = np.where(self.map.environment == "M")
        self.positionMarioRow = positionMario[0]
        self.positionMarioCol = positionMario[1]

        try:
            backOnTheFloorAfterJump = self.leftTheFloorOnce and (self.underMe("@") or self.underMe("S") or self.underMe("B") or self.underMe("?"))
            if backOnTheFloorAfterJump:
                self.jumpingStarted = False
                self.leftTheFloorOnce = False
                return ControllerMovement.NOOP.value # this noop is important, because else you can not jump directly after a long-jump

            if self.jumpingStarted:
                self.leftTheFloorOnce = self.leftTheFloorOnce or self.underMe(" ")
                if self.jumpingLong:
                    return ControllerMovement.rightAB.value
                else:
                    return ControllerMovement.right.value

            # check whether the square in one row under and the same column mario contains
            # the letter "P" in the array
            # if yes, there is a Pipe under mario, therefore the respective function will be called
            if self.underMe("P"):
                return self.jumpShort()

            # check whether the square in the any row as and one column in front of mario contains
            # the letter "P" in the array
            # if yes, there is a Pipe in front of mario, therefore the respective function will be called
            if self.inFrontOfMeInFullColumn("P", 3):
                return self.jumpLong()

            # check whether the square one column in front and one row below mario is empty in the array
            # if yes, there is a pit in front of mario, therefore the respective function will be called
            if self.underMeUpcoming(" "):
                return self.jumpLong()

            # check whether the square in any row and one column in front of mario contains
            # the letter "S" in the array
            # if yes, there is a stair in front of mario, therefore the respective function will be called
            if self.inFrontOfMe("S", 2):
                return self.jumpShort()

            # check whether the square in any row and one column in front of mario contains
            # the letter "G" in the array
            # if yes, there is a Goomba in front of mario, therefore the respective function will be called
            if self.inFrontOfMe("G", 3):  # Goomba
                return self.jumpShort()

            # check whether the square in any row and one column in front of mario contains
            # the letter "C" in the array
            # if yes, there is a Coopa in front of mario, therefore the respective function will be called
            if self.inFrontOfMe("C", 3):  # Coopa
                return self.jumpShort()

            return self.right()
        except:
            return self.doNothing()

    ##
    # this function let mario jump but also saves the information on the length of the jump
    # @author
    # @param jumpingStarted bool about mario is jumping or not
    # @param jumpingLong bool if it is a long jump or a short jump
    # @param isLong bool, true for long jump, false for short jump
    #
    # @return ControllerMovement.[].value as an int gets returned.
    ##

    def __jumpInternal(self, isLong):
        self.jumpingStarted = True
        self.jumpingLong = isLong
        return ControllerMovement.rightA.value

    ##
    # function for a long jump
    # @return __jumpInternal
    ##
    def jumpLong(self):
        return self.__jumpInternal(True)
    ##
    # function for a short jump
    # @return __jumpInternal
    ##
    def jumpShort(self):
        return self.__jumpInternal(False)

    ##
    # function for right movement
    # @return ControllerMovement.[].value as an int gets returned.
    ##
    def right(self):
        return ControllerMovement.right.value

    ##
    # function for NOOP movement
    # @return ControllerMovement.[].value as an int gets returned.
    ##
    def doNothing(self):
        return ControllerMovement.NOOP.value

    ##
    # this function checks the a given amount of blocks in front of Mario on the same row for a given sign
    # @param sign, provided sign after which should be searched
    # @param previewLength int, how many blocks in front of mario should be searched
    #
    # @return bool, if sign was found or not
    ##
    def inFrontOfMe(self, sign, previewLengthX):
        for x in range(0, previewLengthX):
            if(self.map.environment[self.positionMarioRow, self.positionMarioCol + x] == sign):
                return True
        return False;

    ##
    # this function checks a given amount of cols in front of Mario for a given sign
    # @param sign, provided sign after which should be searched
    # @param previewLength int, how many cols in front of mario should be searched
    #
    # @return bool, if sign was found or not
    ##
    def inFrontOfMeInFullColumn(self, sign, previewLengthX):
        for x in range(0, previewLengthX):
            if sign in self.map.environment[:, self.positionMarioCol + x]:
                return True
        return False;

    ##
    # this function checks direct under mario for a given sign
    # @param sign, provided sign after which should be searched
    #
    # @return bool, if sign was found or not
    ##
    def underMe(self, sign):
        return self.map.environment[self.positionMarioRow + 1, self.positionMarioCol] == sign

    ##
    # this function checks direct under mario if a given sign is not there
    # @param sign, provided sign after which should be searched
    #
    # @return bool, if sign was found or not
    ##
    def notUnderMe(self, sign):
        return self.map.environment[self.positionMarioRow + 1, self.positionMarioCol] != sign

    ##
    # this function checks the block under mario upcoming for a given sign
    # @param sign, provided sign after which should be searched
    #
    # @return bool, if sign was found or not
    ##
    def underMeUpcoming(self, sign):
        return self.map.environment[self.positionMarioRow + 1, self.positionMarioCol+1] == sign
