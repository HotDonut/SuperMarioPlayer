from ctypes import *
from os import system

# Output Handles to interact with Windows Command Line
STD_OUTPUT_HANDLE = -11
h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


class COORD(Structure):
    pass


COORD._fields_ = [("X", c_short), ("Y", c_short)]


##
# This method prints any output to the Windows Command Line.
# Existing Output will be overwritten
#
# @author Lukas Geyrhofer
# @param output String which to print to the Command Line
##
def print_nice(output):
    c = output.encode("windows-1252")
    windll.kernel32.SetConsoleCursorPosition(h, COORD(0, 0))
    windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)


##
# This method clears the Windows Command Line completely.
#
# @author Lukas Geyrhofer
##
def clear_cmd():
    system("cls")
    windll.kernel32.SetConsoleCursorPosition(h, COORD(0, 1))
    clearCommand = " " * 80
    c = clearCommand.encode("windows-1252")
    windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)
