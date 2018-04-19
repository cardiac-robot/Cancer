# coding=utf-8

import sys
import qi
from naoqi import ALModule
from naoqi import ALBroker
import almath
import logging
import time
import random
import threading
import functools


class RobotController(object):

    def __init__(self,settings = { 'name'           : "Hansel",
                                   'ip'             : '192.168.0.102',
                                   'port'           : 9559,
                                   'UseSpanish'     : True,
                                   'MotivationTime' : 300000000

                                 }):
        self.settings = settings
        self.ip = self.settings['ip']
        self.port = self.settings['port']
        self.useSpanish = self.settings['UseSpanish']

        self.session = qi.Session()
        self.robotName = self.settings['name']

        self.go_on = True

        self.session.connect("tcp://" + self.ip + ":" + str(self.port))

        print('vv')

        self.tts = self.session.service("ALTextToSpeech")
        self.setLanguage('Spanish')
        self.animatedSpeechProxy = self.session.service("ALAnimatedSpeech")
        self.motion = self.session.service("ALMotion")
        self.posture = self.session.service("ALRobotPosture")

        
        
    


    
    

        

        
        
        
        
        
