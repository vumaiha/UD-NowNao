# Python AR.Drone 2.0
#
# Copyright (C) 2013 Quadeare <lacrampe.florian@gmail.com>
# Twitter : @quadeare

ROBOT_IP = "192.168.1.140"
PORT = 9559

from pygame import *  
import pygame
import threading
import thread
import time
from subprocess import call
import readchar

import signal 
import sys

#import CameraPreview

from naoqi import ALProxy

import NAOSound_KSG
import motion_setFootStepDance
import sensors_touch

motionProxy  = ALProxy("ALMotion", ROBOT_IP, PORT)
postureProxy = ALProxy("ALRobotPosture", ROBOT_IP, PORT)
speakProxy = ALProxy("ALTextToSpeech", ROBOT_IP, PORT)
LEDProxy = ALProxy("ALLeds", ROBOT_IP, PORT)
aup = ALProxy("ALAudioPlayer", ROBOT_IP, PORT)
anSpeakProxy = ALProxy("ALAnimatedSpeech", ROBOT_IP, PORT)

running = True
#cp = CameraPreview.CameraPreview()

gHatP = "(0, 0)"

X = 0
Y = 0
Theta = 0

sd = NAOSound_KSG.NAOSound()

def LEDDisco():
    LEDProxy.randomEyes(5)

def LEDeyes():
    LEDProxy.rotateEyes(880088,.5,1.5)

def Strick():
    motionProxy.angleInterpolation("RShoulderPitch", 0.4, 0.1, False)
    time.sleep(0.5)
    motionProxy.angleInterpolation("RShoulderPitch", -0.4, 0.1, False)

def CheckXYT():
    global _isRun
    global X
    global Y
    global Theta
    if X>1.0: X = 1.0
    if Y>1.0: Y = 1.0
    if Theta>1.0: Theta = 1.0
    if X<-1.0: X = -1.0
    if Y<-1.0: Y = -1.0
    if Theta<-1.0: Theta = -1.0

class controle(threading.Thread):
    """Control class (to control the drone)"""
    global running
    #global cp
    global gHatP
    def __init__(self, nom = ''):
        threading.Thread.__init__(self)
        self._stopevent = threading.Event( )
    def stop(self):
        self._stopevent.set( )
    def run(self):
        global X
    	global Y
    	global Theta
        global NameChild
	global SayInput
	global Posture

	NameChild = "" #default name empty
	SayInput = "Ooh!" #default TTS input
	Posture = "Crouch" #default posture
	
    
        """We call pygame (to use controler)"""
        pygame.init()
        clock = pygame.time.Clock()

        """Set up and init joystick"""
        j=joystick.Joystick(0) 
        j.init()
        #print "\rNumber of axes: " + str(j.get_numaxes())
	#print "\rNumber of balls: " + str(j.get_numballs())
        #print "\rNumber of buttons: " + str(j.get_numbuttons())
        #print "\rNumber of hats: " + str(j.get_numhats())
        
	gHatP = "(0, 0)"
        spd = 0.03

        while running:
            for event in pygame.event.get():

		"""When buttons are depressed"""
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0: #Right trigger
                        Strick()
			print "\rStrike"
                    elif event.button == 1: #L1 button
                        spd = 0.18
		    elif event.button == 2: #R3 button
                        motionProxy.changeAngles("RElbowRoll", -3, spd)
                    elif event.button == 3: #L3 button
                        motionProxy.changeAngles("RElbowRoll", 3, spd)
		    elif event.button == 4: #Button 5
			thread.start_new_thread(LEDeyes,())
                        speakProxy.say("Wow!")
			print "\rWow!"
                    elif event.button == 5: #Button 6
			thread.start_new_thread(LEDeyes,())  
                        anSpeakProxy.say("Hey! ^start(animations/Stand/Gestures/Hey_6) Over here! ^wait(animations/Stand/Gestures/Hey_6)")
			print "\rHey! Over here!"
		    elif event.button == 6: #Button 7
			thread.start_new_thread(LEDeyes,())  
			speakProxy.say("Good job" + NameChild)
			print "\rGood job"
                    elif event.button == 7: #Button 8
                        thread.start_new_thread(LEDDisco,())
			sd.Play()
			print "\rMusic"
                    elif event.button == 8: #Button 9
			thread.start_new_thread(LEDeyes,())                        
			speakProxy.say("Yay!")
			print "\rYay!"
                    elif event.button == 9: #Button 10
			#postureProxy.goToPosture(Posture, 1.0)
                        #print "\r" + Posture
			thread.start_new_thread(LEDeyes,())  
                        speakProxy.say(SayInput)
			print "\r" + SayInput
                    elif event.button == 10: #SE button
                        postureProxy.goToPosture("StandInit", 1.0)
			print "\rStand"
		    elif event.button == 11: #ST button
                        motionProxy.rest()
			print "\rRest"

		"""When buttons are released"""
                if event.type == pygame.JOYBUTTONUP:
                    if event.button == 1: #L1 button
                        spd = 0.1
                    elif event.button == 2: #R3 button
                        motionProxy.changeAngles("RElbowRoll", 0, spd)
                    elif event.button == 3: #L3 button
                        motionProxy.changeAngles("RElbowRoll", 0, spd)
		    elif event.button == 7: #Button 8
                        aup.stopAll()
			print "\rPlayback stopped"

		"""Joystick axis motion"""
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis == 0:
                        if event.value>0.1:
                            motionProxy.changeAngles("RShoulderRoll", -3, spd)
                        elif event.value<-0.1:
                            motionProxy.changeAngles("RShoulderRoll", 3, spd)
                        else: 
                            motionProxy.changeAngles("RShoulderRoll", 0, spd)
                    elif event.axis == 1:
			if event.value>0.1:
                            motionProxy.changeAngles("RShoulderPitch", -3, spd)
                        elif event.value<-0.1:
                            motionProxy.changeAngles("RShoulderPitch", 3, spd)
                        else: 
                            motionProxy.changeAngles("RShoulderPitch", 0, spd)
                    elif event.axis == 2:
                        X = -event.value
			CheckXYT()
                        motionProxy.moveToward(X, Y, Theta, [["Frequency", 1.0]])
		    elif event.axis == 3:
                        if event.value>0.1:
                            motionProxy.changeAngles("RElbowYaw", 3, spd)
                        elif event.value<-0.1:
                            motionProxy.changeAngles("RElbowYaw", -3, spd)
                        else: 
                            motionProxy.changeAngles("RElbowYaw", 0, spd)
		    elif event.axis == 4:
                        Theta = -float(event.value)/2
			CheckXYT()
                        motionProxy.moveToward(X, Y, Theta, [["Frequency", 1.0]])
		    elif event.axis == 5:
                        print "\rAxs 5: " + str(event.value)

		"""Joyhat (NAO head) motion"""
                if event.type == pygame.JOYHATMOTION:
		    if event.hat == 0:
			gHatP =  str(event.value)
                    if "0, -1" in gHatP:
	        	motionProxy.changeAngles("HeadPitch", -3, spd)
                    elif "-1, 0" in gHatP:
	        	motionProxy.changeAngles("HeadYaw", 3, spd)
                    elif "0, 1" in gHatP:
                        motionProxy.changeAngles("HeadPitch", 3, spd)
	    	    elif "1, 0" in gHatP:
	        	motionProxy.changeAngles("HeadYaw", -3, spd)
                    elif "0, 0" in gHatP:
                        motionProxy.changeAngles("HeadYaw", 0, spd)
                        motionProxy.changeAngles("HeadPitch", 0, spd)
            clock.tick(10000)

        print "\rBye bye!"
        quit()

