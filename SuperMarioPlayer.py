# https://github.com/Kautenja/nes-py
from nes_py.wrappers import JoypadSpace;
# https://github.com/Kautenja/gym-super-mario-bros
import gym_super_mario_bros;

import time
import random
import numpy as np

class Images():

    def __init__(self):
        #Goomba, boxes and floor have the same color
        #cannot be used for value at goombas
        self.goombaColor = np.array([228, 92, 16])

        #Pits and background Sky
        self.skyColor = np.array([104, 136, 252])

        #Goomba Eye array
        self.goombaEyeArray = np.array([[228, 92, 16], [228, 92, 16], [228, 92, 16],  [240, 208, 176], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [240, 208, 176], [228, 92, 16], [228, 92, 16], [228, 92, 16]])

        #Pipe array
        self.pipeArray = np.array([[0,0,0],[184,248,24],[184,248,24],[184,248,24],[0,168,0],[0,168,0],[184,248,24],[184,248,24],[184,248,24],[184,248,24],[184,248,24],[0,168,0],[184,248,24],[184,248,24]])

        #Koopa array
        self.koopaShellArray = np.array([[252, 252, 252], [0, 168, 0], [0, 168, 0], [0, 168, 0], [0, 168, 0], [252, 168, 68], [0, 168, 0], [252, 252, 252], [252, 252, 252], [252, 168, 68]])

class Movement():
    
    def __init__(self):

        self.sm_images = Images()

        #Needed for better action distribution
        #jumpright 25
        #runright 10
        #jumprunright 65
        #else 0
        self.basicWeights = [0,0,25,10,65,0,0,0,0,0,0,0,0,0]

    def BigJump(self, env, reward, done, info):
        height = 0

        #print("Prepare!\n")
        state, reward, done, info = env.step(3)
        env.render()

        while height <= info['y_pos']:

            if done:
                state = env.reset()

            height = info['y_pos']
            state, reward, done, info = env.step(4)
        
            env.render()
            #print("Jump!\n")

        while height != info['y_pos']:

            if done:
                state = env.reset()

            height = info['y_pos']
            state, reward, done, info = env.step(3)
            env.render()
            #print("Wait!\n")
        return state, reward, done, info

    def WeightedRandom(self, weightArray):

        listOfValidActionsWithCountOfItemsInferedByWeights = []

        for idx,weight in enumerate(weightArray): 
            listOfValidActionsWithCountOfItemsInferedByWeights += [idx]*weight # inserts "weight"-times an action (= index of operation; see: COMPLEX_MOVEMENT)

        return random.choice(listOfValidActionsWithCountOfItemsInferedByWeights)

    def BadSearchMovement(self, state, reward, done, info, env):
        maskGoomba = (state[194] == self.sm_images.goombaColor).all(axis = 1)
        maskPit = (state[210] == self.sm_images.skyColor).all(axis = 1)

        if np.any(maskGoomba):
            return sm_movement.BigJump(env, reward, done, info)
        else:
            if np.any(maskPit):
                return sm_movement.BigJump(env, reward, done, info)
            else:
                return env.step(sm_movement.WeightedRandom(sm_movement.basicWeights))

class Mario2DMap():
    def __init__(self):
        self.environment = np.array([[" "]*16]*16)

    def PrintEnvironment(self):
        erg = "#"*18
        erg += "\n"
        for x in self.environment:
            erg += "#"
            for y in x:
                erg += y
            erg += "#\n"
        erg += "#"*18
        erg += "\n"
        return(erg)

    def ChangeEnvironment(self, x, y, symbol):
        self.environment[y][x] = symbol

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

sm_movement = Movement()
sm_images = Images()
sm_env = Mario2DMap()

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
    
    #print(state.shape)

    #state, reward, done, info = sm_movement.BadSearchMovement(state, reward, done, info, env)
    #state, reward, done, info = env.step(sm_movement.WeightedRandom(sm_movement.basicWeights))
    #state, reward, done, info = sm_movement.BigJump(env, reward, done, info)
    #state, reward, done, info = env.step(random.randint(0,len(COMPLEX_MOVEMENT)-1))
    state, reward, done, info = env.step(1)
    
    #for i in range(len(state[0])):
    #    state[192][i] = [0, 0, 0]
    #    state[208][i] = [0, 0, 0]  
    
    #newColor = np.array([255, 255, 0])
    #for i in range(len(state)):
    #    for j in range(len(state[i])):
    #        if np.all(state[i][j] == goombaColor):
    #            state[i][j] = newColor
    
    
    #Area of importance
    #Height: 36-Border
    #Width: 126-Border

    
    #mask = np.zeros(slicedState.shape)
    #state[35:, 130:] = mask

    #Ideales Raster
    #16x16
    #Creating 16x16 fields that need to be tracked
    color = [0,0,0]
    for z in range(int(state.shape[0]/16)):
        state[16*z, :] = color
        for y in range(int(state.shape[1]/16)):
            state[:, 16*y] = color

    env.render()
    time.sleep(0.02)
    sm_env.ChangeEnvironment(3,10,'A')
    print(sm_env.PrintEnvironment())
env.close()