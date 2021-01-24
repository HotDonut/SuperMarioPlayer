from enum import Enum

##
# This class is an Enumclass. We use it for readable code and to reduce the usage of random numbers
# @author Weiskirchner Florian
# @version 23. January 2021 (erstellungsdatum)
#
# @param the Enum Movement contains all usable options from COMPLEX_MOVEMENT in SuperMarioPlayer.py
##
class Movement(Enum):
    NOOP = 0
    right = 1
    rightA = 2
    rightB = 3
    rightAB = 4
    A = 5
    left = 6
    leftA = 7
    leftB = 8
    leftAB = 9
    down = 10
    up = 11
