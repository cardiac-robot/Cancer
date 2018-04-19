import os
import time
import threading

import Prueba_pygame as KINECT

class Sensor_Manager(object):

    def __init__(self):

        self.KINECT_ON = False
        self.data={
                    'kinect':{'right':0,'left':0 }
                   }
    
    def set_sensors(self, kinect = True):
        self.KINECT_ON = kinect
        #if self.KINECT_ON:
        #    self.kinect = KINECT.BodyGameRuntime()

    def launch_sensors(self):
        if self.KINECT_ON:
            self.kinect_thread = KINECT.KinectThread()
            self.kinect_thread.start()
            

    def update_data(self):
        if self.KINECT_ON:
            data = self.kinect_thread.kinect.data   
            if not data:
                data={'right':0,'left':0}
        else:
            data={'right':0,'left':0}

        print(data)
        #self.data = {'kinect':0}
        
        
    
    


A = Sensor_Manager()
A.set_sensors()
A.launch_sensors()
time.sleep(4)
while True:
    time.sleep(1)
    A.update_data()