key = "lol"

def KeyRead():
    global key
    global running
    global gHatP
    global NameChild
    global SayInput
    global Posture
    lock = threading.Lock()
    while running:
        with lock:
            key = readchar.readchar()
	    if key == 'x':
                running = False
                #cp.Close()
            elif key == 'h':
		print '\rx	quit.'      
                print '\rt	stop moving.'
        	print '\rr	rest.'
        	print '\rf	wake up.'
        	print '\rv	stand up.'
		print '\rd	play LED disco.'
		print '\rs	play random song.' 
		print '\rh	strick using the right arm.'          
		print '\r1	set stiffness for right arm.'
        	print '\r2	set stiffness for the body.'
	        print '\r3	set stiffness for the head.'
		print '\rn	type name of the baby.'
		print '\ri	type TTS input.'
		print '\rl	get posture list.'
		print '\rp	set posture.'
        	print '\r0	kill all stiffness.'
   	    elif key == '1':
                motionProxy.setStiffnesses('RArm', 1.0)
    	    elif key == '2':
        	 motionProxy.setStiffnesses('Body', 1.0)
	    elif key == '3':
        	 motionProxy.setStiffnesses('Head', 1.0)
    	    elif key == '0':
        	motionProxy.setStiffnesses('Body', 0.0)
            elif key == 'r':
        	motionProxy.rest()
    	    elif key == 'f':
        	motionProxy.wakeUp()
	    elif key == 's':
        	Strick()
    	    elif key == 'v':
        	postureProxy.goToPosture("StandInit", 1.0)
	    elif key == 'd':
        	thread.start_new_thread(LEDDisco,())
    	    elif key == 's':
        	sd.Play()
	    elif key == 'n':
        	NameChild = raw_input("\rName: ")
	    elif key == 'i':
        	SayInput = raw_input("\rTTS Input: ")
	    elif key == 'l':
        	print postureProxy.getPostureList()
	    elif key == 'p':
		Posture = raw_input("\rSet Posture: ")

if __name__ == '__main__':
    try:
        # Controle
        controle = controle('Thread Controle')
        controle.start()
	threading.Thread(target = KeyRead).start()
        print "Welcome to NAO joystick control!"
        #cp.Init()
        
    except (KeyboardInterrupt, SystemExit):
        #cleanup_stop_thread();
        sys.exit(cp.Close())

