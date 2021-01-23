from ctypes import *
from os import system

STD_OUTPUT_HANDLE = -11


class COORD(Structure):
    pass


COORD._fields_ = [("X", c_short), ("Y", c_short)]


def print_nice(output):
    system('cls')

    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleCursorPosition(h, COORD(0, 1))
    clearCommand = " " * 80
    c = clearCommand.encode("windows-1252")
    windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)

    c = output.encode("windows-1252")
    windll.kernel32.SetConsoleCursorPosition(h, COORD(0, 0))
    windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)
