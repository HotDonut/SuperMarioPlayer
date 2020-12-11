# https://github.com/Kautenja/nes-py
from nes_py.wrappers import JoypadSpace
# https://github.com/Kautenja/gym-super-mario-bros
import gym_super_mario_bros

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


def jumpUpSuperHigh(highUpInTheSky):
    i = 0
    while i < highUpInTheSky:
        state, reward, done, info = env.step(4)
        env.render()
        i += 1
    state, reward, done, info = env.step(3)
    env.render()
    return state, reward, done, info


done = True

while True:
    if done:
        state = env.reset()
        print(env.observation_space)
    state, reward, done, info = env.step(4)
    env.render()
    if info['life'] > 0:
        state, reward, done, info = jumpUpSuperHigh(16)
    else:
        print("Paradigm Shift")
        state, reward, done, info = jumpUpSuperHigh(13)
env.close()
