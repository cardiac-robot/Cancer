from __future__ import division
from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

import ctypes
import _ctypes
import pygame
import sys

import ctypes
import _ctypes
import pygame
import sys
import numpy as np
import math
import threading
import multiprocessing
import matplotlib
import time 

if sys.hexversion >= 0x03000000:
    import _thread as thread
else:
    import thread

# colors for drawing different bodies 
SKELETON_COLORS = [pygame.color.THECOLORS["red"], 
                  pygame.color.THECOLORS["blue"], 
                  pygame.color.THECOLORS["green"], 
                  pygame.color.THECOLORS["orange"], 
                  pygame.color.THECOLORS["purple"], 
                  pygame.color.THECOLORS["yellow"], 
                  pygame.color.THECOLORS["violet"]]


class BodyGameRuntime(object):
    def __init__(self):
        pygame.init()

        self.first_user = None
        self.data = None
        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Set the width and height of the screen [width, height]
        self._infoObject = pygame.display.Info()
        self._screen = pygame.display.set_mode((self._infoObject.current_w >> 1, self._infoObject.current_h >> 1), 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)

        pygame.display.set_caption("Kinect for Windows v2 Body Game")

        # Loop until the user clicks the close button.
        #self._done = False

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Kinect runtime object, we want only color and body frames 
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)

        # back buffer surface for getting Kinect color frames, 32bit color, width and height equal to the Kinect color frame size
        self._frame_surface = pygame.Surface((self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height), 0, 32)

        # here we will store skeleton data 
        self._bodies = None

        self.estado = None

        self._done= False

        self.length_step = []


    def draw_body_bone(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if (joint0State == PyKinectV2.TrackingState_NotTracked) or (joint1State == PyKinectV2.TrackingState_NotTracked): 
            return

        # both joints are not *really* tracked
        if (joint0State == PyKinectV2.TrackingState_Inferred) and (joint1State == PyKinectV2.TrackingState_Inferred):
            return

        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)

        try:
            pygame.draw.line(self._frame_surface, color, start, end, 8)
        except: # need to catch it due to possible invalid positions (with inf)
            pass

    def draw_body(self, joints, jointPoints, color):
        # Torso
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Head, PyKinectV2.JointType_Neck);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Neck, PyKinectV2.JointType_SpineShoulder);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_SpineMid);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineMid, PyKinectV2.JointType_SpineBase);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipLeft);
    
        # Right Arm    
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderRight, PyKinectV2.JointType_ElbowRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowRight, PyKinectV2.JointType_WristRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_HandRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandRight, PyKinectV2.JointType_HandTipRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_ThumbRight);

        # Left Arm
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_ElbowLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowLeft, PyKinectV2.JointType_WristLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_HandLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandLeft, PyKinectV2.JointType_HandTipLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_ThumbLeft);

        # Right Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipRight, PyKinectV2.JointType_KneeRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeRight, PyKinectV2.JointType_AnkleRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleRight, PyKinectV2.JointType_FootRight);

        # Left Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_KneeLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeLeft, PyKinectV2.JointType_AnkleLeft);
        
    def draw_color_frame(self, frame, target_surface):
        target_surface.lock()
        address = self._kinect.surface_as_array(target_surface.get_buffer())
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        del address
        target_surface.unlock()

    def process(self, req = None, cad = None, end = None, getPipe = None, loadPipe = None, loadCad = None):
        # -------- Main Program Loop -----------
        
        while not end.is_set():
            # --- Main event loop
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self._done = True # Flag that we are done so we exit this loop

                elif event.type == pygame.VIDEORESIZE: # window resized
                    self._screen = pygame.display.set_mode(event.dict['size'], 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)
                    
            # --- Game logic should go here

            # --- Getting frames and drawing  
            # --- Woohoo! We've got a color frame! Let's fill out back buffer surface with frame's data 
            if self._kinect.has_new_color_frame():
                frame = self._kinect.get_last_color_frame()
                self.draw_color_frame(frame, self._frame_surface)
                frame = None

            # --- Cool! We have a body frame, so can get skeletons
            if self._kinect.has_new_body_frame(): 
                self._bodies = self._kinect.get_last_body_frame()

            # --- draw skeletons to _frame_surface
            if self._bodies is not None:
                if self.first_user == None:
                    
                    for x in range(0,self._kinect.max_body_count):
                        if self._bodies.bodies[x].is_tracked:
                            self.first_user = x
                            break
                        
                else:
                    if self._bodies.bodies[self.first_user].is_tracked:
                        body = self._bodies.bodies[self.first_user]
                        self.joints = body.joints
                        ang=self.Flexo_ExtentionAngles_UpperLimb()
                        cadence=self.Cadencia(cad, loadCad)
                        self.data = ang
                        #if data requested
                        if req.is_set():
                            print("data requested: " + str(self.data))
                            loadPipe.send(self.data)

                            
                        #print(self.data)
                        #time.sleep(self.sample_time)
                        #self.data.update(self.para_cin)
                        joint_points = self._kinect.body_joints_to_color_space(self.joints)
                        self.draw_body(self.joints, joint_points, SKELETON_COLORS[self.first_user])
                        #print(self.data)

                    else:
                        self.first_user = None
                        self.data = None

            # --- copy back buffer surface pixels to the screen, resize it if needed and keep aspect ratio
            # --- (screen size may be different from Kinect's color frame size) 
            h_to_w = float(self._frame_surface.get_height()) / self._frame_surface.get_width()
            target_height = int(h_to_w * self._screen.get_width())
            surface_to_draw = pygame.transform.scale(self._frame_surface, (self._screen.get_width(), target_height));
            self._screen.blit(surface_to_draw, (0,0))
            surface_to_draw = None
            pygame.display.update()

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            self._clock.tick(60)

        # Close our Kinect sensor, close the window and quit.
        self._kinect.close()
        pygame.quit()


    def JointPoints_UpperLimb(self):

        self.P_RWrist = [self.joints[PyKinectV2.JointType_WristRight].Position.x,self.joints[PyKinectV2.JointType_WristRight].Position.y,self.joints[PyKinectV2.JointType_WristRight].Position.z]
        self.P_RElbow = [self.joints[PyKinectV2.JointType_ElbowRight].Position.x,self.joints[PyKinectV2.JointType_ElbowRight].Position.y,self.joints[PyKinectV2.JointType_ElbowRight].Position.z]
        self.P_RShoulder  = [self.joints[PyKinectV2.JointType_ShoulderRight].Position.x,self.joints[PyKinectV2.JointType_ShoulderRight].Position.y,self.joints[PyKinectV2.JointType_ShoulderRight].Position.z]
        self.P_RHand = [self.joints[PyKinectV2.JointType_HandRight].Position.x,self.joints[PyKinectV2.JointType_HandRight].Position.y,self.joints[PyKinectV2.JointType_HandRight].Position.z]
        self.P_RThumb = [self.joints[PyKinectV2.JointType_ThumbRight].Position.x,self.joints[PyKinectV2.JointType_ThumbRight].Position.y,self.joints[PyKinectV2.JointType_ThumbRight].Position.z]
        self.P_RHandTip = [self.joints[PyKinectV2.JointType_HandTipRight].Position.x,self.joints[PyKinectV2.JointType_HandTipRight].Position.y,self.joints[PyKinectV2.JointType_HandTipRight].Position.z]
        
        self.P_LWrist = [self.joints[PyKinectV2.JointType_WristLeft].Position.x,self.joints[PyKinectV2.JointType_WristLeft].Position.y,self.joints[PyKinectV2.JointType_WristLeft].Position.z]
        self.P_LElbow = [self.joints[PyKinectV2.JointType_ElbowLeft].Position.x,self.joints[PyKinectV2.JointType_ElbowLeft].Position.y,self.joints[PyKinectV2.JointType_ElbowLeft].Position.z]
        self.P_LShoulder  = [self.joints[PyKinectV2.JointType_ShoulderLeft].Position.x,self.joints[PyKinectV2.JointType_ShoulderLeft].Position.y,self.joints[PyKinectV2.JointType_ShoulderLeft].Position.z]
        self.P_LHand = [self.joints[PyKinectV2.JointType_HandLeft].Position.x,self.joints[PyKinectV2.JointType_HandLeft].Position.y,self.joints[PyKinectV2.JointType_HandLeft].Position.z]
        self.P_LThumb = [self.joints[PyKinectV2.JointType_ThumbLeft].Position.x,self.joints[PyKinectV2.JointType_ThumbLeft].Position.y,self.joints[PyKinectV2.JointType_ThumbLeft].Position.z]
        self.P_LHandTip = [self.joints[PyKinectV2.JointType_HandTipLeft].Position.x,self.joints[PyKinectV2.JointType_HandTipLeft].Position.y,self.joints[PyKinectV2.JointType_HandTipLeft].Position.z]

        self.P_RAnkle  = [self.joints[PyKinectV2.JointType_AnkleRight].Position.x,self.joints[PyKinectV2.JointType_AnkleRight].Position.y,self.joints[PyKinectV2.JointType_AnkleRight].Position.z]
        self.P_LAnkle  = [self.joints[PyKinectV2.JointType_AnkleLeft].Position.x,self.joints[PyKinectV2.JointType_AnkleLeft].Position.y,self.joints[PyKinectV2.JointType_AnkleLeft].Position.z]

        self.P_SpineMid  = [self.joints[PyKinectV2.JointType_SpineMid].Position.x,self.joints[PyKinectV2.JointType_SpineMid].Position.y,self.joints[PyKinectV2.JointType_SpineMid].Position.z]
        self.P_SpineBase  = [self.joints[PyKinectV2.JointType_SpineBase].Position.x,self.joints[PyKinectV2.JointType_SpineBase].Position.y,self.joints[PyKinectV2.JointType_SpineBase].Position.z]
        self.P_LHip = [self.joints[PyKinectV2.JointType_HipLeft].Position.x,self.joints[PyKinectV2.JointType_HipLeft].Position.y,self.joints[PyKinectV2.JointType_HipLeft].Position.z]
 

    def Flexo_ExtentionAngles_UpperLimb(self):
        
        Elbow_Angles  = {}
        self.JointPoints_UpperLimb()
        self.Flex_Ex_LElbow=Ang_4_puntos(self.P_LWrist,self.P_LElbow,self.P_LElbow,self.P_LShoulder)
        self.Flex_Ex_RElbow=Ang_4_puntos(self.P_RWrist,self.P_RElbow,self.P_RElbow,self.P_RShoulder)
        Elbow_Angles['Left'] = self.Flex_Ex_LElbow
        Elbow_Angles['Right'] = self.Flex_Ex_RElbow
        return(Elbow_Angles)

    def Conteo_FlexExT(self):

        #Arreglaaaaar esto
        if self.Flex_Ex_RElbow>89.5 and self.Flex_Ex_RElbow>90.5:
            self.cont=self.cont+1
        #print(self.cont)

    def Cadencia(self,cad,loadCad):

        #self.restAnkle = self.P_RAnkle[0]-self.P_LAnkle[0]
        #self.restAnkle1 = self.P_RAnkle[1]-self.P_LAnkle[1]
        self.restAnkle2 = self.P_RAnkle[2]-self.P_LAnkle[2]
        self.para_cin = {}

        #vec_3 = [self.restAnkle,self.restAnkle1,self.restAnkle2]

        #vec_1 = [self.P_SpineMid[0] - self.P_SpineBase[0], self.P_SpineMid[1] - self.P_SpineBase[1], self.P_SpineMid[2] - self.P_SpineBase[2]]
        #vec_2 = [self.P_LHip[0] - self.P_SpineBase[0], self.P_LHip[1] - self.P_SpineBase[1], self.P_LHip[2] - self.P_SpineBase[2]]

        #vec_gait = self.prod_cruz(vec_1,vec_2)
        #mag_vec_gait = ((vec_gait[0]**2) + (vec_gait[1]**2) + (vec_gait[2]**2))**(1/2)
        #try:
        #    vec_gait = [vec_gait[0]/mag_vec_gait,vec_gait[1]/mag_vec_gait,vec_gait[2]/mag_vec_gait]
        #except:
        #    vec_gait = [0,0,0]       


        #proyeccion = self.prod_punto(vec_3,vec_gait)

        #sign = math.acos(proyeccion/self.Ampli_vec(vec_3))
        
        #if sign < np.pi/2:
        #    proyeccion = proyeccion
        #else:
        
        proyeccion = self.restAnkle2
        

        #print(proyeccion)

        if self.estado == None:
            if proyeccion < 0:
                self.estado = 'Pos'
            else:
                self.estado = 'Neg'
                

        else:
            if self.estado == 'Pos':
                if proyeccion < 0:
                    self.estado = 'Neg'
                    self.t0=time.time()
                    #print('t0: ' + str(self.t0))
                    try:
                        max_pos = max(self.length_step)
                        self.length_step = []
                        tiempo=self.t1-self.t0
                        tiempo=abs(tiempo)
                        cadencia = 1/tiempo
                        vel=max_pos/tiempo
                        self.temp=tiempo
                        self.cad=cadencia
                        self.velo=vel
                        self.long_pas=max_pos
                        self.para_cin['cadencia'] = self.cad
                        self.para_cin['velocidad'] = self.velo
                        self.para_cin['longitud'] = self.long_pas
                        #print('entro 1')
                        #print cad
                        if not cad.is_set():
                            print('entro 2')
                            loadCad.send(self.para_cin)
                            cad.set()
                            
                        #print("paso")

                        
                        #print(self.para_cin)
                        


                        #print('tiempo ' + str(self.cad))
                        #print('long ' + str(self.long_pas))
                        #print('vel ' +str(self.velo))

                        
                        
                    except:
                        print("joder")
                        pass
                else:
                    self.length_step.append(abs(proyeccion))

                    
            elif self.estado == 'Neg':
                if proyeccion > 0:
                    self.estado = 'Pos'
                    self.t1=time.time()
                    #print('t1: ' + str(self.t1))
                    try:
                        max_neg = max(self.length_step)
                        self.length_step = []
                        tiempo=self.t1-self.t0
                        tiempo=abs(tiempo)
                        cadencia = 1/tiempo
                        vel=max_neg/tiempo
                        self.temp=tiempo
                        self.cad=cadencia
                        self.velo=vel
                        self.long_pas=max_neg

                        self.para_cin['cadencia'] = self.cad
                        self.para_cin['velocidad'] = self.velo
                        self.para_cin['longitud'] = self.long_pas

                        #print(self.para_cin)

                        #print('tiempo ' + str(self.cad))
                        #print('long ' + str(self.long_pas))
                        #print('vel ' +str(self.velo))
                    except:
                        pass
                else:
                    self.length_step.append(abs(proyeccion))



    def Ampli_vec(self,vec):
        amp = math.sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)
        return amp

    def prod_punto(self,v1,v2):
        return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

    def prod_cruz(self,v1,v2):
        return [v1[1]*v2[2] - v1[2]*v2[1],v1[2]*v2[0] - v1[0]*v2[2],v1[0]*v2[1] - v1[1]*v2[0]]

    def pause(self):

        self.pause = True

    def get_data(self):
        return(self.data)

    def play(self):
        self._done = False

    def start(self):

        self.go_on = True

    def shutdown(self):

        self.go_on = False

    def launch_thread(self):
        self.kinectThread = threading.Thread(target=self.start2)
        self.kinectThread.start()

    def start2(self):
        self.process()




