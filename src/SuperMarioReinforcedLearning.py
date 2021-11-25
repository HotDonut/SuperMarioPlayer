import numpy as np
from tensorflow.keras import Model, Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

class SuperMarioReinforcedLearning():
    def __init__(self, theMap):
        self.map = theMap
        self.inputs = 0

        self.model = Sequential()
        self.model.add(Dense(120, input_dim = 240, activation = "relu"))
        self.model.add(Dense(120, activation="relu"))
        self.model.add(Dense(11, activation="softmax"))
        self.model.compile(optimizer=Adam(), loss="sparse_categorical_crossentropy", metrics=["sparse_categorical_accuracy"])



    def saveNeuralNetwork(self):
        pass

    def loadNeuralNetwork(self):
        pass

    def deleteNeuralNetwork(self):
        pass

    def nextStep(self):
        pass

    def transformMap(self):
        evilSymbols = ["G", "C", "U"] #goomba, cooper, shell
        neutralSymbols = ["?", "B", "@", "P", "S", "L"] #questionbox, block, stone, pipe, stairs, lift

        # convert 2D to 1D array
        inputs = self.map.environment.flatten()
        # be able to store strings of length 3
        inputs = inputs.astype("U3")

        #replace all symbols with values
        inputs[inputs == " "] = 0
        inputs[inputs == "M"] = 100
        inputs[:] = [200 if x in neutralSymbols else x for x in inputs]
        inputs[:] = [300 if x in evilSymbols else x for x in inputs]

        #convert to float for neural network
        inputs = inputs.astype(float)

        print(type(inputs))
        print(inputs)