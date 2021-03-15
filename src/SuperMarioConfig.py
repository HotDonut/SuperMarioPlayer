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
