from PIL import Image
import numpy as np
import cv2


class Images:
    goombaImage = cv2.imread('goomba.png', 0)
    marioImage = cv2.imread('mario.png', 0)
    questionBoxImage = cv2.imread('questionbox.png', 0)
    questionBoxImageLight = cv2.imread('questionbox_light.png', 0)
    blockImage = cv2.imread('block.png', 0)
    floorImage = cv2.imread('floor.png', 0)
    pipeImage = cv2.imread('pipe.png', 0)
    cooperImage = cv2.imread('cooper.png', 0)
    stairBlockImage = cv2.imread('stairBlock.png', 0)
    img_gray = 0
    state = 0

    def __init__(self):
        # Goomba, boxes and floor have the same color
        # cannot be used for value at goombas
        self.goombaColor = np.array([228, 92, 16])

        # Pits and background Sky
        self.skyColor = np.array([104, 136, 252])

        # Goomba Eye array
        self.goombaEyeArray = np.array(
            [[228, 92, 16], [228, 92, 16], [228, 92, 16], [240, 208, 176], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
             [0, 0, 0], [0, 0, 0], [240, 208, 176], [228, 92, 16], [228, 92, 16], [228, 92, 16]])

        # Pipe array
        self.pipeArray = np.array(
            [[0, 0, 0], [184, 248, 24], [184, 248, 24], [184, 248, 24], [0, 168, 0], [0, 168, 0], [184, 248, 24],
             [184, 248, 24], [184, 248, 24], [184, 248, 24], [184, 248, 24], [0, 168, 0], [184, 248, 24],
             [184, 248, 24]])

        # Koopa array
        self.koopaShellArray = np.array(
            [[252, 252, 252], [0, 168, 0], [0, 168, 0], [0, 168, 0], [0, 168, 0], [252, 168, 68], [0, 168, 0],
             [252, 252, 252], [252, 252, 252], [252, 168, 68]])

    def processImage(self):
        # converts state (pixel array) to image
        img = Image.fromarray(self.state, 'RGB')
        self.img_gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)

    def detect(self, template, threshold, color, debug):
        res = cv2.matchTemplate(self.img_gray, template, cv2.TM_CCOEFF_NORMED)

        loc = np.where(res >= threshold)
        #  print(loc)
        if debug:
            for pt in zip(*loc[::-1]):
                # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                # print(pt[0], pt[1])
                self.state[:, pt[0]] = color
                self.state[pt[1], :] = color
                print("Goomba position x:", pt[0] / 16, "Goomba position y:", pt[1] / 16, "\n")
        return loc

    def detectMario(self, state, debug):
        self.state = state
        self.processImage()
        # w, h = self.marioImage.shape[::-1]
        color = [255, 0, 0]

        res = cv2.matchTemplate(self.img_gray, self.marioImage, cv2.TM_CCOEFF_NORMED)
        threshold = 0.7
        loc = np.where(res >= threshold)
        #  print(loc)
        # Normalizing detection of mario to top left corner
        if len(loc[0]) != 0:
            loc[0][0] = loc[0][0] - 2
            loc[1][0] = loc[1][0] - 6
        if debug:
            for pt in zip(*loc[::-1]):
                # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                # print(pt[0], pt[1])
                state[:, pt[0]] = color
                state[pt[1], :] = color
                print("Mario position x:", pt[0] / 16, "Mario position y:", pt[1] / 16, "\n")
        return loc

    def detectGoomba(self, state, debug):
        self.state = state
        self.processImage()
        color = [0, 0, 0]
        threshold = 0.5

        return self.detect(self.goombaImage, threshold, color, debug)

    def detectQuestionBox(self, state, debug):
        self.state = state
        self.processImage()
        color = [0, 255, 0]
        threshold = 0.9

        return self.detect(self.questionBoxImage, threshold, color, debug)

    def detectQuestionBoxlight(self, state, debug):
        self.state = state
        self.processImage()
        color = [0, 255, 0]
        threshold = 0.9

        return self.detect(self.questionBoxImageLight, threshold, color, debug)

    def detectBlock(self, state, debug):
        self.state = state
        self.processImage()
        color = [0, 255, 0]
        threshold = 0.9

        return self.detect(self.blockImage, threshold, color, debug)

    def detectFloor(self, state, debug):
        self.state = state
        self.processImage()
        color = [0, 255, 255]
        threshold = 0.8

        return self.detect(self.floorImage, threshold, color, debug)

    def detectPipe(self, state, debug):
        self.state = state
        self.processImage()
        color = [0, 255, 255]
        threshold = 0.9

        return self.detect(self.pipeImage, threshold, color, debug)

    def detectCooper(self, state, debug):
        self.state = state
        self.processImage()
        color = [0, 100, 255]
        threshold = 0.6

        return self.detect(self.cooperImage, threshold, color, debug)

    def detectStairBlock(self, state, debug):
        self.state = state
        self.processImage()
        color = [100, 100, 255]
        threshold = 0.9

        return self.detect(self.stairBlockImage, threshold, color, debug)
