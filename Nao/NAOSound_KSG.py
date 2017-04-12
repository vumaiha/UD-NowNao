import time
import sys
import random
import thread
ROBOT_IP = "192.168.1.140"
PORT = 9559

from naoqi import ALProxy
IP=ROBOT_IP
PORT= 9559

#print aup.getVolume()
#print aup.getMasterVolume()

aup=ALProxy("ALAudioPlayer",IP,PORT)

class NAOSound:

    def __init__(self):
        pass

    def Play(self):
        thread.start_new_thread(sound,())

def sound():
        #s=random.randint(2,5)
        #muz="/home/nao/naoqi/wav/%s.wav" % str(s)
	muz="/home/nao/naoqi/wav/7.wav"
	print "\rPlaying " + muz
        playF=aup.playFile(muz,.4,0.0) #(file,vol,pan)
	

