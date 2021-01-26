import sys
import time
import os

import gym_super_mario_bros
from nes_py.wrappers import JoypadSpace

import src.SuperMarioImages as SuperMarioImages
import src.SuperMarioMovement as SuperMarioMovement
import src.SuperMarioMap as SuperMarioMap
import src.SuperMarioConsoleDebugWindow as SuperMarioConsoleDebugWindow

class SuperMarioEnvironment:
    
    # Instantiating Helper Classes
    __sm_movement = SuperMarioMovement.Movement()
    __sm_images = SuperMarioImages.Images()
    __sm_env = SuperMarioMap.Mario2DMap()

    # Specifies the frame rate for the console output. Must be a value >= 0. 
    # 0 is maximum framerate. A framerate of e.g. 20 only shows every 20th frame.
    consoleFramerate = 0
    renderFramerate = 0


    def startPlayer(self):
        # Instantiating Super Mario Bros. environment
        self.env = JoypadSpace(gym_super_mario_bros.make('SuperMarioBros-v0').env, self.__sm_movement.COMPLEX_MOVEMENT)

        SuperMarioConsoleDebugWindow.clear()

        consoleFrameCount = 0
        renderFrameCount = 0
        done = True

        while True:
            if done:
                state = self.env.reset()
                state, reward, done, info = self.env.step(0)

            state, reward, done, info = self.env.step(self.__sm_movement.goodMovement(self.__sm_env))
            # state, reward, done, info = __sm_movement.badSearchMovement(state, reward, done, info, self.env)
            # state, reward, done, info = env.step(__sm_movement.weightedRandom(self.__sm_movement.basicWeights))
            # state, reward, done, info = __sm_movement.bigJump(self.env, reward, done, info)
            # state, reward, done, info = env.step(random.randint(0,len(self.__sm_movement.COMPLEX_MOVEMENT)-1))
            # state, reward, done, info = env.step(1)


            self.__sm_env.reloadEnvironment()

            # Detecting for all relevant kind of obstacles
            self.__sm_images.processImage(state)
            self.__sm_env.changeEnvironment(self.__sm_images.detectQuestionBox(False), "?")
            self.__sm_env.changeEnvironment(self.__sm_images.detectQuestionBoxlight(False), "?")
            self.__sm_env.changeEnvironment(self.__sm_images.detectBlock(False), "B")
            self.__sm_env.changeEnvironment(self.__sm_images.detectFloor(False), "@")
            self.__sm_env.changeEnvironment(self.__sm_images.detectGoomba(False), "G")
            self.__sm_env.changeEnvironment(self.__sm_images.detectMario(False), "M")
            self.__sm_env.changeEnvironment(self.__sm_images.detectPipe(False), "P")
            self.__sm_env.changeEnvironment(self.__sm_images.detectCooper(False), "C")
            self.__sm_env.changeEnvironment(self.__sm_images.detectStairBlock(False), "S")

            if consoleFrameCount == self.consoleFramerate:
                self.__sm_env.printEnvironment()
                consoleFrameCount = 0
            else:
                consoleFrameCount = consoleFrameCount + 1

            if renderFrameCount == self.renderFramerate:
                self.env.render()
                renderFrameCount = 0
            else:
                renderFrameCount = renderFrameCount + 1


        self.env.close()