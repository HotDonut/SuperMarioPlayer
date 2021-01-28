from ctypes import *
from os import system

from src.SuperMarioConfig import SuperMarioConfig as SuperMarioConfig

class COORD(Structure):
    pass  # like noop - no operation

COORD._fields_ = [("X", c_short), ("Y", c_short)]

class SuperMarioConsoleDebugWindow:

    def __init__(self):
        # Output Handles to interact with Windows Command Line
        self.STD_OUTPUT_HANDLE = -11
        self.handle = windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)
        

    ##
    # This method prints any output to the Windows Command Line.
    # Existing Output will be overwritten
    #
    # @author Lukas Geyrhofer
    # @param output String which to print to the Command Line
    ##
    def debugPrint(self, output):
        # when true use another display method more suitable for windows systems
        if(SuperMarioConfig.WindowsConsoleOutput):
            c = output.encode("windows-1252")
            windll.kernel32.SetConsoleCursorPosition(self.handle, COORD(0, 0))
            windll.kernel32.WriteConsoleA(self.handle, c_char_p(c), len(c), None, None)
        else:
            print(output)

    ##
    # This method clears the Windows Command Line completely.
    #
    # @author Lukas Geyrhofer
    ##
    def clear(self):
        if(SuperMarioConfig.WindowsConsoleOutput):
            system("cls")
            windll.kernel32.SetConsoleCursorPosition(self.handle, COORD(0, 1))
            clearCommand = " " * 80
            c = clearCommand.encode("windows-1252")
            windll.kernel32.WriteConsoleA(self.handle, c_char_p(c), len(c), None, None)
