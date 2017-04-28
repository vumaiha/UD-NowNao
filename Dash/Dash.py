#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import gobject
gtk.threads_init()

from robot import *
import VelocityManage
import time
import math
import threading
import random

import Queue

c = threading.Condition()
gIsDisco = False
gIsBusy = False


           
sounds= [HI,
           HUH,
           UHOH,
           OKAY,
           SIGH,
           TADA,
           WEE,
           BYE,
           HORSE,
           CAT,
           DOG,
           DINOSAUR,
           LION,
           GOAT,
           CROCODILE,
           ELEPHANT,
           FIRESIREN,
           TRUCKHORN,
           CARENGINE,
           CARTIRESQUEEL,
           HELICOPTER,
           JETPLANE,
           BOAT,
           TRAIN,
           BEEPS,
           LASERS,
           GOBBLE,
           BUZZ,
           AYYAIYAI,
           SQUEEK,
           MYSOUND1,
           MYSOUND2,
           MYSOUND3,
           MYSOUND4,
           MYSOUND5]
           
 
_animalSounds = [HORSE,
				CAT,
				DOG,
				DINOSAUR,
				LION,
				GOAT,
				CROCODILE,
				ELEPHANT
				]

_vehicleSounds = [FIRESIREN,
				TRUCKHORN,
				CARENGINE,
				CARTIRESQUEEL,
				HELICOPTER,
				JETPLANE,
				BOAT,
				TRAIN,
				BEEPS
				]


class DashCommandSender(threading.Thread):
    CONNECTED = 0
    DISCONNECTED = 1
    CONNECTING = 2
    DISCONNECTING = 3

    stopthread = threading.Event()

    def __init__(self):
        threading.Thread.__init__(self)
        self.q = Queue.Queue()
        self.lastSendTime = time.time()

        self.dash = robot("DC:86:F3:1F:C5:E9", False)
        self.connectStatus = DashCommandSender.DISCONNECTED

        self.isDisco = False

    def __del__(self):
        self.stop()

    def clear(self):
        self.q.clear()
        self.lastSendTime = time.time()

    def addCommand(self, cmd):
        self.q.put_nowait(cmd)

    def _commandPhaser(self, cmd):
        if cmd == 'connect':
            self.connectStatus = DashCommandSender.CONNECTING
            if not self.dash.isConnected:
                try:
                    self.dash.connect()
                    self.connectStatus = DashCommandSender.CONNECTED
                except:
                    self.connectStatus = DashCommandSender.DISCONNECTED
        elif cmd == 'disconnect':
            self.connectStatus = DashCommandSender.DISCONNECTING
            if self.dash.isConnected:
                self.dash.disconnect()
                time.sleep(1)
                self.connectStatus = DashCommandSender.DISCONNECTED
        elif cmd == 'sound':
            if self.dash.isConnected:
                self.dash.playSound(_sounds[random.randrange(0,35)])
        elif cmd == 'animalsound':
			if self.dash.isConnected:
				self.dash.playSound(_animalSounds[random.randrange(0,7)])
        elif 'wheel' in cmd:
            if self.dash.isConnected:
                scmd = cmd.split(',')
                v = int(scmd[1])
                r = int(scmd[2])
                if v == 0 and r == 0:
                    self.dash.stopWheels()
                else:
                    print str(v) + ',' + str(r)
                    self.dash.setWheelSpeed(v,r)
        else:
            print 'Unknow command...'

    def killAll(self):
        while not self.q.empty():
            self.q.get_nowait()
        self.dash.stopWheels()

    def run(self):
        global gIsDisco
        global gIsBusy

        red = 16
        green = 71
        blue = 41
        redStep = 10
        greenStep = -20
        blueStep = 15

        step = 45
        pos = 90

        while not self.stopthread.isSet():
            #gtk.threads_enter()
            if (not self.q.empty()):
                self._commandPhaser(self.q.get_nowait())
                self.lastSendTime = time.time()
            #gtk.threads_leave()
            red += redStep
            if (red < 0) | (red > 255):
        	red -= redStep
        	redStep = -redStep
            green += greenStep
            if (green < 0) | (green > 255):
        	green -= greenStep
        	greenStep = -greenStep
            blue += blueStep
            if (blue < 0) | (blue > 255):
        	blue -= blueStep
        	blueStep = -blueStep

            c.acquire()
            gIsBusy = True
            if math.ceil(time.time()*100)%10 == 0 and gIsDisco:
                self.dash.colorAll(red, green, blue, red, green, blue, red, green, blue)
           
            if math.ceil(time.time()*10)%10 == 0 and gIsDisco:
                pos += step
                if (pos < -90) | (pos > 90):
                    pos -= (2* step)
                    step = -step
                    self.dash.moveHeadY(0)
                    self.dash.moveHeadX(pos)
            gIsBusy = False
            c.notify_all()
            c.release()

    def stop(self):
        self.stopthread.set()

