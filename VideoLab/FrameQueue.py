#! /usr/bin/env python3

import cv2, os, sys
from threading import Thread, Semaphore, Lock

class FrameQueue():
    def __init__(self,cap = 10):
        self.queue = []
        self.qLock = Lock()
        self.full = Semaphore(0)
        self.empty = Semaphore(cap)

    def add(self,frame):
        self.empty.acquire()
        self.qLock.acquire()
        self.queue.append(frame)
        self.qLock.release()
        self.full.release()

    def remove(self):
        self.full.acquire()
        self.qLock.acquire()
        return self.queue.pop(0)
        self.qLock.release()
        self.empty.release()


    
