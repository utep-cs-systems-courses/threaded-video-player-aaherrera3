#!/usr/bin/env pythone3

import cv2, os, sys, time
import numpy as np
from threading import Thread, Semaphore, Lock

#globals
clipFileName = 'clip.mp4'
frameQueue = []
grayQueue = []
semaphore = Semaphore(2)


#threads

class ExtractFramesThread (Thread):
    def __init__(self):
        Thread.__init__(self)
        self.vidcap = cv2.VideoCapture(clipFileName)
        self.vidlen = int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT))-1
        self.queuecap = 738
        self.count = 0
    def run(self):
        success, image = self.vidcap.read()
        while True:
            if success and len(frameQueue) <= self.queuecap:
                print(f'Reading frame {self.count}')
                semaphore.acquire()
                frameQueue.append(image)
                semaphore.release()
                success, image = self.vidcap.read()
                self.count = self.count + 1
            if self.count == self.vidlen:
                print('Extracting Done')
                break
        return

class ConvertToGrayScaleThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.vidcap = cv2.VideoCapture(clipFileName)
        self.vidlen = int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT))-1
        self.queuecap = 50
        self.count = 0
    def run(self):
        while True:
            if frameQueue and len(grayQueue) < queuecap:
                print(f'Converting frame {self.count} to grayscale')
                semaphore.acquire()
                inputFrame = frameQueue.pop(0)
                semaphore.release()
                grayScaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)
                semaphore.acquire()
                grayQueue.append(grayScaleFrame)
                semaphore.release()
                self.count = self.count + 1
            if self.count == self.vidlen:
                print("Done converting to gray scale")
                break
        return
    
                
                
                
                
                

            
extract = ExtractFramesThread()
extract.run()
#or x in frameQueue:
#   print('pop')
#   print(frameQueue.pop(0))

