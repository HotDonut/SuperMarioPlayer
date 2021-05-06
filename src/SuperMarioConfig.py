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

    # If this flag is set to true console output will be better when using Windows Command Line. Set to False
    # if not using Windows or when not using the Windows Command Line to execute the script.
    WindowsConsoleOutput = True

    # Specifies the frame rate for the console output. Must be a value >= 0. 
    # 0 is maximum framerate. A framerate of e.g. 20 only shows every 20th frame.
    ConsoleFramerate = 0
    RenderFramerate = 0

    DebugQuestionBoxDetection = False
    DebugQuestionBoxLightDetection = False
    DebugBlockDetection = False
    DebugFloorDetection = False
    DebugPipeDetection = False
    DebugCooperDetection = False
    DebugStairDetection = False
    DebugMarioDetection = False
    DebugGoombaDetection = False

    JumpingFailedBecausePressedToEarly = 50

    ##
    # This method returns the SuperMarioConfig class variables (configurtations) as Dictionary which is also usable for the JSON conversion method json.dumps().
    #
    # @author Wolfgang Mair
    # @param A SuperMarioConfig instance
    # @return   A dictionary filled with the current variable values of the SuperMarioConfig instance the method was called from
    ##
    def encoder_config(self, config):
        if isinstance(config, SuperMarioConfig):
            return {
                'WindowsConsoleOutput': SuperMarioConfig.WindowsConsoleOutput,
                'ConsoleFramerate': SuperMarioConfig.ConsoleFramerate,
                'RenderFramerate': SuperMarioConfig.RenderFramerate,
                'DebugQuestionBoxDetection': SuperMarioConfig.DebugQuestionBoxDetection,
                'DebugQuestionBoxLightDetection': SuperMarioConfig.DebugQuestionBoxLightDetection,
                'DebugBlockDetection': SuperMarioConfig.DebugBlockDetection,
                'DebugFloorDetection': SuperMarioConfig.DebugFloorDetection,
                'DebugPipeDetection': SuperMarioConfig.DebugPipeDetection,
                'DebugCooperDetection': SuperMarioConfig.DebugCooperDetection,
                'DebugStairDetection': SuperMarioConfig.DebugStairDetection,
                'DebugMarioDetection': SuperMarioConfig.DebugMarioDetection,
                'DebugGoombaDetection': SuperMarioConfig.DebugGoombaDetection,
                'JumpingFailedBecausePressedToEarly': SuperMarioConfig.JumpingFailedBecausePressedToEarly
            }
        raise TypeError(f'Object {config} is not of type SuperMarioConfig.')

    ##
    # This method creates a json string by using the encoder_config method and json.dumps()
    #
    # @author Wolfgang Mair
    # @return   A json string of the SuperMarioConfig values
    ##
    def encode(self):
        return json.dumps(self, default=self.encoder_config, indent=4)

    ##
    # This method writes the json string of SuperMarioConfig into a file.
    # The file is named DebugConfigInfo.json and can be used to get the current configuration in the debug mode
    #
    # @author Wolfgang Mair
    ##
    def write_json_file(self):
        with open('DebugConfigInfo.json', 'w') as configFile:
            configFile.write(self.encode())

    ##
    # This method loads a configuration from a json file.
    # It then writes the values into the SuperMarioConfig instance it was called from
    # Existing Output will be overwritten
    # If an error occurs an corresponding text will be printed, the external config file will be ignored and the default values will be used
    #
    # @author Wolfgang Mair
    # @param file_path The string path to the json file
    ##
    def load_config(self, file_path):

        if(path.exists(file_path)):
            config_text = ""
            with open(file_path, 'r') as configFile:
                config_text = configFile.read()

            try:
                jsonData = json.loads(config_text)
                SuperMarioConfig.WindowsConsoleOutput = bool(jsonData["WindowsConsoleOutput"])
                SuperMarioConfig.ConsoleFramerate = int(jsonData["ConsoleFramerate"])
                SuperMarioConfig.RenderFramerate = int(jsonData["RenderFramerate"])
                SuperMarioConfig.DebugQuestionBoxDetection = bool(jsonData["DebugQuestionBoxDetection"])
                SuperMarioConfig.DebugQuestionBoxLightDetection = bool(jsonData["DebugQuestionBoxLightDetection"])
                SuperMarioConfig.DebugBlockDetection = bool(jsonData["DebugBlockDetection"])
                SuperMarioConfig.DebugFloorDetection = bool(jsonData["DebugFloorDetection"])
                SuperMarioConfig.DebugPipeDetection = bool(jsonData["DebugPipeDetection"])
                SuperMarioConfig.DebugCooperDetection = bool(jsonData["DebugCooperDetection"])
                SuperMarioConfig.DebugStairDetection = bool(jsonData["DebugStairDetection"])
                SuperMarioConfig.DebugMarioDetection = bool(jsonData["DebugMarioDetection"])
                SuperMarioConfig.DebugGoombaDetection = bool(jsonData["DebugGoombaDetection"])
                SuperMarioConfig.JumpingFailedBecausePressedToEarly = int(jsonData["JumpingFailedBecausePressedToEarly"])
            except:
                print("Config file contained an invalid value for one of the parameters. Using default values to continue.")

        else:
            print("Config file not found. Using default values to continue.")