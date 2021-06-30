import json
from os import path

##
# This class contains all important configuration information of the game
# Furthermore it contains functions to convert the configuration into a json file and vice versa
#
# @author Wolfgang Mair, Lukas Geyrhofer
# @version 07. May 2021
##

class SuperMarioConfig:
    ##
    # This method loads a configuration from a json file.
    # It then writes the values into the SuperMarioConfig instance it was called from
    # Existing Output will be overwritten
    # If an error occurs an corresponding text will be printed, the external config file will be ignored and the default values will be used
    #
    # @author Wolfgang Mair, Lukas Geysrhofer
    # @param file_path The string path to the json file
    ##
    def __init__(self, file_path):

        if(path.exists(file_path)):
            config_text = ""
            with open(file_path, 'r') as configFile:
                config_text = configFile.read()

            try:
                jsonData = json.loads(config_text)

                self.WindowsConsoleOutput = bool(jsonData["WindowsConsoleOutput"])
                self.ConsoleFramerate = int(jsonData["ConsoleFramerate"])
                self.RenderFramerate = int(jsonData["RenderFramerate"])
                self.JumpingFailedBecausePressedToEarly = int(jsonData["JumpingFailedBecausePressedToEarly"])
                self.imageAssetsDirectory = jsonData["imageAssetsDirectory"]
                self.markovStatesPath = jsonData["markovStatesPath"]
                self.markovStateDimensions = jsonData["markovStateDimensions"]
                self.debugAll = bool(jsonData["debugAll"])
                self.themeIdentifier = jsonData["themeIdentifier"]
                self.imageDetectionConfiguration = jsonData["imageDetectionConfiguration"]

            except:
                print("Config file contained an invalid value for one of the parameters. Using default values to continue.")

        else:
            print("Config file not found. Using default values to continue.")

    def getWindowsConsoleOutput(self):
        return self.WindowsConsoleOutput
