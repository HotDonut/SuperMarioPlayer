import gym_super_mario_bros
import os
from nes_py.wrappers import JoypadSpace
import time


import datetime
import src.SuperMarioImages as SuperMarioImages
import src.SuperMarioMovement as SuperMarioMovement
import src.SuperMarioMarkov as SuperMarioMarkov
import src.SuperMarioMap as SuperMarioMap
import src.SuperMarioReinforcedLearning as SuperMarioReinforcedLearning
import src.SuperMarioConsoleDebugWindow as SuperMarioConsoleDebugWindow
from src.SuperMarioConfig import SuperMarioConfig as SuperMarioConfig
from src.SuperMarioPlot import SuperMarioPlot


class SuperMarioEnvironment:

    def startPlayer(self):

        # SuperMarioConfig needs a concrete object to use json encoding/decoding
        config = SuperMarioConfig("SuperMarioConfig.json")

        # map = SuperMarioMap.Mario2DMap()
        movement = SuperMarioMovement.Movement(map)
        # images = SuperMarioImages.Images(config.imageDetectionConfiguration, config.imageAssetsDirectory, config.debugAll)
        # debugWindow = SuperMarioConsoleDebugWindow.SuperMarioConsoleDebugWindow(config.WindowsConsoleOutput)
        # markovMovement = SuperMarioMarkov.SuperMarioMarkov(map, config.markovStatesPath, config.markovStateDimensions)
        reinforcedLearningMovement = SuperMarioReinforcedLearning.SuperMarioReinforcedLearning()

        # images.loadAllAssets()

        # Instantiating Super Mario Bros. environment
        env = JoypadSpace(gym_super_mario_bros.make('SuperMarioBros-v0').env, movement.COMPLEX_MOVEMENT)
        # debugWindow.clear()

        consoleFrameCount = 0
        renderFrameCount = 0
        standingFrameCount = 0 #counts how long mario is stuck
        done = True
        reward = 0
        calculatedAction = 0
        learningCycle = 0
        max_x_pos_whole_training = 100
        max_x_pos_run = 0
        watch_replay = False
        replay_path = os.path.join("best_runs", "12032021-013205_replay.txt")
        replay = []
        now = datetime.datetime.now()
        runTime = now.strftime("%m%d%Y-%H%M%S")
        newBest = False
        old_x_pos = 0
        deathCount = 0
        best_X_per_episode = 0


        if watch_replay:
            with open(replay_path, "r") as file:
                for line in file:
                    calculatedAction = int(line.strip())
                    env.step(calculatedAction)
                    env.render()

            env.reset()
            return


        #reinforcedLearningMovement.loadNeuralNetwork() # <- takes last save
        # reinforcedLearningMovement.loadNeuralNetwork(modelpath="saved_model1.h5", statspath="saved_model_stats1.txt") # <- if you want to load specific save

        # if you want to start a new network
        reinforcedLearningMovement.initNeuralNetwork()
        reinforcedLearningMovement.saveNeuralNetwork()

        state, reward, done, info = env.step(0)

        superMarioPlotDeath = SuperMarioPlot()
        superMarioPlotBestX = SuperMarioPlot()
        oldMacroIterations = reinforcedLearningMovement.macro_iterations
        old_episode = reinforcedLearningMovement.train_iterations
        while True:

            # if info["x_pos"] > 200:
                # print("ABC")

            # Identify current theme
            # currentTheme = config.themeIdentifier[str(info["world"])][str(info["stage"])]
            # print(currentTheme)

            # Detecting for all relevant kind of obstacles
            # images.processImage(state)
            # map.resetMap(False)

            # detectedAssetsAndCorrespondingSymbol = images.detectOnlyThemeSpecificAssets(currentTheme)
            # map.changeMapAll(detectedAssetsAndCorrespondingSymbol)

            # visualization
            if consoleFrameCount >= config.ConsoleFramerate:
                # debugWindow.debugPrint(map.toString())
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
            if reward == 0:
                reward = -1

            calculatedAction = reinforcedLearningMovement.nextStep(reward, calculatedAction, state)
            #calculatedAction = movement.move()
            # debugWindow.debugPrint(map.toString() + "\n" + "Calculated Action: " + str(calculatedAction))
            # debugWindow.debugPrint("Hello World")
            # print(reward)
            state, reward, done, info = env.step(calculatedAction)
            replay.append(calculatedAction)

            if info["x_pos"] > max_x_pos_whole_training:
                max_x_pos_whole_training = info["x_pos"]
                newBest = True

            if info["x_pos"] > max_x_pos_run:
                max_x_pos_run = info["x_pos"]
                standingFrameCount = 0
            else:
                standingFrameCount = standingFrameCount + 1


            if standingFrameCount >= 200:
                reward = -15
                done = True
                # print("He dead")

            if reward == -15:
                deathCount += 1
                max_x_pos_run = 0
                standingFrameCount = 0

            if info["x_pos"] > best_X_per_episode:
                best_X_per_episode = info["x_pos"]

            if oldMacroIterations != reinforcedLearningMovement.macro_iterations:
                superMarioPlotDeath.deathCountPlot(oldMacroIterations, deathCount)
                oldMacroIterations = reinforcedLearningMovement.macro_iterations
                deathCount = 0

            if old_episode != reinforcedLearningMovement.train_iterations:
                superMarioPlotBestX.bestXPlot(old_episode, best_X_per_episode)
                old_episode = reinforcedLearningMovement.train_iterations
                best_X_per_episode = 0

            if done:
                if newBest:
                    newBest = False
                    with open(os.path.join("best_runs", runTime + "_replay.txt"), "w+") as file:
                        for action in replay:
                            file.write(str(action) + "\n")
                    replay.clear()
                    os.replace("saved_model.h5", os.path.join("best_runs",runTime + "_best.h5"))
                    os.replace("saved_model_stats.txt", os.path.join("best_runs", runTime + "_best.txt"))
                reinforcedLearningMovement.train()
                reinforcedLearningMovement.saveNeuralNetwork()
                env.reset()

            # print("------------------------")
            # print("Count: " + str(standingFrameCount))
            # print("Old x pos: " + str(old_x_pos))
            # print("X Pos: " + str(info["x_pos"]))
            # print("------------------------")

        env.close()
