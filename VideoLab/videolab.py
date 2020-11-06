#! /usr/bin/env python3

import cv2, os, sys
from FrameQueue import FrameQueue
from threading import Thread, Semaphore, Lock

videoFile = sys.argv[1] #name of video file 
frameCap = 10 # number of frames per queue
frameQueue = FrameQueue(frameCap) #extracting queue
grayQueue = FrameQueue(frameCap) #converting and displaying queue

class ExtractFramesThread(Thread): 
    def __init__(self):
        Thread.__init__(self)
        self.vidcap = cv2.VideoCapture(videoFile) #open video file to extract
        self.count = 0 #frame count
        
    def run(self):
        success, image = self.vidcap.read() #read first frame 
        while success: #wile still readinga frame
            print(f'Reading frame {self.count}')
            frameQueue.put(image) #insert frame into extract queue
            self.count = self.count + 1 #increase frame count
            success, image = self.vidcap.read() #read next framee
        print('Extraction Complete')
        frameQueue.put("DONE") #Insert termenation key for other threads
            

class GrayScaleThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.count = 0

    def run(self):
        frame = frameQueue.get() #get first frame from extracting queue
        while frame != "DONE": #while we dont see the termination key
            print(f'Converting frame {self.count}')
            grayFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #convert frame to gray scale
            grayQueue.put(grayFrame) #insert into converting and displaying queue
            self.count = self.count + 1 
            frame = frameQueue.get() #get next frame from extracing queue
        print('Converting Done')
        grayQueue.put("DONE") #termination key
        

class DisplayFrameThread(Thread):
    def __init__(self,delay = 42):
        Thread.__init__(self)
        self.count = 0
        self.delay = delay

    def run(self):
        frame = grayQueue.get() #get first frame from converting and displaying queue
        while frame != "DONE":
            print(f'Displaying frame {self.count}')
            cv2.imshow('Video',frame) #display frame
            if cv2.waitKey(self.delay) and 0xFF == ord("q"): #delay frame by delay value
                break
            self.count = self.count + 1 
            frame = grayQueue.get() #get next frame from converting and displaying queue
        print("Display Complete")
        cv2.destroyAllWindows() #close all windows open for displaying video
        

def main():   
    extract = ExtractFramesThread() #create extract thread 
    extract.start() #start extract thread
    
    convert = GrayScaleThread()  #create convert thread
    convert.start()  #start convert thread
    
    display = DisplayFrameThread()  #create display thread
    display.start()  #start display thread

if __name__=="__main__":
    main()

            
        
        
        
        
            
            
