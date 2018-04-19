# -*- coding: utf-8 -*-import sys
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import*
from PyQt4.QtGui import*
import ctypes

class PiperScale_Win1(QtGui.QMainWindow):

    def __init__(self):
        super(PiperScale_Win1,self).__init__()
        #self.project_Handler=project_Handler
        
        self.init_ui()
        
        ##Signals
        self.set_signals()


    def init_ui(self):
        #-------main config-------
        #Window title
        self.setWindowTitle("Main Menu Window")
        self.setStyleSheet("QMainWindow {background: 'white';}")
        #Window size
        self.user32=ctypes.windll.user32
        self.screensize=self.user32.GetSystemMetrics(0), self.user32.GetSystemMetrics(1),
        #Resizing MainWindoe to a percentage of the total
        self.winsize_h=int(self.screensize[0])
        self.winsize_v=int(self.screensize[1])
        self.resize(self.winsize_h,self.winsize_v)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        #----------------------------------
        #-----------Buttons config----------

        #setting background close image
        self.stop=QtGui.QLabel(self)
        self.stop.setGeometry(QtCore.QRect(self.winsize_h*0.943,self.winsize_v*0.02,self.winsize_h*0.038 ,self.winsize_h*0.038))
        Icon4=QtGui.QPixmap("img1/closebtn.png")
        Icon_resize5= Icon4.scaled(self.winsize_h*0.038 ,self.winsize_h*0.038,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.stop.setPixmap(Icon_resize5)

        #setting q1 image
        self.start=QtGui.QLabel(self)
        self.start.setGeometry(QtCore.QRect(self.winsize_h*0.20,self.winsize_v*0.08,self.winsize_h*0.6 ,self.winsize_h*0.15))
        Icon3=QtGui.QPixmap("img1/preg1")
        Icon_resize3= Icon3.scaled(self.winsize_h*0.6 ,self.winsize_h*0.15,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.start.setPixmap(Icon_resize3)
        self.controlButtons = {}

        #setting q2 image
        self.start=QtGui.QLabel(self)
        self.start.setGeometry(QtCore.QRect(self.winsize_h*0.2,self.winsize_v*0.45,self.winsize_h*0.6 ,self.winsize_h*0.15))
        Icon3=QtGui.QPixmap("img1/preg2")
        Icon_resize3= Icon3.scaled(self.winsize_h*0.6 ,self.winsize_h*0.15,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.start.setPixmap(Icon_resize3)
        self.controlButtons = {}


        #Close button
        self.controlButtons['close'] = QtGui.QCommandLinkButton(self)
        self.controlButtons['close'].setGeometry(QtCore.QRect(self.winsize_h*0.943,self.winsize_v*0.02,self.winsize_h*0.038 ,self.winsize_h*0.038))
        self.controlButtons['close'].setIconSize(QSize(0,0))
        self.Borg = BorgButton(self)

        self.show()

    #------------------------------------SIGNAL METHODS------------------------------------------------------------------------------
    def connectStartButton(self,f):
        self.controlButtons['start'].clicked.connect(f)
    def connectStopButton(self, f):
        self.controlButtons['stop'].clicked.connect(f)
    def connectNewRegisterButton(self, f):
        self.controlButtons['newregister'].clicked.connect(f)

    def connectCloseButton(self):
        self.controlButtons['close'].clicked.connect(self.close)

    def set_signals(self):
        self.connectCloseButton()


#Borg Button object
class BorgButton(object):
    def __init__(self, window):
        self.window = window
        self.cursorStatus = 0
        self.j = None
        #setting background Label Borgº
        self.Labelborg=QtGui.QLabel(self.window)
        self.Labelborg.setGeometry(QtCore.QRect(self.window.winsize_h*0.16,self.window.winsize_v*0.70,self.window.winsize_h*0.67 ,self.window.winsize_h*0.1))
        Icon2=QtGui.QPixmap("img1/piper_back")
        Icon_resize= Icon2.scaled(self.window.winsize_h*0.67,self.window.winsize_h*0.1,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.Labelborg.setPixmap(Icon_resize)
        self.Labelborg.setScaledContents(True)

        #setting background Label Borgº
        self.Labelborg1=QtGui.QLabel(self.window)
        self.Labelborg1.setGeometry(QtCore.QRect(self.window.winsize_h*0.16,self.window.winsize_v*0.30,self.window.winsize_h*0.67 ,self.window.winsize_h*0.1))
        Icon2=QtGui.QPixmap("img1/piper_back")
        Icon_resize= Icon2.scaled(self.window.winsize_h*0.67,self.window.winsize_h*0.1,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.Labelborg1.setPixmap(Icon_resize)
        self.Labelborg1.setScaledContents(True)

        #get borg scale buttons
        self.create_borg_button()
    def create_borg_button(self):
        self.Borg = []
        self.Borg2 = []
        self.BorgButton = []
        self.BorgButton2 = []
        offset = 1
        ep = self.window.winsize_h*0.06
        xp = self.window.winsize_h*0.11
        yp1 = self.window.winsize_h*0.175
        yp = self.window.winsize_v*0.71
        hp = self.window.winsize_h*0.05
        wp = self.window.winsize_h*0.085
        x = xp
        y1 = yp1
        e = ep
        y = yp
        h = hp
        w = wp
        for i in range(15):
            self.Borg.append(QtGui.QLabel(self.window))
            self.BorgButton.append(QtGui.QCommandLinkButton(self.window))
            Icon2=QtGui.QPixmap("img1/l" + str(i))
            Icon_resize= Icon2.scaled(h,w)
            self.Borg[-1].setPixmap(Icon_resize)
            self.Borg[-1].setGeometry(x,y,h,w)
            self.BorgButton[-1].setGeometry(QtCore.QRect(x,y,h,w))
            self.BorgButton[-1].setIconSize(QSize(0,0))
            self.Borg2.append(QtGui.QLabel(self.window))
            self.BorgButton.append(QtGui.QCommandLinkButton(self.window))
            Icon2=QtGui.QPixmap("img1/l" + str(i))
            Icon_resize= Icon2.scaled(h,w)
            self.Borg2[-1].setPixmap(Icon_resize)
            self.Borg2[-1].setGeometry(x,y1,h,w)
            self.BorgButton[-1].setGeometry(QtCore.QRect(x,y1,h,w))
            self.BorgButton[-1].setIconSize(QSize(0,0))
            x = x + e



        

def main():
    app=QtGui.QApplication(sys.argv)
    GUI=PiperScale_Win1()
    sys.exit(app.exec_())
A=main()

if __name__ == '__main__':
    app=QtGui.QApplication(sys.argv)
    GUI=PiperScale_Win1()
    sys.exit(app.exec_())
