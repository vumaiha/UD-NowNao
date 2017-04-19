# UD-NowNao
Code for University of Delaware's Nao, Dash, and Dot robots in the GEAR Lab. 
The goal of the program is to have interactive robots that would entice children to move.

04/19/207

=========================================================================================
Code written be Caili Li.
Maintained and Modified by Kristina Strother-Garcia (kmsg@udel.edu) and Mai Ha Vu (maiha@udel.edu).

==========================================================================================
Copyright 2017 University of Delaware.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
==============================================================================

Laptop (specific for the laptop in the GEAR lab)
-----------------------------------------------
-Press power button then mash F12
-Default: legacy boot, hit Enter
-connect to CorobotNetwork

==================================================

Dash
-------------------------------------------------------
-Terminal: python /home/cooplab/git-codes/UD-NowNao/Dash/Dash.py
-Press Connect
-Input focus must be on GUI to control
-Use arrow keys to control
-F key: random sound
-D key: disco mode
-A key: random animal sound

==================================================

NAO
---
-Long press to boot up / shut down
-Short press gives network status
-Double press to turn off autonomous life mode
-Weird sound? Short press to hear warning
-Connect control pad to laptop before running script
-Terminal: python /home/cooplab/git-codes/UD-NowNao/NAO/NAOControl.py
-Press h for help, x to exit

Control Pad
-----------
-Switch must be set to PC (not PS3)
-Preset light must be off
-Home button must be green (not red)
-SE button = stand
-ST button = sit (rest - saves energy)

Left Stick
----------
-Push/pull = forward/backward march
-Rocker = full turn
-#5 = "Wow!"
-#6 = "Hey! Over here!"
-#7 = "Good job" + Name of the child
-#8 (while pushed) = Music
-#9 = "Yay!"
-#10 = Say input

Right Stick
------------
-Hold L1 for fast movement
-Y axis push/pull = shoulder pitch down/up
-X axis left/right = shoulder roll
-Twist = elbow roll
-L3/R3 = elbow pitch
-Tiny thumbstick = head movement

Keyboard
---------
1 = set stiffness for right arm
2/0 = set stiffness for body (on/off)
3 = set stiffness for head
r = rest
f = wake-up
v = stand
d = disco
s = play
n = input Name
i = input text (for text to speech)
l = list postures
p = set posture




