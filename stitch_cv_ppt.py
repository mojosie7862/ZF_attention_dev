from util import *
import random
import tkinter
import cv2
import threading
import time
import os
import win32com.client
import win32api

camwidth = 640
camheight = 480
toggle = 1;
recordingIndex = -999

cam_id = 0
user_initials = "SM"
# numruns = 1
# mindelay = 5
# maxdelay = 10

numruns = 3
mindelay = 3
maxdelay = 5

fishID = "Z1"
gender = "(blank)"
status = "(blank)"
notes = "(blank)"

# pre_stimulus_time = "blank"
# pre_reward_time = "blank"
# reward_aversion_time = "blank"
pre_stimulus_time = 4
pre_reward_time = 4
reward_aversion_time = 4

filename = r'C:\Users\josep\anaconda3\envs\ZF_attention_project\paradigms.pptx'

class VideoRecorder():

    # Video class based on openCV
    def __init__(self, run, paradigm):

        self.open = True
        self.device_index = 0
        self.fps = 6  # fps should be the minimum constant rate at which the camera can
        self.fourcc = "MJPG"  # capture images (with no decrease in speed over time; testing is required)
        self.frameSize = (640, 480)  # video formats and sizes also depend and vary according to the camera used
        self.video_filename = fishID + "_run_" + str(run) + "_" + paradigm + ".avi"
        self.video_cap = cv2.VideoCapture(self.device_index)
        self.video_writer = cv2.VideoWriter_fourcc(*self.fourcc)
        self.video_out = cv2.VideoWriter(self.video_filename, self.video_writer, self.fps, self.frameSize)
        self.frame_counts = 1
        self.start_time = time.time()

    # Video starts being recorded
    def record(self):

        # endtime = sum(fixed_times) / 1000
        # endtime = endtime + pre_stimulus_time + pre_reward_time + reward_aversion_time

        while (self.open == True):
            ret, video_frame = self.video_cap.read()
            if (ret == True):

                self.video_out.write(video_frame)
                self.frame_counts += 1
                time.sleep(0.16)

                gray = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)
                cv2.imshow('video_frame', gray)
                cv2.waitKey(1)
            else:
                break

    # Finishes the video recording therefore the thread too
    def stop(self):

        if self.open == True:

            self.open = False
            self.video_out.release()
            self.video_cap.release()
            cv2.destroyAllWindows()

        else:
            pass

    # Launches the video recording function using a thread
    def start(self):
        video_thread = threading.Thread(target=self.record)
        video_thread.start()

def start_PPTrecording(filename):

    paradigm_slides = [['cf', 12], ['dfm', 7], ['ufm', 2]]
    all_runs = [['cf', 0], ['dfm', 0], ['ufm', 0]]
    global fixed_times
    fixed_times = [1, 1000, 1, 2000, 1]

    app = win32com.client.Dispatch("PowerPoint.Application")
    app.Visible = 1
    app.Presentations.Open(FileName=filename)
    app.ActivePresentation.SlideShowSettings.Run()

    for i in range(numruns):
        this_run = random.choice(paradigm_slides)
        iti = random.randint(mindelay, maxdelay)

        print('run', i + 1, ':', this_run[0], 'ITI:', iti)

        video_thread = VideoRecorder(i, this_run[0])
        video_thread.start()

        win32api.Sleep((pre_stimulus_time * 1000) + 2000)  # pre-stimulus time
        app.SlideShowWindows(1).View.GotoSlide(this_run[1])  # advance to screen cue
        win32api.Sleep(fixed_times[0])  # fixed 1
        app.SlideShowWindows(1).View.Next()  # play screen cue
        win32api.Sleep(fixed_times[1])  # fixed 2
        app.SlideShowWindows(1).View.Next()  # advance to sound slide
        win32api.Sleep(fixed_times[2])  # fixed 3
        app.SlideShowWindows(1).View.Next()  # play CF/FM
        win32api.Sleep(fixed_times[3])  # fixed 4
        app.SlideShowWindows(1).View.Next()  # advance to black slide
        win32api.Sleep(pre_reward_time * 1000)  # pre-reward interval
        app.SlideShowWindows(1).View.Next()  # advance to video slide
        win32api.Sleep(fixed_times[4])  # fixed 5
        app.SlideShowWindows(1).View.Next()  # start video
        win32api.Sleep(reward_aversion_time * 1000)  # reward/aversion time
        app.SlideShowWindows(1).View.Next()  # advance to black slide

        for y, j in enumerate(all_runs):
            if this_run[0] == j[0]:
                j[1] += 1
            if j[1] == numruns / 2:
                paradigm_slides.pop(y)
                all_runs.pop(y)

        time.sleep(iti)
        video_thread.stop()
        while threading.active_count() > 2:
            time.sleep(1)
        if len(all_runs) == 0:
            app.SlideShowWindows(1).View.GotoSlide(1)
            print("Presentation finished.")
            break


start_PPTrecording(filename)