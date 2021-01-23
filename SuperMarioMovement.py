import SuperMarioImages
import SuperMarioMap
import random
import numpy as np
import EnumMovement

class Movement():

    positionMarioRow = 0
    positionMarioCole = 0
    oldYPositionMario = 16
    isFalling = False

    def __init__(self):

        self.sm_images = SuperMarioImages.Images()

        # Needed for better action distribution
        # jumpright 25
        # runright 10
        # jumprunright 65
        # else 0
        self.basicWeights = [0, 0, 25, 10, 65, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.movement = EnumMovement.Movement

    def bigJump(self, env, reward, done, info):
        height = 0

        # print("Prepare!\n")
        state, reward, done, info = env.step(3)
        env.render()

        while height <= info['y_pos']:

            if done:
                state = env.reset()

            height = info['y_pos']
            state, reward, done, info = env.step(4)

            env.render()
            # print("Jump!\n")

        while height != info['y_pos']:

            if done:
                state = env.reset()

            height = info['y_pos']
            state, reward, done, info = env.step(3)
            env.render()
            # print("Wait!\n")
        return state, reward, done, info

    def weightedRandom(self, weightArray):

        listOfValidActionsWithCountOfItemsInferedByWeights = []

        for idx, weight in enumerate(weightArray):
            listOfValidActionsWithCountOfItemsInferedByWeights += [
                                                                      idx] * weight  # inserts "weight"-times an action (= index of operation; see: COMPLEX_MOVEMENT)

        return random.choice(listOfValidActionsWithCountOfItemsInferedByWeights)

    def badSearchMovement(self, state, reward, done, info, env):
        maskGoomba = (state[194] == self.sm_images.goombaColor).all(axis=1)
        maskPit = (state[210] == self.sm_images.skyColor).all(axis=1)

        if np.any(maskGoomba):
            return self.bigJump(env, reward, done, info)
        else:
            if np.any(maskPit):
                return self.bigJump(env, reward, done, info)
            else:
                return env.step(self.weightedRandom(self.basicWeights))

    ##
    # This function search Mario (M) in the Array and saves his position.
    # Based on the position of Mario, it looks around him and tries too find other objects
    # @author Florian Weiskirchner
    #
    # @param doMove Which move should be used from the COMPLEX_MOVEMENT array
    # @param charForMario Which Char Mario has in the array
    # @return doMove gets returned.
    ##
    def goodMovement(self, sm_env):
        self.oldYPositionMario = self.positionMarioRow
        doMove = self.movement.right.value
        self.marioSearch(sm_env)
        self.isFalling = self.checkIfFalling()

        if sm_env.environment[self.positionMarioRow, self.positionMarioCole+2] == "G":                # eventuell if als Funktion machen
            return self.movementBygoomba()

        # if sm_env.environment[self.positionMarioRow + 1, self.positionMarioCole + 1] == "G":
            # return self.avoidGoomba()

        # if sm_env.environment[self.positionMarioRow, self.positionMarioCole + 1] == "P":
            # return self.movementByPipe()

        if sm_env.environment[self.positionMarioRow + 1, self.positionMarioCole] == "P":
            return self.movementOntopOfPipe()

        if (sm_env.environment[:, self.positionMarioCole+1] == "P").any():
            return self.movementByPipe()

        if sm_env.environment[self.positionMarioRow, self.positionMarioCole + 1] == "C":
            return self.movementByCooper()

        if self.isFalling:
            doMove = self.movement.left.value
        # print(positionMarioRow)
        # print(positionMarioCole)
        # print(sm_env.environment[positionMarioRow, positionMarioCole])
        # self.oldYPositionMario = self.positionMarioRow
        return doMove

    def marioSearch(self, sm_env):
        charForMario = "M"
        positionMario = np.where(sm_env.environment == charForMario)
        self.positionMarioRow = positionMario[0]
        self.positionMarioCole = positionMario[1]
        return

    def checkIfFalling(self):
        if self.positionMarioRow > self.oldYPositionMario:
            print("Mario is Falling")
            return True
        return False

    def movementBygoomba(self):
        if self.isFalling:
            return self.movement.NOOP.value
        return self.movement.rightA.value

    def avoidGoomba(self):
        return self.movement.left.value

    def movementByPipe(self):
        if self.isFalling:
            return self.movement.NOOP.value
        return self.movement.rightAB.value

    def movementOntopOfPipe(self):
        if self.isFalling:
            return self.movement.NOOP.value
        return self.movement.right.value

    def movementByCooper(self):
        if self.isFalling:
            return self.movement.NOOP.value
        return self.movement.rightA.value
