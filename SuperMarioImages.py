from PIL import Image
import numpy as np
import cv2

class Images():
    goombaImage = cv2.imread('goomba.png', 0)
    marioImage = cv2.imread('mario.png', 0)
    questionBoxImage = cv2.imread('questionbox.png', 0)
    questionBoxImageLight = cv2.imread('questionbox_light.png', 0)
    blockImage = cv2.imread('block.png', 0)
    floorImage = cv2.imread('floor.png', 0)
    pipeImage  = cv2.imread('pipe.png', 0)

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

    @staticmethod
    def processImage(state):
        # converts state (pixel array) to image
        img = Image.fromarray(state, 'RGB')
        img_rgb = np.array(img)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        return img_gray, img_rgb

    def detectGoomba(self, state, debug):
        img_gray, img_rgb = self.processImage(state)
        w, h = self.goombaImage.shape[::-1]
        color = [0, 0, 0]

        res = cv2.matchTemplate(img_gray, self.goombaImage, cv2.TM_CCOEFF_NORMED)
        threshold = 0.5
        loc = np.where(res >= threshold)
        #  print(loc)
        if debug:
            for pt in zip(*loc[::-1]):
                # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                # print(pt[0], pt[1])
                state[:, pt[0]] = color
                state[pt[1], :] = color
                print("Goomba position x:", pt[0] / 16, "Goomba position y:", pt[1] / 16, "\n")
        return loc
        # cv2.imwrite('res.png', img_rgb)
        # img.show()

    def detectMario(self, state, debug):
        img_gray, img_rgb = self.processImage(state)
        w, h = self.marioImage.shape[::-1]
        color = [255, 0, 0]

        res = cv2.matchTemplate(img_gray, self.marioImage, cv2.TM_CCOEFF_NORMED)
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
        # cv2.imwrite('res.png', img_rgb)
        # img.show()

    def detectQuestionBox(self, state, debug):
        img_gray, img_rgb = self.processImage(state)
        w, h = self.questionBoxImage.shape[::-1]
        color = [0, 255, 0]

        threshold = 0.9
        res = cv2.matchTemplate(img_gray, self.questionBoxImage, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        if debug:
            for pt in zip(*loc[::-1]):
                # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 1)
                # print(pt[0], pt[1])
                state[:, pt[0]] = color
                state[pt[1], :] = color
                print("QuestionBox position x:", pt[0] / 16, "QuestionBox position y:", pt[1] / 16, "\n")

        return loc
        # cv2.imwrite('res.png', img_rgb)
        # img.show()

    def detectQuestionBoxlight(self, state, debug):
        img_gray, img_rgb = self.processImage(state)
        w, h = self.questionBoxImageLight.shape[::-1]
        color = [0, 255, 0]

        threshold = 0.9
        res = cv2.matchTemplate(img_gray, self.questionBoxImageLight, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        if debug:
            for pt in zip(*loc[::-1]):
                # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 1)
                # print(pt[0], pt[1])
                state[:, pt[0]] = color
                state[pt[1], :] = color
                print("QuestionBox position x:", pt[0] / 16, "QuestionBox position y:", pt[1] / 16, "\n")

        return loc
        # cv2.imwrite('res.png', img_rgb)
        # img.show()

    def detectBlock(self, state, debug):
        img_gray, img_rgb = self.processImage(state)
        w, h = self.blockImage.shape[::-1]
        color = [0, 255, 0]

        res = cv2.matchTemplate(img_gray, self.blockImage, cv2.TM_CCOEFF_NORMED)
        threshold = 0.9
        loc = np.where(res >= threshold)
        #  print(loc)
        if debug:
            for pt in zip(*loc[::-1]):
                # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 1)
                # print(pt[0], pt[1])
                state[:, pt[0]] = color
                state[pt[1], :] = color
                print("BrickBlock position x:", pt[0] / 16, "BrickBlock position y:", pt[1] / 16, "\n")
        return loc
        # cv2.imwrite('res.png', img_rgb)
        # img.show()

    def detectFloor(self, state, debug):
        img_gray, img_rgb = self.processImage(state)
        w, h = self.floorImage.shape[::-1]
        color = [0, 255, 255]

        res = cv2.matchTemplate(img_gray, self.floorImage, cv2.TM_CCOEFF_NORMED)
        threshold = 0.80
        loc = np.where(res >= threshold)
        #  print(loc)
        if debug:
            for pt in zip(*loc[::-1]):
                # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 1)
                # print(pt[0], pt[1])
                state[:, pt[0]] = color
                state[pt[1], :] = color
                print("FloorBlock position x:", pt[0] / 16, "FloorBlock position y:", pt[1] / 16, "\n")
        return loc
        # cv2.imwrite('res.png', img_rgb)
        # img.show()

    def detectPipe(self, state, debug):
        img_gray, img_rgb = self.processImage(state)
        w, h = self.pipeImage.shape[::-1]
        color = [0, 255, 255]

        res = cv2.matchTemplate(img_gray, self.pipeImage, cv2.TM_CCOEFF_NORMED)
        threshold = 0.90
        loc = np.where(res >= threshold)
        #  print(loc)
        if debug:
            for pt in zip(*loc[::-1]):
                # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 1)
                # print(pt[0], pt[1])
                state[:, pt[0]] = color
                state[pt[1], :] = color
                print("Pipe position x:", pt[0] / 16, "Pipe position y:", pt[1] / 16, "\n")
        return loc
        # cv2.imwrite('res.png', img_rgb)
        # img.show()

