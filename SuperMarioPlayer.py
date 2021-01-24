# https://github.com/Kautenja/nes-py
# https://github.com/Kautenja/gym-super-mario-bros
import gym_super_mario_bros
import sys
import time
from nes_py.wrappers import JoypadSpace
import os
import SuperMarioImages
import SuperMarioMovement
import SuperMarioMap
import SuperMarioDisplay

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

# Instantiating Helper Classes
sm_movement = SuperMarioMovement.Movement()
sm_images = SuperMarioImages.Images()
sm_env = SuperMarioMap.Mario2DMap()

# Instantiating Super Mario Bros. environment
env = gym_super_mario_bros.make('SuperMarioBros-v0').env
env = JoypadSpace(env, COMPLEX_MOVEMENT)

# Specifies the framerate for the console output. Must be a value >= 0. 0 is maximum framerate.
# A framerate of e.g. 20 only shows every 20th frame.
consoleFramerate = 0

# If this flag is set to true console output will be better when using Windows Command Line. Set to False
# if not using Windows or when not using the Windows Command Line to execute the script.
niceConsoleOutput = True

if niceConsoleOutput:
    SuperMarioDisplay.clear_cmd()

done = True
i = 0

while True:
    if done:
        state = env.reset()
        state, reward, done, info = env.step(0)

    # state, reward, done, info = sm_movement.badSearchMovement(state, reward, done, info, env)
    # state, reward, done, info = env.step(sm_movement.weightedRandom(sm_movement.basicWeights))
    # state, reward, done, info = sm_movement.bigJump(env, reward, done, info)
    # state, reward, done, info = env.step(random.randint(0,len(COMPLEX_MOVEMENT)-1))
    # state, reward, done, info = env.step(1)
    state, reward, done, info = env.step(sm_movement.goodMovement(sm_env))

    sm_env.reloadEnvironment()
    # Detecting for all relevant kind of obstacles
    sm_env.changeEnvironment(sm_images.detectQuestionBox(state, False), "?")
    sm_env.changeEnvironment(sm_images.detectQuestionBoxlight(state, False), "?")
    sm_env.changeEnvironment(sm_images.detectBlock(state, False), "B")
    sm_env.changeEnvironment(sm_images.detectFloor(state, False), "@")
    sm_env.changeEnvironment(sm_images.detectGoomba(state, False), "G")
    sm_env.changeEnvironment(sm_images.detectMario(state, False), "M")
    sm_env.changeEnvironment(sm_images.detectPipe(state, False), "P")
    sm_env.changeEnvironment(sm_images.detectCooper(state, False), "C")
    sm_env.changeEnvironment(sm_images.detectStairBlock(state, False), "S")

    if i == consoleFramerate:
        sm_env.printEnvironment(niceConsoleOutput)
        i = 0

    env.render()
    # time.sleep(0.02)
    if consoleFramerate > 0:
        i = i + 1
env.close()
