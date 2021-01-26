from ctypes import *
from os import system

# If this flag is set to true console output will be better when using Windows Command Line. Set to False
# if not using Windows or when not using the Windows Command Line to execute the script.
niceConsoleOutput = False

# Output Handles to interact with Windows Command Line
STD_OUTPUT_HANDLE = -11
handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

class COORD(Structure):
    pass # like noop - no operation

COORD._fields_ = [("X", c_short), ("Y", c_short)]

##
# This method prints any output to the Windows Command Line.
# Existing Output will be overwritten
#
# @author Lukas Geyrhofer
# @param output String which to print to the Command Line
##
def debugPrint(output):
    # when true use another display method more suitable for windows systems
    if(niceConsoleOutput):
        c = output.encode("windows-1252")
        windll.kernel32.SetConsoleCursorPosition(handle, COORD(0, 0))
        windll.kernel32.WriteConsoleA(handle, c_char_p(c), len(c), None, None)
    else:
        print(output)

##
# This method clears the Windows Command Line completely.
#
# @author Lukas Geyrhofer
##
def clear():
    if(niceConsoleOutput):
        system("cls")
        windll.kernel32.SetConsoleCursorPosition(handle, COORD(0, 1))
        clearCommand = " " * 80
        c = clearCommand.encode("windows-1252")
        windll.kernel32.WriteConsoleA(handle, c_char_p(c), len(c), None, None)
