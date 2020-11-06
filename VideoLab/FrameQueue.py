#! /usr/bin/env python3

import cv2, os, sys
from threading import Thread, Semaphore, Lock

class FrameQueue(): #Framed Queue class
    def __init__(self,cap = 10): #cap for queue basic value of 10 can be change
        self.queue = [] # create a list
        self.qLock = Lock() # lock
        self.full = Semaphore(0) #counting lock to see if its full starts at 0
        self.empty = Semaphore(cap) #counting lock to see if its empty starts at cap

    def put(self,frame):
        self.empty.acquire() # acquire from empty
        self.qLock.acquire() # acquire lock
        self.queue.append(frame) # append to queue
        self.qLock.release() # release lock
        self.full.release() # realease from full

    def get(self):
        self.full.acquire() # acquire from full
        self.qLock.acquire() # acquire lcok
        frame = self.queue.pop(0) # pop first element from queue
        self.qLock.release() # release lock
        self.empty.release() # release from empty
        return frame #return frame

    
