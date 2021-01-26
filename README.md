# SuperMarioPlayer

Real world problems mapped on the classic computer game Super Mario 1.

Hereby we want to make complex decisions based on sensor data (similar to smart manufacturing problems).

The environment is based on openAI/Gym ( see: https://github.com/Kautenja/gym-super-mario-bros )

## Install

* and IDE of your choice for python
* Python / Pip

* pip install gym
* pip install numpy
* pip install gym-super-mario-bros
* pip install opencv-python

## Run

python SuperMarioPlayer.py

# Project Config

* SuperMarioConsoleDebugWindow
  * print_nice: for cmd friendly output (windows)
* SuperMarioEnvironment
  * consoleFramerate: amount of frames skipped in standard out
  * renderFramerate:  amount of frames skipped in open-ai-gym rendering window

  * detect-blocks: enable cross-line for debugging the object detection (open-cv)
* SuperMarioImages:
  * treshholds, cross-line colors


