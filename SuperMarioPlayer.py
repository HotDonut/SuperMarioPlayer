# https://github.com/Kautenja/nes-py
# https://github.com/Kautenja/gym-super-mario-bros
import gym_super_mario_bros
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

env = gym_super_mario_bros.make('SuperMarioBros-v0').env
env = JoypadSpace(env, COMPLEX_MOVEMENT)

done = True

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

    sm_env.reloadEnvironment()
    sm_env.changeEnvironment(sm_images.detectQuestionBox(state, False), "?")
    sm_env.changeEnvironment(sm_images.detectQuestionBoxlight(state, False), "?")
    sm_env.changeEnvironment(sm_images.detectBlock(state, False), "B")
    sm_env.changeEnvironment(sm_images.detectFloor(state, False), "@")
    sm_env.changeEnvironment(sm_images.detectGoomba(state, True), "G")
    sm_env.changeEnvironment(sm_images.detectMario(state, True), "M")
    sm_env.changeEnvironment(sm_images.detectPipe(state, False), "P")

    print(sm_env.printEnvironment())

    env.render()
    #time.sleep(0.02)
env.close()