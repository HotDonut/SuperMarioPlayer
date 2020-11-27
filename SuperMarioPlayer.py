# https://github.com/Kautenja/nes-py
from nes_py.wrappers import JoypadSpace;
# https://github.com/Kautenja/gym-super-mario-bros
import gym_super_mario_bros;

import time
import random
import numpy as np


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


basicWeights = [0,0,25,10,65,0,0,0,0,0,0,0,0,0]

env = gym_super_mario_bros.make('SuperMarioBros-v0').env
env = JoypadSpace(env, COMPLEX_MOVEMENT)

done = True
state, reward, done, info = env.step(0)


while True:
    if done:
        state = env.reset()
        state, reward, done, info = env.step(0)

    state, reward, done, info = env.step(WeightedRandom(basicWeights))
    #state, reward, done, info = BigJump(env, reward, done, info)
    #state, reward, done, info = env.step(random.randint(0,len(COMPLEX_MOVEMENT)-1))
    #state, reward, done, info = env.step(1)
    env.render()
    time.sleep(0.02)
env.close()
