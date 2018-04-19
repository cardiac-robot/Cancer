# -*- coding: utf-8 -*-import sys
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import*
from PyQt4.QtGui import*
import ctypes

class MainWin(QtGui.QMainWindow):
    onData=QtCore.pyqtSignal()
    onJoy=QtCore.pyqtSignal()
    onStart = QtCore.pyqtSignal()
    onStop = QtCore.pyqtSignal()
    onBorg = QtCore.pyqtSignal()
    onSensorUpdate = QtCore.pyqtSignal()   


    def __init__(self):
        super(MainWin,self).__init__()
        self.init_ui()
        self.dataToDisplay={'left_angle':0,
                            'right_angle':0,

                            }
        

        
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
        self.resize(self.winsize_h*1.5,self.winsize_v*1.5)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #----------------------------------
        #-----------Buttons config----------
        #setting heart rate image
        self.start=QtGui.QLabel(self)
        self.start.setGeometry(QtCore.QRect(self.winsize_h*0.10,self.winsize_v*0.15,self.winsize_h*0.055 ,self.winsize_h*0.055))
        Icon3=QtGui.QPixmap("img/heart-rate")
        Icon_resize3= Icon3.scaled(self.winsize_h*0.055 ,self.winsize_h*0.055,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.start.setPixmap(Icon_resize3)
        
        #setting elbow angles image
        self.stop=QtGui.QLabel(self)
        self.stop.setGeometry(QtCore.QRect(self.winsize_h*0.10,self.winsize_v*0.30,self.winsize_h*0.05,self.winsize_h*0.05))
        Icon4=QtGui.QPixmap("img/elbow")
        Icon_resize5= Icon4.scaled(self.winsize_h*0.05 ,self.winsize_h*0.05,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.stop.setPixmap(Icon_resize5)

        #setting background start image
        self.stop=QtGui.QLabel(self)
        self.stop.setGeometry(QtCore.QRect(self.winsize_h*0.87,self.winsize_v*0.40,self.winsize_h*0.05 ,self.winsize_h*0.05))
        Icon4=QtGui.QPixmap("img/play3")
        Icon_resize5= Icon4.scaled(self.winsize_h*0.05 ,self.winsize_h*0.05, QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.stop.setPixmap(Icon_resize5)

        #setting background stop image
        self.stop=QtGui.QLabel(self)
        self.stop.setGeometry(QtCore.QRect(self.winsize_h*0.87,self.winsize_v*0.60,self.winsize_h*0.05 ,self.winsize_h*0.05))
        Icon4=QtGui.QPixmap("img/stop1")
        Icon_resize5= Icon4.scaled(self.winsize_h*0.05 ,self.winsize_h*0.05, QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.stop.setPixmap(Icon_resize5)

        #setting borg scale image
        self.stop=QtGui.QLabel(self)
        self.stop.setGeometry(QtCore.QRect(self.winsize_h*0.10,self.winsize_v*0.48,self.winsize_h*0.05 ,self.winsize_h*0.05))
        Icon4=QtGui.QPixmap("img/borgsc")
        Icon_resize5= Icon4.scaled(self.winsize_h*0.05 ,self.winsize_h*0.05, QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.stop.setPixmap(Icon_resize5)
        
        #setting background close image
        self.stop=QtGui.QLabel(self)
        self.stop.setGeometry(QtCore.QRect(self.winsize_h*0.943,self.winsize_v*0.02,self.winsize_h*0.038 ,self.winsize_h*0.038))
        Icon4=QtGui.QPixmap("img/closebtn.png")
        Icon_resize5= Icon4.scaled(self.winsize_h*0.038 ,self.winsize_h*0.038,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.stop.setPixmap(Icon_resize5)

        #Heart rate:
        self.hrDisplay = {}
        
        #heart rate label
        self.hrDisplay['name'] = QtGui.QLabel(self)
        self.hrDisplay['name'].setText("Heart Rate")
        self.hrDisplay['name'].setStyleSheet("font-size:18px; Arial")
        self.hrDisplay['name'].setGeometry(QtCore.QRect(self.winsize_h*0.1,self.winsize_v*0.05,self.winsize_h*0.12 ,self.winsize_h*0.1))
        
        self.hrDisplay['lcd'] = QtGui.QLCDNumber(self)
        self.hrDisplay['lcd'].setGeometry(QtCore.QRect(self.winsize_h*0.165,self.winsize_v*0.16,self.winsize_h*0.12 ,self.winsize_h*0.04))

        #Right elbow angles:
        self.elbowDisplay = {}

        self.elbowDisplay['name'] = QtGui.QLabel(self)
        self.elbowDisplay['name'].setText("Elbow Angles")
        self.elbowDisplay['name'].setStyleSheet("font-size:18px; Arial")
        self.elbowDisplay['name'].setGeometry(QtCore.QRect(self.winsize_h*0.09,self.winsize_v*0.2,self.winsize_h*0.12 ,self.winsize_h*0.1))

        self.elbowDisplay['name1'] = QtGui.QLabel(self)
        self.elbowDisplay['name1'].setText("Right")
        self.elbowDisplay['name1'].setStyleSheet("font-size:18px; Arial")
        self.elbowDisplay['name1'].setGeometry(QtCore.QRect(self.winsize_h*0.20,self.winsize_v*0.2,self.winsize_h*0.12 ,self.winsize_h*0.1))

        self.elbowDisplay['lcd'] = QtGui.QLCDNumber(self)
        self.elbowDisplay['lcd'].setGeometry(QtCore.QRect(self.winsize_h*0.18,self.winsize_v*0.31,self.winsize_h*0.08 ,self.winsize_h*0.04))
     

        #Left elbow angles:
        self.LelbowDisplay = {}

        self.LelbowDisplay['name'] = QtGui.QLabel(self)
        self.LelbowDisplay['name'].setText("Left")
        self.LelbowDisplay['name'].setStyleSheet("font-size:18px; Arial")
        self.LelbowDisplay['name'].setGeometry(QtCore.QRect(self.winsize_h*0.29,self.winsize_v*0.2,self.winsize_h*0.12 ,self.winsize_h*0.1))

        self.LelbowDisplay['lcd'] = QtGui.QLCDNumber(self)
        self.LelbowDisplay['lcd'].setGeometry(QtCore.QRect(self.winsize_h*0.27,self.winsize_v*0.31,self.winsize_h*0.08 ,self.winsize_h*0.04))

        #Borg Scale state:
        self.BorgDisplay = {}

        self.BorgDisplay['name'] = QtGui.QLabel(self)
        self.BorgDisplay['name'].setText("Borg Scale Status")
        self.BorgDisplay['name'].setStyleSheet("font-size:18px; Arial")
        self.BorgDisplay['name'].setGeometry(QtCore.QRect(self.winsize_h*0.08,self.winsize_v*0.32,self.winsize_h*0.13 ,self.winsize_h*0.15))

        self.BorgDisplay['lcd'] = QtGui.QLCDNumber(self)
        self.BorgDisplay['lcd'].setGeometry(QtCore.QRect(self.winsize_h*0.20,self.winsize_v*0.49,self.winsize_h*0.08 ,self.winsize_h*0.04))



    
        self.controlButtons = {}
        #start button
        self.controlButtons['start'] =QtGui.QCommandLinkButton(self)
        self.controlButtons['start'].setGeometry(QtCore.QRect(self.winsize_h*0.87,self.winsize_v*0.40,self.winsize_h*0.05 ,self.winsize_h*0.05))
        self.controlButtons['start'].setIconSize(QSize(0,0))

        self.controlButtons['stop'] =QtGui.QCommandLinkButton(self)
        self.controlButtons['stop'].setGeometry(QtCore.QRect(self.winsize_h*0.87,self.winsize_v*0.60,self.winsize_h*0.05 ,self.winsize_h*0.05))
        self.controlButtons['stop'].setIconSize(QSize(0,0))
        
        #Close button
        self.controlButtons['close'] = QtGui.QCommandLinkButton(self)
        self.controlButtons['close'].setGeometry(QtCore.QRect(self.winsize_h*0.943,self.winsize_v*0.02,self.winsize_h*0.038 ,self.winsize_h*0.038))
        self.controlButtons['close'].setIconSize(QSize(0,0))

        #Create Borg button
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
        
        self.controlButtons['start'].clicked.connect(self.onStartClicked)
        self.controlButtons['stop'].clicked.connect(self.onStopClicked)
        self.controlButtons['close'].clicked.connect(self.hide)
        self.onData.connect(self.display_data)

    def onStartClicked(self):
        #function to modify the interface state and visuals
        self.onStart.emit()
        print('start clicked')
        #lock start button
        self.controlButtons['start'].setEnabled(False)
        self.controlButtons['stop'].setEnabled(True)
        self.update_display_data(d = {
                                        'hr' : 1,
                                        'yaw_t' : 2,
                                        'pitch_t' : 3,
                                        'roll_t' : 4,
                                        'yaw_c' : 5,
                                        'pitch_c' : 6,
                                        'roll_c' : 7
                                        }
                                )
    def display_data(self):

        self.hrDisplay['lcd'].display(self.dataToDisplay['hr'])
        self.LelbowDisplay['lcd'].display(self.dataToDisplay['Lelbow'])
        self.elbowDisplay.display(self.dataToDisplay['elbow'])
        
    def update_display_data(self,
                            d = {
                                'hr' : 0,
                                'yaw_t' : 0,
                                'pitch_t' : 0,
                                'roll_t' : 0,
                                'yaw_c' : 0,
                                'pitch_c:' : 0,
                                'roll_c' : 0,
                                'borg' : 0
                                }
                            ):
        self.dataToDisplay =  d
        self.onData.emit()
    def onStopClicked(self):
        self.onStop.emit()
        #function to modify the interface state and visuals
        self.controlButtons['start'].setEnabled(True)
        self.controlButtons['stop'].setEnabled(False)
        print('stop clicked')
        self.update_display_data(d = {
                                        'hr' : 0,
                                        'yaw_t' : 0,
                                        'pitch_t' : 0,
                                        'roll_t' : 0,
                                        'yaw_c' : 0,
                                        'pitch_c' : 0,
                                        'roll_c' : 0,
                                        'borg': 0
                                        }
                                        )
    
class BorgButton(object):
    def __init__(self, window):
        self.window = window
        self.cursorStatus = 0
        self.j = None
        #setting background Label Borgº
        self.Labelborg=QtGui.QLabel(self.window)
        self.Labelborg.setGeometry(QtCore.QRect(self.window.winsize_h*0.05,self.window.winsize_v*0.70,self.window.winsize_h*0.8 ,self.window.winsize_h*0.1))
        Icon2=QtGui.QPixmap("img/borgh")
        Icon_resize= Icon2.scaled(self.window.winsize_h*0.8 ,self.window.winsize_h*0.1,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.Labelborg.setPixmap(Icon_resize)
        self.Labelborg.setScaledContents(True)

        #get borg scale buttons
        self.create_borg_button()

    def create_borg_button(self):
        self.Borg = []
        self.BorgButton= []
        offset = 1
        ep = self.window.winsize_h*0.052
        xp = self.window.winsize_h*0.054
        yp = self.window.winsize_v*0.74
        hp = self.window.winsize_h*0.05
        wp = self.window.winsize_h*0.05
        x = xp
        e = ep
        y = yp
        h = hp
        w = wp
        for i in range(15):
            self.Borg.append(QtGui.QLabel(self.window))
            self.BorgButton.append(QtGui.QCommandLinkButton(self.window))
            Icon2=QtGui.QPixmap("img/l" + str(i))
            Icon_resize= Icon2.scaled(h,w,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
            self.Borg[-1].setPixmap(Icon_resize)
            self.Borg[-1].setGeometry(x,y,h,w)
            self.BorgButton[-1].setGeometry(QtCore.QRect(x,y,h,w))
            self.BorgButton[-1].setIconSize(QSize(0,0))
    
            x = x + e
        
        

def main():
    app=QtGui.QApplication(sys.argv)
    GUI=MainWin()
    sys.exit(app.exec_())
A=main()

if __name__ == '__main__':
    app=QtGui.QApplication(sys.argv)
    GUI=MainWin()
    sys.exit(app.exec_())
