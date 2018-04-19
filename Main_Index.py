import threading
import gui.Interfaz as interface
import gui.PiperScaleWin as PiperScaleWin

import lib.manager as manager
from PyQt4 import QtCore, QtGui
import time
import sys


class CancerInterface(object):
    def __init__(self, settings = {
                                    'UseSensors': True,
                                    #'UseRobot'  : False,
                                    #'RobotIp'   : "192.168.0.100",
                                    #'RobotPort' : 9559
                                  }
                                    ):
        self.therapy_win=interface.MainWin()
        self.Piper_win=PiperScaleWin.PiperScale_Win1()

        self.SensorUpdateThread = SensorUpdateThread(f = self.sensor_update, sample = 1)


        self.Manager=manager.Manager()

        if self.settings['UseSensors']:

            self.Manager.set_sensors(ecg = False, kinect = True)
            self.KinectCaptureThread = KinectCaptureThread(interface=self)

        self.ON = True

        self.therapy_win.connectStartButton(self.on_start_clicked)
        self.therapy_win.connectStopButton(self.on_stop_clicked)
        self.therapy_win.show()

    def on_start_clicked(self):
        print('started from index')
        self.SensorUpdateThread.start()
        if self.settings['UseSensors']:
            print('sensors')
            self.KinectCaptureThread.start()
            #self.EcgCaptureThread.start()
            
    def on_stop_clicked(self):
        self.shutdown()
        print('stopped from index')
        if self.settings['UseSensors']:
            print('sensors')
            self.ManagerRx.shutdown()

    def kinect_handler(self, data):
        print('Getting kinect data ')

    def sensor_update(self):

        if self.settings['UseSensors']:
            #self.ManagerRx  .update_data()
            self.data = self.Manager.get_data()
            print(self.data)
            self.therapy_win.update_display_data(d = {
                                                        #'hr' : self.data['ecg']['hr'],
                                                        'left' : self.data['kinect']['left'],
                                                        'right' : self.data['kinect']['right']
                                                
                                                      }
                                    )
            self.therapy_win.onSensorUpdate.emit()

    def shutdown(self):
        
        self.SensorUpdateThread.shutdown()
        if self.settings['UseSensors']:
            
            #sensor update processes
            self.KinectCaptureThread.shutdown()
            #self.EcgCaptureThread.shutdown()


class KinectCaptureThread(QtCore.QThread):
    def __init__(self, parent = None, sample = 1, interface = None):
        super(KinectCaptureThread,self).__init__()
        self.on = False 
        self.interface = interface



    def shutdown(self):
        self.on = False 
        self.interface.Manager.shutdown()

class SensorUpdateThread(QtCore.QThread):

     def __init__(self, parent = None, f = None, sample = 1):
        super(SensorUpdateThread,self).__init__()
        self.f = f
        self.Ts = sample
        self.ON = True
        
     def run(self):

        if self.f:
            while self.ON:
                self.f()
                time.sleep(self.Ts)

     def shutdown(self):
        self.ON = False

    

    
        

    

    
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    a =CancertInterface()
    sys.exit(app.exec_())            
            

        

        
        

    
