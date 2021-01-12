# https://github.com/Kautenja/nes-py
import random
import time
from PIL import Image
# https://github.com/Kautenja/gym-super-mario-bros
import gym_super_mario_bros
import time
import random
import numpy as np
import cv2
from nes_py.wrappers import JoypadSpace

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

        # Koopa array
        self.koopaShellArray = np.array(
            [[252, 252, 252], [0, 168, 0], [0, 168, 0], [0, 168, 0], [0, 168, 0], [252, 168, 68], [0, 168, 0],
             [252, 252, 252], [252, 252, 252], [252, 168, 68]])

    @staticmethod
    def processImage():
        # converts state (pixel array) to image
        img = Image.fromarray(state, 'RGB')
        img_rgb = np.array(img)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        return img_gray, img_rgb

    def detectGoomba(self, debug):
        img_gray, img_rgb = Images.processImage()
        template = cv2.imread('goomba.png', 0)
        w, h = template.shape[::-1]
        color = [0, 0, 0]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.5
        loc = np.where(res >= threshold)
        #  print(loc)
        if debug:
            for pt in zip(*loc[::-1]):
                # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                # print(pt[0], pt[1])
                state[:, pt[0]] = color
                state[pt[1], :] = color
                print(pt[0] / 16, pt[1] / 16)
        return loc
        # cv2.imwrite('res.png', img_rgb)
        # img.show()

    def detectMario(self, debug):
        img_gray, img_rgb = Images.processImage()
        template = cv2.imread('mario.png', 0)
        w, h = template.shape[::-1]
        color = [255, 0, 0]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        #  print(loc)
        if debug:
            for pt in zip(*loc[::-1]):
                # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                # print(pt[0], pt[1])
                state[:, pt[0]] = color
                state[pt[1], :] = color
                print(pt[0] / 16, pt[1] / 16)
        return loc
        # cv2.imwrite('res.png', img_rgb)
        # img.show()

    def detectQuestionBox(self, debug):
        img_gray, img_rgb = Images.processImage()
        template = cv2.imread('questionbox.png', 0)
        w, h = template.shape[::-1]
        color = [0, 255, 0]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.6
        loc = np.where(res >= threshold)
        #  print(loc)
        if debug:
            for pt in zip(*loc[::-1]):
                # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 1)
                # print(pt[0], pt[1])
                state[:, pt[0]] = color
                state[pt[1], :] = color
        return loc
        # cv2.imwrite('res.png', img_rgb)
        # img.show()

    def detectBlock(self, debug):
        img_gray, img_rgb = Images.processImage()
        template = cv2.imread('block.png', 0)
        w, h = template.shape[::-1]
        color = [0, 255, 0]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.9
        loc = np.where(res >= threshold)
        #  print(loc)
        if debug:
            for pt in zip(*loc[::-1]):
                # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 1)
                # print(pt[0], pt[1])
                state[:, pt[0]] = color
                state[pt[1], :] = color
        return loc
        # cv2.imwrite('res.png', img_rgb)
        # img.show()

    def detectFloor(self, debug):
        img_gray, img_rgb = Images.processImage()
        template = cv2.imread('floor.png', 0)
        w, h = template.shape[::-1]
        color = [0, 255, 255]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.80
        loc = np.where(res >= threshold)
        #  print(loc)
        if debug:
            for pt in zip(*loc[::-1]):
                # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 1)
                # print(pt[0], pt[1])
                state[:, pt[0]] = color
                state[pt[1], :] = color
        return loc
        # cv2.imwrite('res.png', img_rgb)
        # img.show()

class Movement():
    
    def __init__(self):

        self.sm_images = Images()

        #Needed for better action distribution
        #jumpright 25
        #runright 10
        #jumprunright 65
        #else 0
        self.basicWeights = [0,0,25,10,65,0,0,0,0,0,0,0,0,0]

    def bigJump(self, env, reward, done, info):
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

    def weightedRandom(self, weightArray):

        listOfValidActionsWithCountOfItemsInferedByWeights = []

        for idx,weight in enumerate(weightArray): 
            listOfValidActionsWithCountOfItemsInferedByWeights += [idx]*weight # inserts "weight"-times an action (= index of operation; see: COMPLEX_MOVEMENT)

        return random.choice(listOfValidActionsWithCountOfItemsInferedByWeights)

    def badSearchMovement(self, state, reward, done, info, env):
        maskGoomba = (state[194] == self.sm_images.goombaColor).all(axis = 1)
        maskPit = (state[210] == self.sm_images.skyColor).all(axis = 1)

        if np.any(maskGoomba):
            return sm_movement.bigJump(env, reward, done, info)
        else:
            if np.any(maskPit):
                return sm_movement.bigJump(env, reward, done, info)
            else:
                return env.step(sm_movement.weightedRandom(sm_movement.basicWeights))

class Mario2DMap():
    def __init__(self):
        self.environment = np.array([[" "]*16]*16)

    def printEnvironment(self):
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

    def reloadEnvironment(self):
        self.environment = np.array([[" "]*16]*16)

    def changeEnvironment(self, loc, symbol):
        for pt in zip(*loc[::-1]):
            x = round(pt[0] / 16)
            y = round(pt[1] / 16)
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

    #state, reward, done, info = sm_movement.badSearchMovement(state, reward, done, info, env)
    state, reward, done, info = env.step(sm_movement.weightedRandom(sm_movement.basicWeights))
    #state, reward, done, info = sm_movement.bigJump(env, reward, done, info)
    #state, reward, done, info = env.step(random.randint(0,len(COMPLEX_MOVEMENT)-1))
    #state, reward, done, info = env.step(1)


    sm_env.reloadEnvironment()
    sm_env.changeEnvironment(sm_images.detectQuestionBox(False), "?")
    sm_env.changeEnvironment(sm_images.detectBlock(False), "B")
    sm_env.changeEnvironment(sm_images.detectFloor(False), "@")
    sm_env.changeEnvironment(sm_images.detectGoomba(False),"G")
    sm_env.changeEnvironment(sm_images.detectMario(False), "M")

    print(sm_env.printEnvironment())

    env.render()
    time.sleep(0.02)
env.close()