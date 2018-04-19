import Prueba_pygame as KINECT
import ecg_sensor as ECG
import time
import threading


class SensorManager(object):
    def __init__(self, settings = {"UseKinect":True,
                                   "UseEcg":True}):

        self.KINECT_ON = settings["UseKinect"]
        self.ECG_ON = settings["UseEcg"]

    def set_sensors(self):
        if self.KINECT_ON:
            print("set kinect")
            self.kinect = KINECT.KinectProcess()
        if self.ECG_ON:
            print("set ecg")
            self.ecg = ECG.EcgSensor(
                                        port = 'COM6',
					sample = 1

                                      )
    def play_sensors(self):
        
        if self.ECG_ON:
            self.ecg.play()
        
    def launch_sensors(self):
        if self.KINECT_ON:
            self.kinect.launch_process()
        if self.ECG_ON:
            self.ecg.start()
            threading.Thread(target = self.ecg.process).start()
            print("launch ecg")

    def get_data(self):
        kinect = None
        ecg = None
    
        if self.KINECT_ON:
            kinect=self.kinect.get_data()
        if self.ECG_ON:
            ecg = self.ecg.get_data()

        data = {'ecg': ecg, 'kinect': kinect}
        return(data)

    def shutdown(self):
        if self.KINECT_ON:
            self.kinect.shutdown()

        if self.ECG_ON:
            self.ecg.shutdown()
            print("ecg shutdown")

    




if __name__== "__main__":
    sm = SensorManager()
    sm.set_sensors()
    sm.launch_sensors()
    sm.play_sensors()

    for i in range(30):
        m=sm.get_data()
        print(m)
        time.sleep(0.5)

    sm.shutdown()
    time.sleep(3)
    print("going out from manager")

    """
    a=KINECT.KinectProcess()
    a.launch_process()

    for i in range(20):
        time.sleep(1)

    
    print("closing")
    a.shutdown()
    """
