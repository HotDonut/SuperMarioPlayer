import gym_super_mario_bros
from nes_py.wrappers import JoypadSpace

import src.SuperMarioImages as SuperMarioImages
import src.SuperMarioMovement as SuperMarioMovement
import src.SuperMarioMarkov as SuperMarioMarkov
import src.SuperMarioMap as SuperMarioMap
import src.SuperMarioConsoleDebugWindow as SuperMarioConsoleDebugWindow
from src.SuperMarioConfig import SuperMarioConfig as SuperMarioConfig


class SuperMarioEnvironment:

    def startPlayer(self):

        # SuperMarioConfig needs a concrete object to use json encoding/decoding
        config = SuperMarioConfig()
        # load config into SuperMarioConfig class variables
        config.load_config("SuperMarioConfig.json")
        # create debug config json file (current config)
        # config.write_json_file()

        map = SuperMarioMap.Mario2DMap()
        movement = SuperMarioMovement.Movement(map)
        images = SuperMarioImages.Images(config.imageDetectionConfiguration, config.imageAssetsDirectory)
        debugWindow = SuperMarioConsoleDebugWindow.SuperMarioConsoleDebugWindow()
        markovMovement = SuperMarioMarkov.SuperMarioMarkov(map, config.markovStatesPath, config.markovStateDimensions)

        images.loadAllAssets()

        # Instantiating Super Mario Bros. environment
        env = JoypadSpace(gym_super_mario_bros.make('SuperMarioBros-1-2-v0').env, movement.COMPLEX_MOVEMENT)
        debugWindow.clear()

        consoleFrameCount = 0
        renderFrameCount = 0
        frameCount = 0
        done = True

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

            # map.changeMap(images.detectQuestionBox(), "?")
            # map.changeMap(images.detectQuestionBoxlight(), "?")
            # map.changeMap(images.detectBlock(), "B")
            # map.changeMap(images.detectFloor(), "@")
            # map.changeMap(images.detectGoomba(), "G")
            # map.changeMap(images.detectPipe(), "P")
            # map.changeMap(images.detectCooper(), "C")
            # map.changeMap(images.detectStairBlock(), "S")
            # map.changeMap(images.detectMario(), "M")

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
            calculatedAction = markovMovement.nextStep(info["y_pos"])
            #calculatedAction = movement.move()
            debugWindow.debugPrint(map.toString() + "\n" + "\n" + str(calculatedAction))
            state, reward, done, info = env.step(calculatedAction)

            # debug

            # Mario Clips in to the Stairs (debug)
            # if frameCount == 1368:
            #     print("")

            # print(frameCount)
            # f = open("MapsNew.txt", "a")
            # String = "Map at Frame " + str(frameCount) + ":\n\n" + map.toString()
            # f.write(String)
            # f.close()
            # frameCount = frameCount + 1

        env.close()
