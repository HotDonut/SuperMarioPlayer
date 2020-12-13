# https://github.com/Kautenja/nes-py
from nes_py.wrappers import JoypadSpace;
# https://github.com/Kautenja/gym-super-mario-bros
import gym_super_mario_bros;

import time
import random
import numpy as np
from os import system


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

def BigJump(env, reward, done, info):
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
    
def WeightedRandom(weightArray):

    my_list = []

    for i,j in enumerate(weightArray):
        my_list += [i]*j

    return random.choice(my_list)

#Needed for better action distribution
basicWeights = [0,0,25,10,65,0,0,0,0,0,0,0,0,0]

#Goomba Array [y,x,Farbe]
goombaArray = np.array([])

#Goomba Augen Array
goombaEyeArray = np.array([[228, 92, 16], [228, 92, 16], [228, 92, 16],  [240, 208, 176], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [240, 208, 176], [228, 92, 16], [228, 92, 16], [228, 92, 16]])

#Goomba Farben
#Goomba, boxes and floor have the same color
goombaColor = np.array([228, 92, 16])
goombaColorBlack = np.array([0, 0, 0])
goombaColorBeige = np.array([240, 208, 176])

#Pits and background Sky
skyColor = np.array([104, 136, 252])

env = gym_super_mario_bros.make('SuperMarioBros-v0').env
env = JoypadSpace(env, COMPLEX_MOVEMENT)

done = True
state, reward, done, info = env.step(0)


while True:
    if done:
        state = env.reset()
        state, reward, done, info = env.step(0)

    
    #print(state.shape)

    #state, reward, done, info = env.step(WeightedRandom(basicWeights))
    #state, reward, done, info = BigJump(env, reward, done, info)
    #state, reward, done, info = env.step(random.randint(0,len(COMPLEX_MOVEMENT)-1))
    #state, reward, done, info = env.step(1)
    
    #for i in range(len(state[0])):
    #    state[192][i] = [0, 0, 0]
    #    state[208][i] = [0, 0, 0]  
    


    env.render()

    maskGoomba = (state[194] == goombaColor).all(axis = 1)
    maskPit = (state[210] == skyColor).all(axis = 1)
    
    if np.any(maskGoomba):
        state, reward, done, info = BigJump(env, reward, done, info)
    else:
        if np.any(maskPit):
            state, reward, done, info = BigJump(env, reward, done, info)
        else:
            state, reward, done, info = env.step(WeightedRandom(basicWeights))


    #newColor = np.array([255, 255, 0])
    #for i in range(len(state)):
    #    for j in range(len(state[i])):
    #        if np.all(state[i][j] == [228, 92, 16]):
    #            state[i][j] = newColor

    env.render()
    time.sleep(0.02)
env.close()
