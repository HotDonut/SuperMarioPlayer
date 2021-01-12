# https://github.com/Kautenja/nes-py
from nes_py.wrappers import JoypadSpace
# https://github.com/Kautenja/gym-super-mario-bros
import gym_super_mario_bros

import time


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

env = gym_super_mario_bros.make('SuperMarioBros-v0')
env = JoypadSpace(env, COMPLEX_MOVEMENT)

done = True

while True:
    if done:
        state = env.reset()

    state, reward, done, info = env.step(4)
    env.render()
    time.sleep(0.01)

    #print("Reward: %d" )
env.close()
