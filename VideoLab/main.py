#!/usr/bin/env pythone3

import cv2, os, sys, time
import numpy as np
from threading import Thread, Semaphore, Lock

#globals
clipFileName = 'clip.mp4'
frameQueue = []
grayQueue = []
framecap = 50


#threads

class ExtractFramesThread (Thread): #exrtacting frame thread
    def __init__(self, semaphore):
        Thread.__init__(self)
        self.vidcap = cv2.VideoCapture(clipFileName) #open video
        self.vidlen = int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT))-1 #video max frames 
        self.queuecap = framecap #how many frames to extract before going to next thread
        self.count = 0 #count of frames done
        self.semaphore = semaphore #lock
    def run(self): #function to run code 
        success, image = self.vidcap.read() #read first frame
        while True:
            self.semaphore.acquire() #lock 
            if success and len(frameQueue) <= self.queuecap: #check that we did read a frame and the queue is not full
                print(f'Reading frame {self.count}')
                frameQueue.append(image) #append to frame queue 
                success, image = self.vidcap.read() #read next frame
                self.count = self.count + 1 #increase count
            self.semaphore.release() #release 
                
            if self.count == self.vidlen: #if the count is equal to the max frames we are done
                print('Extracting Done')
                break
        return

class ConvertToGrayScaleThread(Thread):
    def __init__(self, semaphore):
        Thread.__init__(self)
        self.vidcap = cv2.VideoCapture(clipFileName)
        self.vidlen = int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT))-1
        self.queuecap = framecap
        self.count = 0
        self.semaphore = semaphore
    def run(self):
        while True:
            self.semaphore.acquire()
            if frameQueue and len(grayQueue) <= self.queuecap: #check to see if frameQueue has frames and that gray queue is not full
                print(f'Converting frame {self.count} to grayscale')
                inputFrame = frameQueue.pop(0) # get the first frame in queue
                grayScaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY) # convert to gray scale 
                grayQueue.append(grayScaleFrame) #append to gray queue
                self.count = self.count + 1 #increase frame count 
            self.semaphore.release()
                
            if self.count == self.vidlen:
                print("Done converting to gray scale")
                break
        return

class DisplayFrameThread(Thread):
    def __init__(self,semaphore):
        Thread.__init__(self)
        self.vidcap = cv2.VideoCapture(clipFileName)
        self.vidlen = int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT))-1
        self.delay = 42 #how much time to delay each frame
        self.count = 0
        self.semaphore = semaphore

    def run(self):
        while True:
            self.semaphore.acquire()
            if grayQueue:
                print(f'Displaying frame {self.count}')
                inputFrame = grayQueue.pop(0) # pop first frame i gray queue
                cv2.imshow('video',inputFrame) #display the frame
                self.count = self.count + 1 #increase frame count
                if cv2.waitKey(self.delay) and 0xFF == ord("q"): #delay the frame 
                    break
            self.semaphore.release()
            
            if self.count == self.vidlen:
                break
        cv2.destroyAllWindows() #close all windows of the display video 
        return

def main():
    semaphore = Semaphore()
    extract = ExtractFramesThread(semaphore=semaphore) #create the estract thread
    extract.start() #start the thread
    convert = ConvertToGrayScaleThread(semaphore=semaphore) #create the convert thread
    convert.start() #start the thread
    display = DisplayFrameThread(semaphore=semaphore) #create the display thread
    display.start() #start the thread

if __name__=="__main__":
    main()




