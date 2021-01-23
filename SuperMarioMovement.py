import SuperMarioImages
import SuperMarioMap
import random
import numpy as np

class Movement():

    def __init__(self):

        self.sm_images = SuperMarioImages.Images()

        # Needed for better action distribution
        # jumpright 25
        # runright 10
        # jumprunright 65
        # else 0
        self.basicWeights = [0, 0, 25, 10, 65, 0, 0, 0, 0, 0, 0, 0, 0, 0]

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

    def goodMovement(self, sm_env):
        doMove = 3
        mario = "M"
        positionMario = np.where(sm_env.environment == mario)
        positionMarioRow = positionMario[0]
        positionMarioCole = positionMario[1]

        '''
        if sm_env.environment[positionMarioRow, positionMarioCole+1] == "G":
            return self.movementBygoomba()
        '''
        # if sm_env.environment[positionMarioRow, positionMarioCole + 1] == "P":

        if (sm_env.environment[:, positionMarioCole+1] == "P").any():
            if sm_env.environment[positionMarioRow+1, positionMarioCole] == "@":
                return self.movementByPipe()
            return 0

        if (sm_env.environment[positionMarioRow+1, positionMarioCole] == " ").any:
            return self.movementByPit()

        if (sm_env.environment[:, positionMarioCole+1] == "S").any():
            if sm_env.environment[positionMarioRow+1, positionMarioCole] == "@":
                return self.movementByStairs()
            return 0
        # print(positionMarioRow)
        # print(positionMarioCole)
        # print(sm_env.environment[positionMarioRow, positionMarioCole])
        return doMove

    def movementBygoomba(self):
        return 2

    def movementByPipe(self):
        return 4

    def movementByPit(self):
        return 4

    def movementByStairs(self):
        return 2
