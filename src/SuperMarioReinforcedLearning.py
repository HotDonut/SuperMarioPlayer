import random
import numpy as np
import tensorflow as tf
import cv2
from tensorflow.keras.models import clone_model, load_model, save_model
from tensorflow.keras import Model, Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow_core.python.keras import regularizers


class SuperMarioReinforcedLearning():
    def __init__(self):
        np.random.seed(42)
        tf.random.set_seed(42)

        self.lambda_value = 0.9
        self.learningRate = 0.1
        self.experience_replay_length = 8000
        self.reduction_rate = 0.20

        self.inputs = 0
        self.prediction_list_buffer = None
        self.saved_inputs = []
        self.saved_predictions = []
        self.iteriationInCurrentBatch = 0
        self.train_iterations = 0
        self.macro_iterations = 0
        self.macro_cycle = 3
        self.batchSize = 100
        self.train_inputs = None
        self.train_labels = None
        self.epsilon = 0.01


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
            calculated_action = random.randint(0, 6)
        else:
            calculated_action = np.argmax(prediction_list)

        # save state and outcome with temporal difference for learning
        if self.prediction_list_buffer is not None:

            # calculate temporal difference for learning
            updated_Q_value = self.lossFunction(reward, prediction_list[0][calculated_action])

            self.prediction_list_buffer[0][np.argmax(self.prediction_list_buffer)] = updated_Q_value
            self.saved_inputs.append(self.inputs_buffer)
            self.saved_predictions.append(self.prediction_list_buffer)


        self.prediction_list_buffer = prediction_list

        #if self.iteriationInCurrentBatch % self.batchSize is 0:
        #   self.train()



        return calculated_action

    def lossFunction(self, reward, maxQValue):
        # see loss function image in working directory
        return self.prediction_list_buffer[0][np.argmax(self.prediction_list_buffer)] + self.learningRate * (reward + self.lambda_value * maxQValue - self.prediction_list_buffer[0][np.argmax(self.prediction_list_buffer)])

    def train(self):
        print("Episode:", self.train_iterations)
        self.train_iterations += 1

        if len(self.saved_inputs) > self.experience_replay_length:
            print("reducing experience replay")
            cutoff_index = int(self.experience_replay_length * self.reduction_rate)
            self.saved_inputs = self.saved_inputs[cutoff_index:]
            self.saved_predictions = self.saved_predictions[cutoff_index:]

        # print(inputs)
        # print(predictions)
        print(len(self.saved_inputs))

        self.main_model.fit(np.array(self.saved_inputs).reshape([-1, 240, 256, 3]), np.array(self.saved_predictions).reshape([-1, 7]), epochs=5, verbose=False)


        if self.train_iterations % self.macro_cycle is 0:
            self.target_model = clone_model(self.main_model)
            self.macro_iterations += 1
            print("copy weights to target network, macro cycle:", self.macro_iterations)




    def initNeuralNetwork(self):
        self.target_model = Sequential()
        self.target_model.add(Conv2D(64, (16, 16), strides=(4, 4), input_shape=(240, 256, 3), activation="relu", padding="same"))
        self.target_model.add(MaxPooling2D(pool_size=(4, 4), padding="same"))
        self.target_model.add(Conv2D(32, (4, 4), strides=(2, 2), activation="selu", padding="same"))
        self.target_model.add(Flatten())
        self.target_model.add(Dense(120, activation="relu", kernel_regularizer=regularizers.l2(0.001)))
        self.target_model.add(Dense(60, activation="relu", kernel_regularizer=regularizers.l2(0.001)))
        self.target_model.add(Dense(7))  # linear activation
        self.target_model.compile(optimizer=Adam(), loss="mse", metrics=["accuracy"])
        self.target_model.summary()

        self.main_model = clone_model(self.target_model)
        self.main_model.compile(optimizer=Adam(), loss="mse", metrics=["accuracy"])
    def saveNeuralNetwork(self):
        print("\nsaving network")
        self.target_model.save('saved_model.h5')
        # self.target_model.save_weights("saved_model_weights", save_format="tf")
        file = open("saved_model_stats.txt", "w+")
        file.write(str(self.train_iterations) + "\n" + str(self.macro_iterations))
        file.close()

    def loadNeuralNetwork(self, modelpath='saved_model.h5', statspath="saved_model_stats.txt"):
        self.target_model = load_model(modelpath, compile=True)
        self.target_model.compile(optimizer=Adam(), loss="mse", metrics=["accuracy"])
        self.target_model.summary()
        self.main_model = clone_model(self.target_model)
        self.main_model.compile(optimizer=Adam(), loss="mse", metrics=["accuracy"])
        with open(statspath, "r") as file:
            self.train_iterations = int(file.readline())
            self.macro_iterations = int(file.readline())

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