def Ang_4_puntos(P1,P2,P3,P4):

    #Vector 1

    vecX=P1[0]-P2[0]
    vecY=P1[1]-P2[1]
    vecZ=P1[2]-P2[2]
    mag_vec1=((vecX**2) + (vecY**2) + (vecZ**2))**(1/2)
    try:
        vec1 = [vecX/mag_vec1 , vecY/mag_vec1 , vecZ/mag_vec1 ]
    except:
        vec1 = [0,0,0]  

    vecX2=P3[0]-P4[0]
    vecY2=P3[1]-P4[1]
    vecZ2=P3[2]-P4[2]
    mag_vec2=((vecX2**2) + (vecY2**2) + (vecZ2**2))**(1/2)
    try:
        vec2 = [vecX2/mag_vec2 , vecY2/mag_vec2 , vecZ2/mag_vec2 ]
    except:
        vec2 = [0,0,0]  

    prod = 0
    for m in range (0,2):
        prod = prod + vec1[m]*vec2[m]

    Angulo = math.acos(prod) * (180/np.pi)

    return Angulo


class KinectThread(threading.Thread):
    def __init__(self):
        super(KinectThread, self).__init__()

    def run(self):
        self.kinect = BodyGameRuntime()
        self.kinect.process()

class KinectProcess(object):
    def __init__(self):
        self.onData = multiprocessing.Event()
        self.onCad = multiprocessing.Event()
        self.onShutdown = multiprocessing.Event()
        self.getPipe, self.loadPipe = multiprocessing.Pipe()
        self.getCad, self.loadCad = multiprocessing.Pipe()
        
        self.process = multiprocessing.Process(target = self.kinect_process, args=(self.onData, self.onCad,self.onShutdown,self.getPipe, self.loadPipe,self.loadCad,))

    def get_data(self):
        cad = None
        self.onData.set()
        data  =self.getPipe.recv()
        self.onData.clear()

        #print("data received: " + str(data))
        if self.onCad.is_set():
            cad = self.getCad.recv()
            self.onCad.clear()
           # print "cadence data received: " + str(cad)

        datos_t = {'Angulos': data, 'Param_EspT': cad}
        print(datos_t)
    def shutdown(self):
        self.onShutdown.set()

    
    def launch_process(self):
        self.process.start()
    
    def kinect_process(self, onData, onCad, onShutdown, getPipe, loadPipe, loadCad):
        
        self.kinect = BodyGameRuntime()
        self.kinect.process(req = onData, cad = onCad, end = onShutdown, getPipe = getPipe, loadPipe = loadPipe, loadCad = loadCad)

        
        
def iniciar():
    game = BodyGameRuntime()
    game.process()

#__main__ = "Kinect v2 Body Game"
if __name__ == '__main__':
    """
    #game = BodyGameRuntime()
    #game.launch_thread()
    b = threading.Thread(target=iniciar)
    b.start()
    while True:
        time.sleep(1)
        print('aaa')
    """
    k = KinectProcess()
    k.launch_process()
    for i in range(10):
        k.get_data()
        time.sleep(1)

    print "............shutdown............."
    time.sleep(1)
    k.shutdown()
    time.sleep(3)
