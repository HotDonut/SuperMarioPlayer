import gym_super_mario_bros
from nes_py.wrappers import JoypadSpace

import src.SuperMarioImages as SuperMarioImages
import src.SuperMarioMovement as SuperMarioMovement
import src.SuperMarioMarkov as SuperMarioMarkov
import src.SuperMarioMap as SuperMarioMap
import src.SuperMarioReinforcedLearning as SuperMarioReinforcedLearning
import src.SuperMarioConsoleDebugWindow as SuperMarioConsoleDebugWindow
from src.SuperMarioConfig import SuperMarioConfig as SuperMarioConfig


class SuperMarioEnvironment:

    def startPlayer(self):

        # SuperMarioConfig needs a concrete object to use json encoding/decoding
        config = SuperMarioConfig("SuperMarioConfig.json")

        map = SuperMarioMap.Mario2DMap()
        movement = SuperMarioMovement.Movement(map)
        images = SuperMarioImages.Images(config.imageDetectionConfiguration, config.imageAssetsDirectory, config.debugAll)
        debugWindow = SuperMarioConsoleDebugWindow.SuperMarioConsoleDebugWindow(config.WindowsConsoleOutput)
        markovMovement = SuperMarioMarkov.SuperMarioMarkov(map, config.markovStatesPath, config.markovStateDimensions)
        reinforcedLearningMovement = SuperMarioReinforcedLearning.SuperMarioReinforcedLearning(map)

        images.loadAllAssets()

        # Instantiating Super Mario Bros. environment
        env = JoypadSpace(gym_super_mario_bros.make('SuperMarioBros-v0').env, movement.COMPLEX_MOVEMENT)
        debugWindow.clear()

        consoleFrameCount = 0
        renderFrameCount = 0
        done = True
        reward = 0
        calculatedAction = 0
        learningCycle = 0

        while True:
            if done:
                state = env.reset()
                state, reward, done, info = env.step(0)
                env.render()
                movement.reset()

            # Identify current theme
            currentTheme = config.themeIdentifier[str(info["world"])][str(info["stage"])]
            # print(currentTheme)

            # Detecting for all relevant kind of obstacles
            images.processImage(state)
            map.resetMap(False)

            detectedAssetsAndCorrespondingSymbol = images.detectOnlyThemeSpecificAssets(currentTheme)
            map.changeMapAll(detectedAssetsAndCorrespondingSymbol)

            # visualization
            if consoleFrameCount >= config.ConsoleFramerate:
                debugWindow.debugPrint(map.toString())
                consoleFrameCount = 0
            else:
                consoleFrameCount = consoleFrameCount + 1

            if renderFrameCount >= config.RenderFramerate:
                env.render()
                renderFrameCount = 0
            else:
                renderFrameCount = renderFrameCount + 1

            # execute action
            # calculatedAction = markovMovement.nextStep(info["y_pos"])
            calculatedAction = reinforcedLearningMovement.nextStep(reward, calculatedAction)
            #calculatedAction = movement.move()
            debugWindow.debugPrint(map.toString() + "\n" + "Calculated Action: " + str(calculatedAction))
            debugWindow.debugPrint("Hello World")
            state, reward, done, info = env.step(calculatedAction)
            # print(reward)


        env.close()
