#!/usr/bin/env python

class VelocityManage:
    def __init__(self, vmin = -500, vmax = 500, vmed = 0, rmin = -400, rmax = 400, rmed = 0):
        self.vMin = vmin
        self.vMax = vmax
        self.vMed = vmed
        self.rMin = rmin
        self.rMax = rmax
        self.rMed = rmed
        self.v = 0
        self.r = 0

    def _CheckRange(self):
        if self.v > self.vMax:
            self.v = self.vMax
        if self.r > self.rMax:
            self.r = self.rMax
        if self.v < self.vMin:
            self.v = self.vMin
        if self.r < self.rMin:
            self.r = self.rMin

    def AddSpeed(self, cmd, step = 40):
        if cmd == 0:
            self.r = self.r + step
        elif cmd == 1:
            self.r = self.r - step
        elif cmd == 2:
            self.v = self.v + step
        elif cmd == 3:
            self.v = self.v - step
        self._CheckRange()

    def ReduceSpeed(self, vspeed = 100, rspeed = 100):
        if self.v > self.vMed:
            self.v = self.v - vspeed
            if self.v < self.vMed:
                self.v = self.vMed
        else:
            self.v = self.v + vspeed
            if self.v > self.vMed:
                self.v = self.vMed
        if self.r > self.rMed:
            self.r = self.r - rspeed
            if self.r < self.rMed:
                self.r = self.rMed
        else:
            self.r = self.r + rspeed
            if self.r > self.rMed:
                self.r = self.rMed

    def ResetDirection(self):
        self.r = self.rMed

