# https://github.com/Kautenja/nes-py
from nes_py.wrappers import JoypadSpace;
# https://github.com/Kautenja/gym-super-mario-bros
import gym_super_mario_bros;

import time
import random


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

def BigJump(env, done, info):
    height = 0
    while True:
        if height > info['y_pos']:
            break;
        if done:
            state = env.reset()

        height = info['y_pos']
        state, reward, done, info = env.step(4)
        env.render()
        print("Jump!\n")

    while True:
        if height == info['y_pos']:
            break;
        if done:
            state = env.reset()

        height = info['y_pos']
        state, reward, done, info = env.step(3)
        env.render()
        print("Wait!\n")
    return state, reward, done, info

env = gym_super_mario_bros.make('SuperMarioBros-v0').env
env = JoypadSpace(env, COMPLEX_MOVEMENT)

done = True

state, reward, done, info = env.step(0)
temp = state

while True:
    if done:
        state = env.reset()
        state, reward, done, info = env.step(0)

    state, reward, done, info = BigJump(env, done, info)
    env.render()
    print(env.observation_space.high)
    time.sleep(2)
env.close()