class ArrowKey:
    def __init__(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False

class DashApp:
    #Logic
    def run(self):
        if not self._isChecking:
            return True
        if self.cmd.connectStatus == DashCommandSender.CONNECTING:
            self.clEventbox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('blue'))
            self.connectLabel.set_markup("<span font_desc=\"24.0\"> Connecting... </span>")
            self.connectButton.set_sensitive(False)
        elif self.cmd.connectStatus == DashCommandSender.DISCONNECTING:
            self.clEventbox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('blue'))
            self.connectLabel.set_markup("<span font_desc=\"24.0\"> Disconnecting... </span>")
            self.connectButton.set_sensitive(False)
        elif self.cmd.connectStatus == DashCommandSender.CONNECTED:
            self.clEventbox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('green'))
            self.connectLabel.set_markup("<span font_desc=\"24.0\"> Connected </span>")
            self.connectButton.get_children()[0].set_markup("<span font_desc=\"24.0\"> Disconnect </span>")
            self.connectButton.set_sensitive(True)
            self._isChecking = False
        else:
            self.clEventbox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
            self.connectLabel.set_markup("<span font_desc=\"24.0\"> No connection </span>")
            self.connectButton.get_children()[0].set_markup("<span font_desc=\"24.0\"> Connect </span>")
            self.connectButton.set_sensitive(True)
            self._isChecking = False
        return True

    def speedPush(self):
        global gIsBusy
        self.DashVelocity.ReduceSpeed()
        cmdstr = 'wheel,' + str(self.DashVelocity.v) + ',' + str(self.DashVelocity.r)
        #self.cmd.addCommand(cmdstr)
        c.acquire()
        if not gIsBusy: self.cmd._commandPhaser(cmdstr)
        else: c.wait()
        c.release()     
        return True
    
    def keyCheck(self):
        if self.keyState.left:
            self.DashVelocity.AddSpeed(0)
        if self.keyState.right:
            self.DashVelocity.AddSpeed(1)
        if self.keyState.up:
            self.DashVelocity.AddSpeed(2)
        if self.keyState.down:
            self.DashVelocity.AddSpeed(3)
        return True
    #Logic End

    #Events
    def onConnect(self, widget, data=None):
        if self.cmd.connectStatus == DashCommandSender.CONNECTED:
            self.cmd.addCommand('disconnect')
        elif self.cmd.connectStatus == DashCommandSender.DISCONNECTED:
            self.cmd.addCommand('connect')
        self._isChecking = True

    def onPressKey(self, widget, event):
        global gIsDisco
        global gIsBusy
        if self._isPhraseKey:
            if event.keyval == gtk.keysyms.Left:
                self.keyState.left = True
                return True
            elif event.keyval == gtk.keysyms.Right:
                self.keyState.right = True
                return True
            elif event.keyval == gtk.keysyms.Up:
                self.keyState.up = True
                return True
            elif event.keyval == gtk.keysyms.Down:
                self.keyState.down = True
                return True
            elif event.keyval == 32:#space
                self.cmd.killAll()
                return True
            elif event.keyval == 97:#pressing 'a' plays a random animal sound
                c.acquire()
                if not gIsBusy: self.cmd.addCommand('animalsound')
                else: c.wait()
                c.release()
                return True
            elif event.keyval == 100:#pressing 'd' makes Dash light up and turn its head
                gIsDisco = not gIsDisco
                return True
            elif event.keyval == 102:#pressing 'f' plays a random sound
                c.acquire()
                if not gIsBusy: self.cmd.addCommand('sound')
                else: c.wait()
                c.release()
                return True
            else: 
                return False
        else:
            return False

    def onReleaseKey(self, widget, event):
        if self._isPhraseKey:
            if event.keyval == gtk.keysyms.Left:
                self.keyState.left = False
                self.DashVelocity.ResetDirection()
                return True
            elif event.keyval == gtk.keysyms.Right:
                self.keyState.right = False
                self.DashVelocity.ResetDirection()
                return True
            elif event.keyval == gtk.keysyms.Up:
                self.keyState.up = False
                return True
            elif event.keyval == gtk.keysyms.Down:
                self.keyState.down = False
                return True
            else: 
                return False
        else:
            return False

    def destroy(self, widget, data=None):
        self.cmd.stop()
        gtk.main_quit()
    #Events End

    def __init__(self):
        rcfile = '/usr/share/themes/Xfce-smooth/gtk-2.0/gtkrc'
        gtk.rc_parse(rcfile)

        self._isChecking = False
        self._isPhraseKey = True#False
        self.DashVelocity = VelocityManage.VelocityManage()
        self.keyState = ArrowKey()

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)
        self.window.set_title('Dash Control')
        self.window.set_default_size(1600, 940)
        self.window.add_events(gtk.gdk.KEY_PRESS_MASK)
        self.window.connect('key-press-event', self.onPressKey)
        self.window.connect('key-release-event', self.onReleaseKey)

        #Core
        self.cmd = DashCommandSender()
        #Core End

        #Panel Layout 
        mainPanel = gtk.VBox(False, 10)
        firstRow = gtk.HBox(False, 10)
        secondRow = gtk.HBox(False, 10)
        thirdRow = gtk.HBox(False, 10)
        self.window.add(mainPanel)
        #Panel Layout End

        #First Row
        self.clEventbox = gtk.EventBox()
        self.connectLabel = gtk.Label(' No connection ')
        self.clEventbox.add(self.connectLabel)
        self.clEventbox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
        self.connectLabel.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
        self.connectLabel.set_justify(gtk.JUSTIFY_CENTER)
        self.connectLabel.set_markup("<span font_desc=\"24.0\">No connection</span>");
        firstRow.pack_start(self.clEventbox, False, True)
        self.connectButton = gtk.Button(' Connect ')  
        self.connectButton.get_children()[0].set_markup("<span font_desc=\"24.0\"> Connect </span>")
        self.connectButton.connect('clicked', self.onConnect, None)
        firstRow.pack_start(self.connectButton, True, True)
        #First Row End

        #Second Row
        self.speedAdj = gtk.Adjustment(0,0,400,1,100,4)
        self.speedScale = gtk.HScale(self.speedAdj)
        secondRow.pack_start(self.speedScale, True, True)
        #Second Row End

        #Third Row
        self.goButton = gtk.ToggleButton(label='Go', use_underline=True)
        self.goButton.get_children()[0].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
        self.goButton.get_children()[0].modify_fg(gtk.STATE_ACTIVE, gtk.gdk.color_parse('white'))
        self.goButton.get_children()[0].modify_fg(gtk.STATE_PRELIGHT, gtk.gdk.color_parse('white'))
        self.goButton.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#0080FF'))
        self.goButton.modify_bg(gtk.STATE_ACTIVE, gtk.gdk.color_parse('#FF8000'))
        self.goButton.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.color_parse('#FF8000'))
        self.goButton.get_children()[0].set_markup("<span font_desc=\"24.0\"> Go </span>")
        thirdRow.pack_start(self.goButton, True, True)
        #Third Row End

        #Pack Panel
        mainPanel.pack_start(firstRow, False, False)
        mainPanel.pack_start(secondRow, False, False)
        mainPanel.pack_start(thirdRow, False, False)
        #Pack Panel End

        #Show All
        self.connectButton.show()
        self.connectLabel.show()
        self.clEventbox.show()
        self.goButton.show()
        self.speedScale.show()
        firstRow.show() 
        secondRow.show()
        thirdRow.show()
        mainPanel.show()
        self.window.show()
        #Show All End

    def main(self):
        #Post Call
        gobject.timeout_add(100, self.run)
        gobject.timeout_add(200, self.speedPush)
        gobject.timeout_add(10, self.keyCheck)
        self.cmd.start() 
        #Post Call End
        gtk.main()

if __name__ == "__main__":
    dashApp = DashApp()
    dashApp.main()

