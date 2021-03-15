import random
import numpy as np
from enum import Enum

import src.SuperMarioImages as SuperMarioImages
from src.SuperMarioConfig import SuperMarioConfig as SuperMarioConfig

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
        
        self.jumpingStarted = False
        self.jumpingLong = False
        self.leftTheFloorOnce = False

    ##
    # Based on the position of Mario, this method looks around him and tries too find other objects
    # @author Florian Weiskirchner
    #
    # @param oldYPositionMario is the Y Position from Mario in the last Move
    # @param doMove Which move should be used from the COMPLEX_MOVEMENT array
    # @param charForMario Which Char Mario has in the array
    # @param isFalling is a bool which is true when Mario is falling and false when he is jumping or running
    # @return doMove gets returned.
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

            if self.inFrontOfMe("G", 3):  # Goomba
                return self.jumpShort()

            if self.inFrontOfMe("C", 3):  # Coopa
                return self.jumpShort()

            return self.right()
        except:
            return self.doNothing()


    def __jumpInternal(self, isLong):
        self.jumpingStarted = True
        self.jumpingLong = isLong
        return ControllerMovement.rightA.value


    def jumpLong(self):
        return self.__jumpInternal(True)

    def jumpShort(self):
        return self.__jumpInternal(False)

    def right(self):
        return ControllerMovement.right.value

    def doNothing(self):
        return ControllerMovement.NOOP.value

    def inFrontOfMe(self, sign, previewLengthX):
        for x in range(0, previewLengthX):
            if(self.map.environment[self.positionMarioRow, self.positionMarioCol + x] == sign):
                return True
        return False;

    def inFrontOfMeInFullColumn(self, sign, previewLengthX):
        for x in range(0, previewLengthX):
            if sign in self.map.environment[:, self.positionMarioCol + x]:
                return True
        return False;

    def underMe(self, sign):
        return self.map.environment[self.positionMarioRow + 1, self.positionMarioCol] == sign

    def notUnderMe(self, sign):
        return self.map.environment[self.positionMarioRow + 1, self.positionMarioCol] != sign

    def underMeUpcoming(self, sign):
        return self.map.environment[self.positionMarioRow + 1, self.positionMarioCol+1] == sign
