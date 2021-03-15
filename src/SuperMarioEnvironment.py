import sys
import time
import os

import gym_super_mario_bros
from nes_py.wrappers import JoypadSpace

import src.SuperMarioImages as SuperMarioImages
import src.SuperMarioMovement as SuperMarioMovement
import src.SuperMarioMap as SuperMarioMap
import src.SuperMarioConsoleDebugWindow as SuperMarioConsoleDebugWindow
from src.SuperMarioConfig import SuperMarioConfig as SuperMarioConfig

class SuperMarioEnvironment:
    
    def startPlayer(self):

        map = SuperMarioMap.Mario2DMap()
        movement = SuperMarioMovement.Movement(map)
        images = SuperMarioImages.Images()
        debugWindow = SuperMarioConsoleDebugWindow.SuperMarioConsoleDebugWindow();

        # Instantiating Super Mario Bros. environment
        env = JoypadSpace(gym_super_mario_bros.make('SuperMarioBros-v0').env, movement.COMPLEX_MOVEMENT)
        debugWindow.clear()

        consoleFrameCount = 0
        renderFrameCount = 0
        done = True

        while True:
            if done:
                state = env.reset()
                state, reward, done, info = env.step(0)
                env.render()
                movement.reset()

            # Detecting for all relevant kind of obstacles
            images.processImage(state)
            map.resetMap(False)
            map.changeMap(images.detectQuestionBox(), "?")
            map.changeMap(images.detectQuestionBoxlight(), "?")
            map.changeMap(images.detectBlock(), "B")
            map.changeMap(images.detectFloor(), "@")
            map.changeMap(images.detectGoomba(), "G")
            map.changeMap(images.detectPipe(), "P")
            map.changeMap(images.detectCooper(), "C")
            map.changeMap(images.detectStairBlock(), "S")
            map.changeMap(images.detectMario(), "M")

            # visualization
            if consoleFrameCount >= SuperMarioConfig.ConsoleFramerate:
                debugWindow.debugPrint(map.toString())
                consoleFrameCount = 0
            else:
                consoleFrameCount = consoleFrameCount + 1

            if renderFrameCount >= SuperMarioConfig.RenderFramerate:
                env.render()
                renderFrameCount = 0
            else:
                renderFrameCount = renderFrameCount + 1

            # execute action
            calculatedAction = movement.move()
            debugWindow.debugPrint(map.toString()+"\n"+"\n"+str(calculatedAction))
            state, reward, done, info = env.step(calculatedAction)
            
        env.close()