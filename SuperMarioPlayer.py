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

sm_movement = SuperMarioMovement.Movement()
sm_images = SuperMarioImages.Images()
sm_env = SuperMarioMap.Mario2DMap()

env = gym_super_mario_bros.make('SuperMarioBros-7-3-v0').env
env = JoypadSpace(env, COMPLEX_MOVEMENT)

done = True
framerate = 5
i = 0
niceConsoleOutput = True

while True:
    if done:
        state = env.reset()
        state, reward, done, info = env.step(0)

        # TODO create a string map based on info like eg:
        #
        ############################################################
        #                                                          # remove points / coin count / world / time
        #                                                          #
        #                                                          #
        #                                                          #
        #                                                          #
        #                                                          #
        #                                                          #
        #                                                          #
        #                  BBB                                     #
        #                                                          #
        #            M                 G                           #
        #                                                          #
        ############################################################

    # print(state.shape)

    # state, reward, done, info = sm_movement.badSearchMovement(state, reward, done, info, env)
    state, reward, done, info = env.step(sm_movement.weightedRandom(sm_movement.basicWeights))
    # state, reward, done, info = sm_movement.bigJump(env, reward, done, info)
    # state, reward, done, info = env.step(random.randint(0,len(COMPLEX_MOVEMENT)-1))
    # state, reward, done, info = env.step(1)
    # state, reward, done, info = env.step(sm_movement.goodMovement(sm_env))

    sm_env.reloadEnvironment()
    sm_env.changeEnvironment(sm_images.detectQuestionBox(state, False), "?")
    sm_env.changeEnvironment(sm_images.detectQuestionBoxlight(state, False), "?")
    sm_env.changeEnvironment(sm_images.detectBlock(state, False), "B")
    sm_env.changeEnvironment(sm_images.detectFloor(state, False), "@")
    sm_env.changeEnvironment(sm_images.detectGoomba(state, False), "G")
    sm_env.changeEnvironment(sm_images.detectMario(state, False), "M")
    sm_env.changeEnvironment(sm_images.detectPipe(state, False), "P")
    sm_env.changeEnvironment(sm_images.detectCooper(state, False), "C")
    sm_env.changeEnvironment(sm_images.detectStairBlock(state, False), "S")

    if i == framerate:
       sm_env.printEnvironment(niceConsoleOutput)
       sys.stdout.flush()
       i = 0

    # print(sm_env.printEnvironment())

    # check mario detection debug
    # if sm_env.marioNotFound > 5:
    #   print("Error: Mario not found")


    #newColor = np.array([255, 255, 0])
    #for i in range(len(state)):
    #    for j in range(len(state[i])):
    #        if np.all(state[i][j] == [228, 92, 16]):
    #            state[i][j] = newColor

    env.render()
    #time.sleep(0.02)
    i = i + 1
env.close()