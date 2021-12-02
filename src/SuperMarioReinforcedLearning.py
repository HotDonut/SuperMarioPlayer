import random
import numpy as np
import tensorflow as tf
import cv2
from tensorflow.keras.models import clone_model, load_model
from tensorflow.keras import Model, Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow_core.python.keras import regularizers


class SuperMarioReinforcedLearning():
    def __init__(self):
        np.random.seed(42)
        tf.random.set_seed(42)

        self.lambda_value = 0.9

        self.inputs = 0
        self.prediction_list_buffer = None
        self.saved_experiences = []
        self.iteriationInCurrentBatch = 0
        self.train_iterations = 0
        self.macro_iterations = 0
        self.macro_cycle = 10
        self.batchSize = 100
        self.save_cycle = 10
        self.epsilon = 0.05


    def nextStep(self, reward, action_taken, picture):
        self.iteriationInCurrentBatch += 1
        # cropped = picture[0:200,100:200]
        # converted = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        picture = picture.reshape([-1, 240, 256, 3])

        # save current state(input) for later calculations
        self.inputs_buffer = picture

        # compute q values
        prediction_list = self.target_model.predict([picture])

        # get action with highest q value or explore
        if random.uniform(0, 1) < self.epsilon:
            calculated_action = random.randint(1, 10)
        else:
            calculated_action = np.argmax(prediction_list)

        # calculate temporal difference for learning
        temporal_difference = self.calculateTemporalDifference(reward, prediction_list[0][calculated_action])

        # save state and outcome with temporal difference for learning
        if self.prediction_list_buffer is not None:
            self.prediction_list_buffer[0][action_taken] = temporal_difference
            self.saved_experiences.append([self.inputs_buffer, self.prediction_list_buffer])


        self.prediction_list_buffer = prediction_list

        if self.iteriationInCurrentBatch % self.batchSize is 0:
            self.train()



        return calculated_action

    def calculateTemporalDifference(self, reward, maxQValue):
        return reward + self.lambda_value * maxQValue

    def train(self):
        print("training cycle:", self.train_iterations)
        self.train_iterations += 1

        inputs = np.reshape(np.array([item[0] for item in self.saved_experiences]), (-1, 240, 256, 3))
        predictions = np.reshape(np.array([item[1] for item in self.saved_experiences]), (-1, 11))

        # print(inputs)
        # print(predictions)

        self.main_model.fit(inputs, predictions, epochs=1, verbose=False)
        self.saved_experiences.clear()

        if self.train_iterations % self.macro_cycle is 0:
            self.target_model = clone_model(self.main_model)
            self.macro_iterations += 1
            self.saveNeuralNetwork()
            print("\nsaving network")
            print("copy weights to target network, macro cycle:", self.macro_iterations)


    def initNeuralNetwork(self):
        self.main_model = Sequential()
        self.main_model.add(Conv2D(64, (16, 16), strides=(4, 4), input_shape=(240, 256, 3), activation="relu", padding="same"))
        self.main_model.add(MaxPooling2D(pool_size=(4, 4), padding="same"))
        self.main_model.add(Conv2D(32, (4, 4), strides=(2, 2), activation="selu", padding="same"))
        self.main_model.add(Flatten())
        self.main_model.add(Dense(120, activation="relu", kernel_regularizer=regularizers.l2(0.001)))
        self.main_model.add(Dense(60, activation="relu", kernel_regularizer=regularizers.l2(0.001)))
        self.main_model.add(Dense(11))  # linear activation
        self.main_model.compile(optimizer=Adam(), loss="mse", metrics=["accuracy"])
        self.main_model.summary()

        self.target_model = clone_model(self.main_model)

    def saveNeuralNetwork(self):
        self.target_model.save('saved_model.h5')
        file = open("saved_model_stats.txt", "w")
        file.write(str(self.train_iterations) + "\n" + str(self.macro_iterations))
        file.close()

    def loadNeuralNetwork(self):
        self.main_model = load_model('saved_model.h5')
        self.main_model.compile(optimizer=Adam(), loss="mse", metrics=["accuracy"])
        self.main_model.summary()
        self.target_model = clone_model(self.main_model)
        file = open("saved_model_stats.txt", "r")
        self.train_iterations = int(file.readline())
        self.macro_iterations = int(file.readline())
        pass

    def deleteNeuralNetwork(self):
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
        self.inputs = inputs.astype(float)
        self.inputs = np.reshape(self.inputs, (1, 240))

        # print(type(inputs))
        # print(inputs)